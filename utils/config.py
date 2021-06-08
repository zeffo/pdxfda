import json
from utils import config
from os import getcwd

PATH = f"{getcwd()}/ui/config.json"


def config(key=None) -> dict:
    with open(PATH) as f:
        data = json.load(f)
    return data.get(key) if key else data


def update(setting, value):
    data = config()
    data[setting] = value
    with open(PATH, 'w') as f:
        json.dump(data, f)


    