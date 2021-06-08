import PySimpleGUI as psg
from utils import config, update, week, month, to_datetime
from database import Client

psg.theme("DarkAmber")

class UI:
    def __init__(self):
        self.meta = {}

    def load(self, items: int):
        LOAD = [
            [psg.ProgressBar(items, k='bar')]
        ]
        self.window = psg.Window("Getting Results...", LOAD, finalize=True)

    def update_bar(self, count):
        self.window['bar'].update(count)


    def set_keywords(self, file):
        db = Client(config('mongo_srv_url'))
        db.PDXFDA.Keywords.delete_many({})
        IGNORE = {'','"'}
        with open(file) as f:
            keywords = f.read().lower().split('\n')
            res = db.PDXFDA.Keywords.insert_many([{'keyword': word} for word in keywords if word not in IGNORE])
        
        
    def get_meta(self, values: dict):
        meta = {
            'perf': 'mt' if values['mt'] else 'st',
        }
        if values['custom']:
            meta['start'] = to_datetime(values['from'])
            meta['end'] = to_datetime(values['to'])
        elif values['week']:
            meta['start'], meta['end'] = week()
        elif values['month']:
            meta['start'], meta['end'] = month()
        return meta

    def run(self):
        RUN = [
            [psg.Radio("Multi-threaded", group_id=1, default=True, k='mt'), psg.Radio("Single-threaded", group_id=1, k='st')],
            [psg.Radio("1 Week", group_id=2, default=True, k='week', enable_events=True), psg.Radio("1 Month", group_id=2, k='month', enable_events=True),psg.Radio("Custom Time Range (DD-MM-YYYY) ", group_id=2, k='custom', enable_events=True)],
            [psg.Column([[psg.Text("From: "), psg.InputText(k='from'), psg.Text("To: "), psg.InputText(k='to')]], visible=False, k='range')],
            [psg.Button('Start', k='start')]
        ]
        self.window = psg.Window("Run Script", RUN)
        while True:
            event, values = self.window.read()
            if event == psg.WIN_CLOSED:
                break
            elif event == 'custom':
                self.window['range'].update(visible=True)
            elif event in ('month', 'week'):
                self.window['range'].update(visible=False)
            elif event == 'start':
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
            elif event == 'Save':
                update('mongo_srv_url', values.get('DatabaseUrl'))
                break
            elif event == 'Back':
                break
        self.window.close()
        self.home() 

    def keywords(self):
        KEYWORDS = [
            [psg.FileBrowse('Set Keywords File', file_types=(('TXT Files', '*.txt'),), k='keywordsfile', enable_events=True)]
        ]
        self.window = psg.Window("Set Search Terms", KEYWORDS)
        while True:
            event, values = self.window.read()
            if event == psg.WIN_CLOSED:
                break
            elif event == 'keywordsfile':
                self.set_keywords(values.get('keywordsfile'))
                break
        self.window.close()
        self.home()

    def home(self):
        HOME = [
        [psg.Button("Database", tooltip="Configure MongoDB settings"), psg.Button("Keywords", tooltip="Update search terms")],
        [psg.Button("Run", tooltip="Run the code with the configured settings")],
        ]

        self.window = psg.Window("OpenFDA API Parser", HOME)
        while True:
            event, values = self.window.read()
            if event == psg.WIN_CLOSED:
                break
            elif event == 'Database':
                self.window.close()
                self.database()
            elif event == 'Run':
                self.window.close()
                self.run()
            elif event == 'Keywords':
                self.window.close()
                self.keywords()

