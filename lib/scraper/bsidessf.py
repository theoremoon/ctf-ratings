import requests
from urllib.parse import urljoin
import json
from datetime import datetime

class BSidesSFScraper():
    def __init__(self, url, **kwargs):
        self.url = url

    def _scoreboard(self):
        r = requests.get(urljoin(self.url, "/api/scoreboard"))
        r.raise_for_status()
        ranking = json.loads(r.text.split("\n")[1])["scoreboard"]
        board = []
        for team in ranking:
            board.append({
                "pos": team["position"],
                "team": team["name"],
                "score": team["score"]
            })
        return board

    def _tasks(self):
        r = requests.get(urljoin(self.url, "/api/challenges"))
        r.raise_for_status()
        challenges = json.loads(r.text.split("\n")[1])["challenges"]
        tasks = []
        taskStats = {}
        for challenge in challenges:
            tasks.append(challenge["name"])
            for answer in challenge["answers"]:
                solver = answer["team"]["name"]
                if solver not in taskStats:
                    taskStats[solver] = {}
                taskStats[solver][ challenge["name"] ] = {"points": challenge["current_points"], "time": int(datetime.strptime(answer["timestamp"], "%a, %d %b %Y %H:%M:%S -0000").timestamp())}
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
