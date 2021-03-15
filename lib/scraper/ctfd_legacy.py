import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from urllib.parse import urljoin
from datetime import datetime
from bs4 import BeautifulSoup
import re
import time

class LegacyCTFdScraper():
    def __init__(self, url, **kwargs):
        self.url = url
        if "session" in kwargs:
            self.session = kwargs["session"]

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
        print("[+] get scoreboard...")
        r = self._get("/scoreboard")
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        trs = soup.select("#scoreboard tbody tr")
        teams = []
        for tr in trs:
            team_id = tr.find("a")["href"].split("/")[-1]
            team_name = tr.find("a").text
            score = int(tr.find_all("td")[-1].text)
            teams.append({"id": team_id, "name": team_name, "pos": len(teams), "score": score, "taskStats": {}})
        print("[+] done")
        return teams

    def _team_solves(self, team_id):
        print("[+] get team solves...")
        r = self._get("/{}/{}".format(self.mode[:-1], team_id))
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        trs = soup.select("table tbody tr")
        tasks = {}
        for tr in trs:
            name = tr.find("a").text
            score = tr.select("td")[2].text
            datestr = tr.select("td")[3].text
            time = datetime.strptime(re.sub(r"([0-9])(th|st|nd|rd)", r"\1", datestr), "%B %d, %I:%M:%S %p")
            time = time.replace(year=datetime.now().year)
            tasks[name] = {"points": score, "time": int(time.timestamp())}

        print("[+] done")
        return tasks

    def _teams_tasks(self):
        """
        問題のIDはstrで管理する
        [順位に昇順なチーム名], {チーム名:[チームが解いた問題のID]}, {問題ID:問題の詳細}
        """
        teams = self._teams()
        tasks = set()

        for i in range(len(teams)):
            if i % 10 == 0:
                time.sleep(0.5)
                print("[+] progress: {}/{}".format(i+1, len(teams)))

            solves = self._team_solves(teams[i]["id"])
            tasks.update(solves.keys())
            teams[i]["taskStats"] = solves

        return teams, list(tasks)

    def scoreboard(self):
        board, tasks = self._teams_tasks()
        return {"tasks": tasks, "standings": board}
