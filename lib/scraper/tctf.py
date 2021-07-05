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

class TCTFScraper():
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
        r = self._get("/data/scoreboard.json")
        data = r.json()

        problem_id = {}
        for p in data["problems"]:
            problem_id[p["id"]] = p["title"]

        teams = []
        for t in data["teams"]:
            teams.append({
                "pos": t["rank"],
                "team": t["username"],
                "score": t["score"],
                "taskStats": {problem_id[p_id]:None for p_id in t["solved"]},
            })

        return {"standings": teams, "tasks": list(problem_id.values())}
