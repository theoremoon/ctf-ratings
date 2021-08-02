import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from urllib.parse import urljoin
from logging import getLogger, StreamHandler, Formatter
from http.cookies import SimpleCookie
from bs4 import BeautifulSoup
from tqdm import tqdm

logger = getLogger(__name__)
handler = StreamHandler()
handler.setFormatter(Formatter('%(asctime)-15s %(message)s'))
logger.addHandler(handler)

class ImaginaryCTFScraper():
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

    def _team_solved(self, link):
        r = self._get(link)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        rows = soup.select("tbody tr")
        tasks = {}
        for row in rows:
            tasks[row.select("td")[0].text.strip()] = None
        return tasks

    def scoreboard(self):
        r = self._get("/Leaderboard")
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        # parse tbody
        tasks = set()
        standings = []
        rows = soup.select("tbody tr")
        for row in tqdm(rows):
            data = row.select("td")

            pos = int(data[0].text.strip())
            score = int(data[2].text.strip())

            team = row.select_one("a")
            teamname = team.text.strip()
            team_solved = self._team_solved(team["href"])
            tasks.update(list(team_solved.keys()))

            standings.append({
                "team": teamname,
                "pos": pos,
                "score": score,
                "taskStats": team_solved,
            })
        return {"tasks": list(tasks), "standings": standings}
