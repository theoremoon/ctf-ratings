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

class CTFdScraper():
    def __init__(self, url, **kwargs):
        self.url = url

        cookies = SimpleCookie()
        if "cookies" in kwargs and kwargs["cookies"]:
            cookies.load(kwargs["cookies"])

        self.cookiejar = requests.cookies.RequestsCookieJar()
        self.cookiejar.update(cookies)

        self.mode = 'teams'
        if 'mode' in kwargs:
            self.mode = kwargs["mode"]  # type: str

    def _get(self, path):
        s = requests.Session()
        retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 501, 502, 503, 504])
        s.mount("http://", HTTPAdapter(max_retries=retries))
        s.mount("https://", HTTPAdapter(max_retries=retries))
        return s.get(urljoin(self.url, path), cookies=self.cookiejar)

    def _team_solves(self, team_id):
        r = self._get("/api/v1/{}/{}/solves".format(self.mode, team_id))
        r.raise_for_status()
        data = r.json()["data"]
        stats = {}
        for stat in data:
            stats[stat["challenge"]["name"]] = {
                "points": stat["challenge"]["value"],
                "time": int(datetime.strptime(
                    stat["date"],
                    "%Y-%m-%dT%H:%M:%S%z"
                ).timestamp()),
            }
        return stats

    def _tasks(self):
        logger.warning("getting tasks...")
        r = self._get("/api/v1/challenges")
        r.raise_for_status()
        data = r.json()["data"]
        logger.warning("done")
        return [task["name"] for task in data]

    def scoreboard(self):
        logger.warning("getting scoreboard...")
        r = self._get("/api/v1/scoreboard")
        r.raise_for_status()
        data = r.json()["data"]
        logger.warning("done")

        tasks = set(self._tasks())
        standings = []
        for team in tqdm(data):
            taskStats = self._team_solves(team["account_id"])
            standings.append({
                "team": team["name"],
                "pos": team["pos"],
                "score": team["score"],
                "id": team["account_id"],
                "taskStats": taskStats,
            })
            tasks.update(taskStats.keys())
        return {"tasks": list(tasks), "standings": standings}
