# ScryGuy
Unified search across structured data sources

## Requirements

Requires at least python 3.5 as this code uses [type hints](https://peps.python.org/pep-0484/).

## Development

```shell
# install requirements
pip install -r requirements.txt

# run flask
export FLASK_APP=app.py
flask run
```

## How to add new sources

Define your source as a class that implements the methods in `Source` in [`sources.py`](sources.py)

```python
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

```

## Next Steps

- [ ] Replace flask requirement with aioHTTP server
- [ ] Add front page sources