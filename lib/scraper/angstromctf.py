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

class AngstromCTFScraper():
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

    def _teams(self):
        r = self._get("teams?frozen=1")
        r.raise_for_status()
        data = r.json()

        teams = [{
            "id": team["id"],
            "team": team["name"],
            "pos": 0,
            "score": team["score"],
            "lastSolve": int(
                datetime.strptime(
                    team["lastSolve"].split(".")[0],
                    "%Y-%m-%dT%H:%M:%S"
                ).timestamp()
            ),
            "taskStats": {},
        } for team in data if team["score"] > 0 and "lastSolve" in team]
        teams = sorted(teams, key=lambda x: (x["score"], -x["lastSolve"]), reverse=True)
        for i in range(len(teams)):
            teams[i]["pos"] = i + 1

        return teams

    def _team_solves(self, team_id):
        r = self._get("teams/{}".format(team_id))
        r.raise_for_status()
        data = r.json()
        stats = {}
        for stat in data["solves"]:
            stats[stat["challenge"]["title"]] = {
                "points": stat["challenge"]["value"],
                "time": int(datetime.strptime(
                    stat["time"].split(".")[0],
                    "%Y-%m-%dT%H:%M:%S"
                ).timestamp()),
            }
        return stats

    def _tasks(self):
        r = self._get("challenges")
        r.raise_for_status()
        data = r.json()
        return [task["title"] for task in data]

    def scoreboard(self):
        logger.warning("getting scoreboard...")
        teams = self._teams()
        logger.warning("done")

        logger.warning("getting tasks...")
        tasks = self._tasks()
        logger.warning("done")

        logger.warning("getting teams...")
        standings = []
        for team in tqdm(teams):
            taskStats = self._team_solves(team["id"])
            standings.append({
                "team": team["team"],
                "pos": team["pos"],
                "score": team["score"],
                "id": team["id"],
                "taskStats": taskStats,
            })
        logger.warning("done")
        return {"tasks": list(tasks), "standings": standings}
