import gspread
from errors import APIError
from database import Client
from models import Drug, Document, Submission, Product
from utils import query, handle, check_for_keywords, config
from datetime import datetime
import logging
from time import perf_counter
from ui import UI
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from threading import Thread

logging.basicConfig(filename=".log", level=logging.DEBUG)
logger = logging.getLogger("pdxfda")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename=".log", mode="w")
handler.setFormatter(logging.Formatter(r"%(levelname)s - %(message)s"))
logger.addHandler(handler)

# I was forced to make result and async_result for safe parallel and concurrent execution. I would not do this in a normal case


def result(drug: Drug, keywords: list):
    try:
        pdf = drug.label.read()
        found = check_for_keywords(pdf, keywords)
    except APIError:
        pdf = "missing"
        found = None
    data = drug._dict()
    data["flagged"] = found
    data["rejected"] = False
    data["timestamp"] = datetime.utcnow()
    return data

def multithreaded(ui):
    executor = ProcessPoolExecutor()
    db = Client(config("mongo_srv_url"))
    keywords = db.get_keywords()
    rejected = db.get_rejected()
    futures = []
    data = query(ui.meta["start"], ui.meta["end"])
    for item in data["results"]:
        drug = Drug(item)
        if drug.label and drug.id not in rejected:
            fut = executor.submit(result, drug, keywords)
            futures.append(fut)
    ui.load(len(futures))
    done = 0
    for fut in futures:
        res = fut.result()
        done += 1
        db.update_drug(res)
        ui.update_bar(done)
    


async def singlethreaded(ui):
    pass


def main():
    ui = UI()
    ui.home()
    if ui.meta["perf"] == "mt":
        multithreaded(ui)
    else:
        singlethreaded(ui)


if __name__ == "__main__":
    try:
        start = perf_counter()
        main()
        logging.getLogger("pdxfda").info(perf_counter() - start)
    except Exception as error:
        handle(error)
