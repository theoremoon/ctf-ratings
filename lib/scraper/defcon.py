import math
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from urllib.parse import urljoin
from logging import getLogger, StreamHandler, Formatter
from http.cookies import SimpleCookie

logger = getLogger(__name__)
handler = StreamHandler()
handler.setFormatter(Formatter('%(asctime)-15s %(message)s'))
logger.addHandler(handler)

class DEFCONScraper():
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
        r = self._get("/challenges.json")
        r.raise_for_status()
        return [task[0] for task in r.json()['message']['open']]

    def _solves(self):
        r = self._get("/challenges.json")
        r.raise_for_status()
        return [{
            'task': solve[0],
            'team': solve[1],
            'time': int(float(solve[2])),
        } for solve in r.json()['message']['solves']]

    def _taskPoint(self, solves: int) -> int:
      if solves < 2:
          return 500
      return int(100 + 400 / (1 + 0.08 * solves * math.log(solves)))

    def scoreboard(self):
        tasks = self._tasks()
        teams = {}
        solveCount = {task:0 for task in tasks}

        for solve in self._solves():
            if solve["team"] not in teams:
                teams[solve["team"]] = {
                    "team": solve["team"],
                    "pos": 0,
                    "score": 0,
                    "taskStats": {},
                }
            teams[solve["team"]]["taskStats"][solve["task"]] = {
                "time": solve["time"]
            }
            solveCount[solve["task"]] += 1

        taskPoints = {
            task: self._taskPoint(solveCount[task])
            for task in tasks
        }

        teamList = list(teams.values())
        for i in range(len(teamList)):
            teamList[i]["score"] = sum(taskPoints[task] for task in teamList[i]["taskStats"].keys())

        teamList = sorted(teamList, key=lambda x: (x["score"], -max(v["time"] for v in x["taskStats"].values()) ), reverse=True)
        for i in range(len(teamList)):
            teamList[i]["pos"] = i+1

        return {"tasks": tasks, "standings": teamList}
