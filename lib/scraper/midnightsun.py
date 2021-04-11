import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from logging import getLogger, StreamHandler, Formatter
from http.cookies import SimpleCookie

logger = getLogger(__name__)
handler = StreamHandler()
handler.setFormatter(Formatter('%(asctime)-15s %(message)s'))
logger.addHandler(handler)

class MidnightsunScraper():
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
        logger.warning("getting scoreboard...")
        r = self._get("/dashboard/scoreboard")
        r.raise_for_status()
        logger.warning("done")

        tasks = []
        soup = BeautifulSoup(r.text, "html.parser")
        heads = soup.select("table.ctf-scoreboard thead th")
        for head in heads[4:]:
            tasks.append(head.text.strip())

        standings = []
        solves = soup.select("table.ctf-scoreboard tbody tr")
        for solve in solves:
            datas = solve.select("td")
            pos = int(datas[0].text.strip())
            team = datas[1].text.strip()
            score = int(datas[2].text.strip())
            taskStats = {}

            for i, taskStat in enumerate(datas[4:]):
                if taskStat.text.strip() != "":
                    taskStats[tasks[i]] = None
            standings.append({
                "pos": pos,
                "team": team,
                "score": score,
                "taskStats": taskStats,
            })

        return {"standings": standings, "tasks": tasks}
