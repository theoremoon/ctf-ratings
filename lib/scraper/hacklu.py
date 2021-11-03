import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from urllib.parse import urljoin
from logging import getLogger, StreamHandler, Formatter
from http.cookies import SimpleCookie
from bs4 import BeautifulSoup
from tqdm import tqdm
import re

logger = getLogger(__name__)
handler = StreamHandler()
handler.setFormatter(Formatter('%(asctime)-15s %(message)s'))
logger.addHandler(handler)

class HackluScraper():
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
        r = self._get("/challenges")
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")
        rows = soup.select("tbody tr")
        tasks = {}
        for row in rows:
            data = row.select("td")
            tasks[data[0].text.strip()] = {
                "category": data[1].text.strip(),
                "tags": [],
            }
        return tasks

    def _team_solves(self, team_url):
        r = self._get(team_url[len(self.url):])
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")
        rows = soup.select("tbody tr")
        solved_tasks = {}
        for row in rows:
            data = row.select("td")
            solved_tasks[data[0].text.strip()] = None
        return solved_tasks

    def scoreboard(self):
        r = self._get("/scoreboard")
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        tasks = self._tasks()

        # parse tbody
        standings = []
        team_urls = []
        rows = soup.select("tbody tr")
        for row in tqdm(rows):
            data = row.select("td")

            pos = int(data[0].text.strip())
            team = data[1].text.strip()
            score = int(re.findall(r"\d+", data[2].text.strip())[0])
            standings.append({
                "team": team,
                "pos": pos,
                "score": score,
                "taskStats": {},
            })
            team_url = data[1].select_one("a")["href"]
            team_urls.append(team_url)

        for i in tqdm(range(len(team_urls))):
            solved_tasks = self._team_solves(team_urls[i])
            standings[i]["taskStats"] = solved_tasks

        return {"tasks": list(tasks.keys()), "standings": standings, "taskinfo": tasks}
