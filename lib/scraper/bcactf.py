import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from logging import getLogger, StreamHandler, Formatter
from http.cookies import SimpleCookie
from tqdm import tqdm
import dateparser

logger = getLogger(__name__)
handler = StreamHandler()
handler.setFormatter(Formatter('%(asctime)-15s %(message)s'))
logger.addHandler(handler)

class BCACTFScraper():
    def __init__(self, url, **kwargs):
        self.url = url
        cookies = SimpleCookie()
        if "cookies" in kwargs:
            cookies.load(kwargs["cookies"])

        self.cookiejar = requests.cookies.RequestsCookieJar()
        self.cookiejar.update(cookies)

    def _get(self, path):
        s = requests.Session()
        retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 501, 502, 503, 504])
        s.mount("http://", HTTPAdapter(max_retries=retries))
        s.mount("https://", HTTPAdapter(max_retries=retries))
        return s.get(urljoin(self.url, path), cookies=self.cookiejar, verify=False)

    def _tasks(self):
        r = self._get("/challenges")
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        tasknames = soup.select(".challenge-group h3")

        return [t.text.strip() for t in tasknames]

    def _team(self, path):
        r = self._get(path)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        rows = soup.select("#solves tr")

        stats = {}
        for row in rows:
            data = row.select("td")
            task = data[0].text.strip()
            score = int(data[1].text.strip())
            solved_at = int(dateparser.parse(data[3].find("abbr")["title"]).timestamp())
            stats[task] = {
                "points": score,
                "time": solved_at,
            }
        return stats

    def _teams(self):
        logger.warning("getting scoreboard...")
        r = self._get("/scoreboard")
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")
        rows = soup.select("#teams tr")
        teams = []
        for row in tqdm(rows):
            data = row.select("td")
            pos = int(data[0].text.strip())
            team = data[1].text.strip()
            score = int(data[3].text.strip())
            if score <= 0:
                continue
            teams.append({
                "team": team,
                "pos": pos,
                "score": score,
                "taskStats": self._team(data[1].find("a")["href"]),
            })
        return teams

    def scoreboard(self):
        standings = self._teams()
        tasks = self._tasks()

        return {"standings": standings, "tasks": tasks}
