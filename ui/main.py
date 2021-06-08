import PySimpleGUI as psg
from utils import config, update, week, month, to_datetime
from database import Client
from pymongo.errors import ConfigurationError

psg.theme("DarkAmber")


class UI:
    def __init__(self):
        self.meta = {}

    def emails(self):
        loaded = config("emails")

        EMAILS = [
            [psg.Text("\n".join(loaded), k="menu")],
            [psg.InputText(k="input", do_not_clear=False)],
            [
                psg.Button("Add", k="add"),
                psg.Button("Remove", k="remove"),
                psg.Button("Back", k="back"),
            ],
        ]

        self.window = psg.Window("Configure emails", EMAILS)
        while True:
            event, values = self.window.read()
            if event in {psg.WIN_CLOSED, "back"}:
                break
            elif event == "add":
                loaded = config("emails")
                if values["input"] not in loaded:
                    loaded.append(values["input"])
                    update("emails", loaded)
                    longest = len(sorted(loaded, key=lambda s: len(s), reverse=True)[0])
                    self.window["menu"].set_size(size=(longest, len(loaded)))
                    self.window["menu"].update("\n".join(loaded))
            elif event == "remove":
                try:
                    loaded = config("emails")
                    loaded.remove(values["input"])
                    update("emails", loaded)
                    self.window["menu"].update("\n".join(loaded))
                    self.window["menu"].set_size(size=(None, len(loaded)))
                except ValueError:
                    pass

        self.window.close()
        self.home()

    def load(self, items: int):
        LOAD = [[psg.ProgressBar(items, k="bar")]]
        self.window = psg.Window("Getting Results...", LOAD, finalize=True)

    def update_bar(self, count):
        self.window["bar"].update(count)

    def set_keywords(self, file):
        db = Client(config("mongo_srv_url"))
        db.PDXFDA.Keywords.delete_many({})
        IGNORE = {"", '"'}
        with open(file) as f:
            keywords = f.read().lower().split("\n")
            res = db.PDXFDA.Keywords.insert_many(
                [{"keyword": word} for word in keywords if word not in IGNORE]
            )

    def get_meta(self, values: dict):
        meta = {
            "perf": "mt" if values["mt"] else "st",
        }
        if values["custom"]:
            meta["start"] = to_datetime(values["from"])
            meta["end"] = to_datetime(values["to"])
        elif values["week"]:
            meta["start"], meta["end"] = week()
        elif values["month"]:
            meta["start"], meta["end"] = month()
        return meta

    def run(self):
        RUN = [
            [
                psg.Radio("Multi-threaded", group_id=1, default=True, k="mt"),
                psg.Radio("Single-threaded", group_id=1, k="st"),
            ],
            [
                psg.Radio(
                    "1 Week", group_id=2, default=True, k="week", enable_events=True
                ),
                psg.Radio("1 Month", group_id=2, k="month", enable_events=True),
                psg.Radio(
                    "Custom Time Range (DD-MM-YYYY) ",
                    group_id=2,
                    k="custom",
                    enable_events=True,
                ),
            ],
            [
                psg.Column(
                    [
                        [
                            psg.Text("From: "),
                            psg.InputText(k="from"),
                            psg.Text("To: "),
                            psg.InputText(k="to"),
                        ]
                    ],
                    visible=False,
                    k="range",
                )
            ],
            [psg.Button("Start", k="start")],
        ]
        self.window = psg.Window("Run Script", RUN)
        while True:
            event, values = self.window.read()
            if event == psg.WIN_CLOSED:
                break
            elif event == "custom":
                self.window["range"].update(visible=True)
            elif event in ("month", "week"):
                self.window["range"].update(visible=False)
            elif event == "start":
                self.meta = self.get_meta(values)
                break

        self.window.close()
        return

    def database(self):
        DATABASE = [
            [psg.Text("Enter your MongoDB SRV URL: ")],
            [psg.Input(default_text=config("mongo_srv_url"), key="DatabaseUrl")],
            [psg.Button("Save"), psg.Button("Back")],
        ]

        self.window = psg.Window("Database Settings", DATABASE)
        while True:
            event, values = self.window.read()
            if event == psg.WIN_CLOSED:
                break
            elif event == "Save":
                update("mongo_srv_url", values.get("DatabaseUrl"))
                break
            elif event == "Back":
                break
        self.window.close()
        self.home()

    def keywords(self):
        KEYWORDS = [
            [
                psg.Text(
                    "Please set a valid Mongo SRV URL first!", visible=False, k="warn"
                )
            ],
            [
                psg.FileBrowse(
                    "Set Keywords File",
                    file_types=(("TXT Files", "*.txt"),),
                    k="keywordsfile",
                    enable_events=True,
                )
            ],
        ]
        self.window = psg.Window("Set Search Terms", KEYWORDS)
        while True:
            event, values = self.window.read()
            if event == psg.WIN_CLOSED:
                break
            elif event == "keywordsfile":
                try:
                    self.set_keywords(values.get("keywordsfile"))
                except ConfigurationError:
                    self.window["warn"].update(visible=True)
                else:
                    self.window["warn"].update(visible=False)
                    break
        self.window.close()
        self.home()

    def home(self):
        HOME = [
            [
                psg.Button("Database", tooltip="Configure MongoDB settings"),
                psg.Button("Keywords", tooltip="Update search terms"),
                psg.Button("Emails", tooltip="Configure output emails"),
            ],
            [psg.Button("Run", tooltip="Run the code with the configured settings")],
        ]

        self.window = psg.Window("OpenFDA API Parser", HOME)
        while True:
            event, values = self.window.read()
            if event == psg.WIN_CLOSED:
                self.window.close()
                break
            elif event == "Database":
                self.window.close()
                self.database()
            elif event == "Run":
                self.window.close()
                self.run()
            elif event == "Keywords":
                self.window.close()
                self.keywords()
            elif event == "Emails":
                self.window.close()
                self.emails()
