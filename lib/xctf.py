import requests
import time
from urllib.parse import urljoin
from lib.scraper import IScraper
import re

def _is_solveditem(item):
    if not (type(item) is dict):
        return False
    if not ("solved" in item):
        return False
    return True



class XCTFScraper(IScraper):
    def __init__(self, url, session):
        # self.eventid = re.search(r"event=(?P<event>[0-9]+)", url).group("event")
        self.event_hash = re.search(r"hash=(?P<hash>[0-9a-f-]+\.event)", url).group("hash")
        self.base = "https://adworld.xctf.org.cn/"
        self.session = session

    def _scoreboard(self):
        total = 0
        cur_rows = []
        while True:
            r = requests.get(urljoin(self.base, "/api/evts/ranks"), params={"order": "asc", "evt": self.event_hash, "offset": len(cur_rows)}, cookies={'session': self.session})
            r.raise_for_status()
            data = r.json()
            total = data["total"]
            cur_rows.extend(data["rows"])
            print("[+] {}/{}".format(len(cur_rows), total))
            if len(cur_rows) >= total:
                break

        return cur_rows

    def _tasks(self):
        r = requests.get(urljoin(self.base, "/api/evts/rank_tasks"), params={"evt": self.event_hash}, cookies={'session': self.session})
        r.raise_for_status()
        data = r.json()
        return data["rows"][0]


    def teams_chals(self):
        team_ids = {t["obj_name"]:[str(k) for k, v in t.items() if _is_solveditem(v)] for t in self._scoreboard()}
        tasks = {str(t["id"]):{"categories":[t["category_name"]], "name":t["task"]["title"]} for cat in self._tasks().values() for t in cat}

        return team_ids, tasks

