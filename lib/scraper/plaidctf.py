import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from urllib.parse import urljoin
from datetime import datetime
from logging import getLogger, StreamHandler, Formatter
from tqdm import tqdm
from http.cookies import SimpleCookie

logger = getLogger(__name__)
handler = StreamHandler()
handler.setFormatter(Formatter('%(asctime)-15s %(message)s'))
logger.addHandler(handler)

class PlaidCTFScraper():
    def __init__(self, url, **kwargs):
        self.url = url

        cookies = SimpleCookie()
        if "cookies" in kwargs and kwargs["cookies"]:
            cookies.load(kwargs["cookies"])

        self.cookiejar = requests.cookies.RequestsCookieJar()
        self.cookiejar.update(cookies)

    def _get(self, path):
        s = requests.Session()
        retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 501, 502, 503, 504])
        s.mount("http://", HTTPAdapter(max_retries=retries))
        s.mount("https://", HTTPAdapter(max_retries=retries))
        return s.get(urljoin(self.url, path), cookies=self.cookiejar)

    def _tasks(self):
        r = self._get("/api/challenge")
        r.raise_for_status()
        data = r.json()["challenges"]

        tasks = {}
        for task in data:
            for i, flag in enumerate(task["flags"]):
                tasks[flag["id"]] = "{} - {}".format(task["metadata"]["title"], i + 1)
        return tasks

    def _standings(self):
        r = self._get("/api/scoreboard")
        r.raise_for_status()
        data = r.json()["teams"]
        return [{
            "team": t["name"],
            "pos": t["rank"],
            "score": t["score"],
            "solves": [solve["flagId"] for solve in t["solves"]],
        }for t in data]

    def scoreboard(self):
        tasks = self._tasks()
        standings = self._standings()
        for i in range(len(standings)):
            standings[i]["taskStats"] = {tasks[flagID]: None for flagID in standings[i]["solves"]}
            del standings[i]["solves"]
        return {"tasks": list(tasks.values()), "standings": standings}
