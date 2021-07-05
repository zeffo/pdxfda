from errors import APIError
from database import Client
from models import Drug
from utils import query, handle, check_for_keywords, config, spreadsheet, to_worksheet
from datetime import datetime
import logging
from time import perf_counter
from ui import UI
from concurrent.futures import ProcessPoolExecutor
import gspread


logging.basicConfig(filename=".log", level=logging.DEBUG)
logger = logging.getLogger("pdxfda")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename=".log", mode="w")
handler.setFormatter(logging.Formatter(r"%(levelname)s - %(message)s"))
logger.addHandler(handler)

# I was forced to make result and async_result for safe parallel and concurrent execution. I would not do this in a normal case


def result(drug: Drug, keywords: list):
    data = drug._dict()
    found = None
    if data["label"] != "missing":
        found = check_for_keywords(drug.label.read(), keywords)
    data["flagged"] = found
    data["rejected"] = False
    data["timestamp"] = datetime.utcnow()
    return data


def multithreaded(ui):
    db = Client(config("mongo_srv_url"))
    keywords = db.get_keywords()
    rejected = db.get_rejected()
    futures = []
    start, end = ui.meta["start"], ui.meta["end"]
    data = query(start, end)
    with ProcessPoolExecutor() as executor:
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
        sh = spreadsheet()
        to_worksheet(sh, "Cancer Related", db.get_flagged_drugs())
        to_worksheet(sh, "Newly added/updated drugs", db.get_new_drugs())
        to_worksheet(sh, "Drugs with Missing Labels", db.get_missing_labels())
        to_worksheet(sh, 'Drugs without cancer-related terms', db.get_missing_drugs())
        sh.del_worksheet(sh.sheet1)
        for email in config("emails"):
            sh.share(email, "user", "writer")
        ui.result(sh.url)


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
