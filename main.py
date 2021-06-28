from errors import APIError
from database import Client
from models import Drug
from utils import handle, check_for_keywords, config, spreadsheet, to_worksheet, query_from_config
from datetime import datetime
import logging
from time import perf_counter
from concurrent.futures import ProcessPoolExecutor

logging.basicConfig(filename=".log", level=logging.DEBUG)
logger = logging.getLogger("pdxfda")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename=".log", mode="w")
handler.setFormatter(logging.Formatter(r"%(levelname)s - %(message)s"))
logger.addHandler(handler)


def result(drug: Drug, keywords: list):
    # Need to store: Name, NDA, Label, Found Keywords (flagged), Rejection Status, Timestamp
    data = drug._dict()
    found = None
    if data["label"] != "missing":
        found = check_for_keywords(drug.label.read(), keywords)
    data["flagged"] = found
    data["rejected"] = False
    data["timestamp"] = datetime.utcnow()
    return data

def main():
    db = Client(config('mongo_srv_url'))
    keywords = db.get_keywords()
    rejected = db.get_rejected()
    futures = []
    data = query_from_config()

    with ProcessPoolExecutor() as executor:
        for item in data["results"]:
            drug = Drug(item)
            if drug.id not in rejected:
                fut = executor.submit(result, drug, keywords)
                futures.append(fut)

    for fut in futures:
        res = fut.result()
        db.update_drug(res)

    sh = spreadsheet()
    to_worksheet(sh, "Cancer Related", db.get_flagged_drugs())
    to_worksheet(sh, "Newly added/updated drugs", db.get_new_drugs())
    to_worksheet(sh, "Drugs with Missing Labels", db.get_missing_labels())
    sh.del_worksheet(sh.sheet1)
    for email in config('emails'):
        sh.share(email, 'user', 'writer')

    print("Data sent to", sh.url)


if __name__ == "__main__":
    try:
        start = perf_counter()
        main()
        logging.getLogger("pdxfda").info(perf_counter() - start)
    except Exception as error:
        handle(error)
