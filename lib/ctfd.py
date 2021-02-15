import requests
import time
from urllib.parse import urljoin
from lib.scraper import IScraper

class CTFdScraper(IScraper):
    def __init__(self, url, **kwargs):
        self.url = url
        self.session = None
        if 'session' in kwargs:
            self.session = kwargs["session"] # type: str|None
        self.mode = 'teams'
        if 'mode' in kwargs:
            self.mode = kwargs["mode"] # type: str


    def _teams(self):
        if self.session:
            r = requests.get(urljoin(self.url, "/api/v1/scoreboard"), cookies={'session': self.session})
        else:
            r = requests.get(urljoin(self.url, "/api/v1/scoreboard"))
        r.raise_for_status()
        data = r.json()
        return data["data"]

    def _team_solves(self, team: int):
        if self.session:
            r = requests.get(urljoin(self.url, "/api/v1/{}/{}/solves".format(self.mode, team)), cookies={'session': self.session})
        else:
            r = requests.get(urljoin(self.url, "/api/v1/{}/{}/solves".format(self.mode, team)))
        r.raise_for_status()
        data = r.json()
        return data["data"]

    def teams_chals(self):
        teams = self._teams()
        team_standings = [t["name"] for t in teams]


        team_chals = {}
        for i in range(len(teams)):
            if i % 10 == 0:
                time.sleep(1)
                print("[+] progress: {}/{}".format(i+1, len(teams)))

            solves = self._team_solves(teams[i]["account_id"])
            team_chals[teams[i]["name"]] = solves

        team_ids = {}
        challenges = {}
        used_ids = set()
        for t, cs in team_chals.items():
            ids = [str(c["challenge_id"]) for c in cs]
            team_ids[t] = ids
            challenges.update({str(c["challenge_id"]):{"name": c["challenge"]["name"], "categories": [c["challenge"]["category"]]} for c in cs})

        return team_standings, team_ids, challenges

