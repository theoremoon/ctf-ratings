import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from urllib.parse import urljoin
import json
from datetime import datetime

class D3CTFScraper():
    def __init__(self, url, **kwargs):
        self.url = url
        self.session = kwargs["session"]
        self.token = kwargs["token"]

    def _get(self, path):
        s = requests.Session()
        retries = Retry(backoff_factor=5, status_forcelist=[500, 501, 502, 503, 504])
        s.mount("http://", HTTPAdapter(max_retries=retries))
        s.mount("https://", HTTPAdapter(max_retries=retries))
        return s.get(urljoin(self.url, path), cookies={'laravel_session': self.session}, headers={'Authorization': "Bearer {}".format(self.token)})

    def _scoreboard(self):
        page = 1
        count = 0
        teams = []
        while True:
            r = self._get("/API/Team/ranking?language=en&page={}&withCount=false".format(page))
            r.raise_for_status()
            data = r.json()["data"]
            count = data["total"]
            for team in data["ranking"]:
                teams.append({
                    "pos": len(teams) + 1,
                    "team": team["team_name"],
                    "score": team["dynamic_total_score"]
                })
            if count <= len(teams):
                break

        removeindex = []
        for i in range(len(teams)):
            if teams[i]["score"] == 0:
                removeindex.append(i)
        for i in removeindex[::-1]:
            del teams[i]

        return teams

    def _tasks(self):
        r = self._get("/API/Challenge/list?language=en")
        r.raise_for_status()
        data = r.json()["data"]
        challenges = data["challenges"]

        tasks = []
        taskStats = {}
        for cat in challenges.values():
            for cat2 in cat.values():
                for challenge in cat2:
                    tasks.append(challenge["title"])
                    r2 = self._get("/API/Challenge/solvedTeams?language=en&challengeId={}".format(challenge["challenge_id"]))
                    r2.raise_for_status()
                    solved = r2.json()["data"]
                    for solve in solved:
                        solver = solve["teamName"]
                        if solver not in taskStats:
                            taskStats[solver] = {}
                        taskStats[solver][challenge["title"]] = {"points": challenge["nowScore"], "time": int(datetime.strptime(solve["solvedAt"], "%Y-%m-%dT%H:%M:%S+00:00").timestamp())}
        return tasks, taskStats

    def scoreboard(self):
        board = self._scoreboard()
        tasks, taskStats = self._tasks()
        for i in range(len(board)):
            if board[i]["team"] in taskStats:
                board[i]["taskStats"] = taskStats[ board[i]["team"] ]
            else:
                board[i]["taskStats"] = {}
        return {"tasks": tasks, "standings": board}
