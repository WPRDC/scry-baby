from functools import lru_cache
from typing import TypedDict

import aiohttp


class ResultRecord(TypedDict):
    """ Format of search response record item """
    # unique id across all sources
    uid: str

    # string slug that should be unique across items from the same source
    slug: str

    # name of the object that will be displayed in search etc
    name: str

    # name of the object that will be displayed in search etc
    description: str

    # url to director searchers for the item
    link_url: str


class Source:
    """
    Describes how a WPRDC source of data for use in search.
    """
    path: str = '/'
    host: str = '127.0.0.1'
    session: aiohttp.ClientSession = None

    def get_url(self, query: str) -> str:
        """ Returns the full URL with path and query string"""
        raise NotImplementedError

    def get_path_with_qs(self, obj: str) -> str:
        """ Returns the path and query string without the host """
        raise NotImplementedError

    def transform_response(self, obj: str) -> list[ResultRecord]:
        """ Parse response, extract the relevant items, and return them as ResultRecords"""
        raise NotImplementedError


class ProfilesSource(Source):
    path: str = '/'
    host: str = 'https://api.profiles.wprdc.org'
    session: aiohttp.ClientSession = None

    # base path for profiles site
    _link_base_path: str = 'https://profiles.wprdc.org'

    _url: str = None

    def __init__(self, path):
        self.path = path

    @lru_cache
    def get_url(self, query: str) -> str:
        return f'{self.host}{self.get_path_with_qs(query)}'

    @lru_cache
    def get_path_with_qs(self, query: str) -> str:
        return f'{self.path}?search={query}'

    def transform_response(self, obj: dict) -> list[ResultRecord]:
        results: list[ResultRecord] = []
        if 'results' in obj:
            for item in obj['results']:
                results.append(self._transform_record(item))
        return results

    def _transform_record(self, obj: dict) -> ResultRecord:
        """ Handles transforming individual records"""
        return {
            'uid': f"profiles{self.path}/{obj['slug']}",
            'slug': obj['slug'],
            'name': obj['name'],
            'description': obj['description'],
            'link_url': f"{self._link_base_path}/{obj['slug']}"
        }
