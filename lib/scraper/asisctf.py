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

class AsisCTFScraper():
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

    def scoreboard(self):
        r = self._get("/scoreboard")
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")

        # parse thead
        tasks = soup.select("thead tr th")[4:]  # skip #, Team, Points, Country
        tasks = [t.text.strip() for t in tasks]

        # parse tbody
        standings = []
        rows = soup.select("tbody tr")
        for row in tqdm(rows):
            heads = row.select("th")
            data = row.select("td")

            pos = int(heads[0].text.strip())
            team = data[0].text.strip()
            score = int(data[1].text.strip())

            solves = solves = row.select(".chall")
            solves = [len(solve.select("svg")) > 0 for solve in solves]
            assert len(tasks) == len(solves)
            taskStats = {tasks[i]: None for i in range(len(tasks)) if solves[i]}

            standings.append({
                "team": team,
                "pos": pos,
                "score": score,
                "taskStats": taskStats,
            })
        return {"tasks": tasks, "standings": standings}
