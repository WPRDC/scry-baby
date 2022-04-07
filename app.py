import asyncio
import time
from typing import Mapping

import aiohttp
from flask import Flask, request

from settings import ACTIVE_SOURCES
from sources import Source, ResultRecord

app = Flask(__name__)


def s2c(s):
    """ Snake- to camel-case"""
    parts = s.split('_')
    return parts[0] + ''.join(x.title() for x in parts[1:])


def snake_to_camel_fields(d: dict):
    """ Returns dict but with keys in camel-case for use in api output """
    return {s2c(k): v for (k, v) in d.items()}


async def search_site(source: Source, query: str, **kwargs) -> list[ResultRecord]:
    url = source.get_url(query)
    print(f'Getting data for {url}')
    resp = await source.session.request('GET', url=source.get_path_with_qs(query), **kwargs)
    data = await resp.json()
    print(f'Received data for {url}')
    return source.transform_response(data)


async def search_across_sites(query: str):
    tasks = []
    saved_sessions: Mapping[str, aiohttp.ClientSession] = {}

    # Have sources with the same host use a shared session
    # for each source
    for source in ACTIVE_SOURCES:
        # make or get its session
        if source.host not in saved_sessions:
            saved_sessions[source.host] = aiohttp.ClientSession(source.host)
        source.session = saved_sessions[source.host]
        tasks.append(search_site(source, query))

    data = await asyncio.gather(*tasks)
    for sesh in saved_sessions.values():
        await sesh.close()
    # flatten the list and return it
    return [item for datum in data for item in datum]


@app.route('/', methods=['GET'])
async def search():
    start = time.time()
    query = request.args.get('q', None)
    if query:
        results = await search_across_sites(query)
        end = time.time()
        return {
            'count': len(results),
            'elapsed_time': end - start,
            'sources': [source.get_url(query) for source in ACTIVE_SOURCES],
            'results': [snake_to_camel_fields(item) for item in results]
        }
    return {}


if __name__ == '__main__':
    app.run()
