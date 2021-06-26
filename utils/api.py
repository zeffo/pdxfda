from requests import get
from typing import Optional
from datetime import datetime
from errors import APIError
from aiohttp import ClientSession
from .config import config
import gspread
from logging import getLogger

logger = getLogger('pdxfda')


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


def to_worksheet(sh, name: str, data) -> None:
    """ Makes a new worksheet """
    if data:
        ws = sh.add_worksheet(title=name, rows=str(len(data)), cols=str(len(data[0])))
        ws.insert_rows(data)
    else:
        logger.warning(f'{name} has no data!')

def spreadsheet():
    gc = gspread.service_account(filename='auth.json')
    sh = gc.create(f"Drug Approval Data ({datetime.now()})")
    for email in config("emails"):
        sh.share(email, perm_type='user', role='writer')
    return sh