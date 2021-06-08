from utils import async_query, check_for_keywords
from models import Drug
from datetime import datetime, timezone, timedelta
from database import AsyncClient
from asyncio import get_running_loop, create_task, gather
from logging import getLogger
from errors import APIError

logger = getLogger("pdxfda")


async def aiotest():
    db = AsyncClient(
        "mongodb://127.0.0.1:27017/?compressors=disabled&gssapiServiceName=mongodb"
    )
    end = datetime.now(tz=timezone(offset=-timedelta(hours=4)))
    start = end - timedelta(hours=504)
    data = await async_query(start, end)
    tasks = []
    for item in data["results"]:
        drug = Drug(item)
        if drug.label:
            tasks.append(create_task(result(drug, db)))
    await gather(*tasks)


async def result(drug: Drug, db: AsyncClient):
    try:
        res = await get_running_loop().run_in_executor(
            None,
            check_for_keywords,
            await drug.label.async_read(),
            await db.get_keywords(),
        )
    except APIError:
        res = "404"
    logger.info(res)
