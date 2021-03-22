import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from urllib.parse import urljoin
from datetime import datetime
from bs4 import BeautifulSoup
import re
import time
from logging import getLogger, StreamHandler, Formatter

logger = getLogger(__name__)
handler = StreamHandler()
handler.setFormatter(Formatter('%(asctime)-15s %(message)s'))
logger.addHandler(handler)

class LegacyCTFdScraper():
    def __init__(self, url, **kwargs):
        self.url = url
        if "session" in kwargs:
            self.session = kwargs["session"]

        self.mode = 'teams'
        if 'mode' in kwargs:
            self.mode = kwargs["mode"]  # type: str

    def _get(self, path):
        s = requests.Session()
        retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 501, 502, 503, 504])
        s.mount("http://", HTTPAdapter(max_retries=retries))
        s.mount("https://", HTTPAdapter(max_retries=retries))
        if self.session:
            return s.get(urljoin(self.url, path), cookies={'session': self.session})
        else:
            return s.get(urljoin(self.url, path))

    def _teams(self):
        logger.warning("[+] get scoreboard...")
        r = self._get("/scoreboard")
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        hdr = soup.select("#scoreboard thead th")
        score_index = -1
        for i, th in enumerate(hdr):
            if re.match(r"^score$", th.text, re.IGNORECASE):
                score_index = i
                break
        else:
            raise ValueError("[-] failed to find score index")

        trs = soup.select("#scoreboard tbody tr")
        teams = []
        for tr in trs:
            id = tr.find("a")["href"].split("/")[-1]
            name = tr.find("a").text.strip()
            score = int(tr.find_all("td")[score_index].text)
            teams.append({"id": id, "team": name, "pos": len(teams) + 1, "score": score, "taskStats": {}})
        logger.warning("[+] done")
        return teams

    def _team_solves(self, team_id):
        r = self._get("/{}/{}".format(self.mode, team_id))
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        trs = soup.select("table tbody tr")
        tasks = {}
        for tr in trs:
            if len(tr.find_all("td")) != 4:
                continue

            name = tr.find("a").text.strip()
            score = tr.find_all("td")[2].text
            datestr = tr.select("span[data-time]")[0]["data-time"].strip()
            datestr = re.sub(r"\.[0-9]+", "", datestr)
            time = datetime.strptime(datestr, "%Y-%m-%dT%H:%M:%SZ")
            tasks[name] = {"points": score, "time": int(time.timestamp())}
        return tasks

    def _teams_tasks(self):
        """
        問題のIDはstrで管理する
        """
        teams = self._teams()
        tasks = set()

        for i in range(len(teams)):
            if i % 10 == 0:
                time.sleep(0.5)
                logger.warning("[+] progress: {}/{}".format(i + 1, len(teams)))

            solves = self._team_solves(teams[i]["id"])
            tasks.update(solves.keys())
            teams[i]["taskStats"] = solves

        return teams, list(tasks)

    def scoreboard(self):
        board, tasks = self._teams_tasks()
        return {"tasks": tasks, "standings": board}
