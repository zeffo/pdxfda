import json
from utils import config
from os import getcwd

PATH = f"{getcwd()}/ui/config.json"


def config(key=None) -> dict:
    try:
        with open(PATH) as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"mongo_srv_url": "", "emails": []}
        with open(PATH, "w") as f:
            json.dump(data, f)
    return data.get(key) if key else data


def update(setting, value):
    data = config()
    data[setting] = value
    with open(PATH, "w") as f:
        json.dump(data, f)
