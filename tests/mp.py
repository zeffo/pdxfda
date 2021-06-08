from concurrent.futures import ProcessPoolExecutor
from database import Client
from utils import query, two_weeks
from models import Drug
from logging import getLogger
from utils import check_for_keywords
from errors import APIError

logger = getLogger("pdxfda")


def mptest():
    data = query(*two_weeks())
    db = Client("mongodb://127.0.0.1:27017")
    keywords = db.get_keywords()
    futures = []
    executor = ProcessPoolExecutor()
    for item in data["results"]:
        drug = Drug(item)
        if drug.label:
            fut = executor.submit(result, drug, keywords)
            futures.append(fut)
    for future in futures:
        future.result()


def result(drug: Drug, keywords):
    try:
        res = check_for_keywords(drug.label.read(), keywords)
    except APIError:
        res = "404"
    logger.info(res)
