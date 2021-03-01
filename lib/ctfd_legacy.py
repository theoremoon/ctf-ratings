import requests
from bs4 import BeautifulSoup
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import time
from urllib.parse import urljoin
from lib.scraper import IScraper

class CTFdLegacyScraper(IScraper):
    def __init__(self, url, **kwargs):
        self.url = url
        self.session = None
        if 'session' in kwargs:
            self.session = kwargs["session"] # type: str|None
        self.mode = 'teams'
        if 'mode' in kwargs:
            self.mode = kwargs["mode"] # type: str

    def _get(self, path):
        s = requests.Session()
        retries = Retry(backoff_factor=5, status_forcelist=[500, 501, 502, 503, 504])
        s.mount("http://", HTTPAdapter(max_retries=retries))
        s.mount("https://", HTTPAdapter(max_retries=retries))
        if self.session:
            return s.get(urljoin(self.url, path), cookies={'session': self.session})
        else:
            return s.get(urljoin(self.url, path))


    def _teams(self):
        r = self._get("/scoreboard")
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        trs = soup.select("#scoreboard tbody tr")
        teams = []
        for tr in trs:
            team_id = tr.find("a")["href"].split("/")[-1]
            team_name = tr.find("a").text
            teams.append({"account_id": team_id, "name": team_name})
        return teams

    def _team_solves(self, team: int):
        r = self._get("/{}/{}".format(self.mode[:-1], team))
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        trs = soup.select("table tbody tr")
        tasks = []
        for tr in trs:
            task_id = tr.find("a")["href"].split("#")[-1]
            task_name = tr.find("a").text
            task_category = tr.select("td")[1].text
            tasks.append({"challenge_id": task_id, "challenge": {"name": task_name, "category": task_category}})

        return tasks

    def teams_chals(self):
        """
        問題のIDはstrで管理する
        [順位に昇順なチーム名], {チーム名:[チームが解いた問題のID]}, {問題ID:問題の詳細}
        """
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

