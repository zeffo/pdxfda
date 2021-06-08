from requests import get
from typing import Optional
from datetime import datetime
from errors import APIError
from aiohttp import ClientSession


def query(start: datetime, end: datetime) -> dict:
    """Makes an API query within the given timeframe. Returns the API response as a `dict`. Raises APIError if the HTTP response is not `200 OK`."""
    strf = r"%Y-%m-%d"
    url = f"https://api.fda.gov/drug/drugsfda.json?search=submissions.submission_status_date:[{start.strftime(strf)}+TO+{end.strftime(strf)}]&limit=1000"
    resp = get(url)
    if resp.status_code == 200:
        return resp.json()
    else:
        raise APIError(resp.status_code)


async def async_query(start: datetime, end: datetime, session: ClientSession) -> dict:
    """Makes an API query asynchronously within the given timeframe. Returns the API response as a `dict`. Raises APIError if the HTTP response is not `200 OK`."""
    strf = r"%Y-%m-%d"
    url = f"https://api.fda.gov/drug/drugsfda.json?search=submissions.submission_status_date:[{start.strftime(strf)}+TO+{end.strftime(strf)}]&limit=1000"
    async with session.get("get", url) as resp:
        if resp.status == 200:
            return await resp.json()
        else:
            raise APIError(resp.status)
