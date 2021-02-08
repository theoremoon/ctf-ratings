import requests
import time
from urllib.parse import urljoin
from lib.scraper import IScraper
import re
from typing import Tuple, List

class RCTFScraper(IScraper):
    def __init__(self, url, session):
        self.base = url
        self.token = session

    def _scoreboard(self):
        total = 0
        cur_rows = []
        while True:
            r = requests.get(urljoin(self.base, "/api/v1/leaderboard/now"), params={"limit": 100, "offset": len(cur_rows)})
            r.raise_for_status()
            data = r.json()["data"]
            total = data["total"]
            cur_rows.extend(data["leaderboard"])
            print("[+] {}/{}".format(len(cur_rows), total))
            if len(cur_rows) >= total:
                break
        return cur_rows

    def _team_info(self, team_id: str) -> Tuple[str, List[str]]:
        r = requests.get(urljoin(self.base, "/api/v1/users/{}".format(team_id)))
        r.raise_for_status()
        data = r.json()["data"]
        return data["name"], [s["id"] for s in data["solves"]]


    def _tasks(self):
        r = requests.get(urljoin(self.base, "/api/v1/challs"), headers={'Authorization': "Bearer {}".format(self.token)})
        r.raise_for_status()
        data = r.json()["data"]
        return {str(d["id"]):{"categories":[d["category"]], "name":d["name"]} for d in data}


    def teams_chals(self):
        scoreboard = self._scoreboard()
        team_standings = []
        teams = {}
        for i, t in enumerate(scoreboard):
            if i % 10 == 9:
                time.sleep(1)
                print("{}/{}".format(i+1, len(scoreboard)))
            name, info = self._team_info(t["id"])
            team_standings.append(name)
            teams[name] = info

        tasks = self._tasks()
        return team_standings, teams, tasks

