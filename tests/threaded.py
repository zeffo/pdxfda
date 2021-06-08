from threading import Thread
from database import Client
from utils import query, two_weeks
from models import Drug
from logging import getLogger
from utils import check_for_keywords
from errors import APIError

logger = getLogger("pdxfda")


def threadtest():
    data = query(*two_weeks())
    db = Client("mongodb://127.0.0.1:27017")
    keywords = db.get_keywords()
    threads = []
    for item in data["results"]:
        drug = Drug(item)
        if drug.label:
            thread = Thread(target=result, args=(drug, keywords))
            thread.start()
            threads.append(thread)
    for thread in threads:
        thread.join()


def result(drug: Drug, keywords):
    try:
        res = check_for_keywords(drug.label.read(), keywords)
    except APIError:
        res = "404"
    logger.info(res)
