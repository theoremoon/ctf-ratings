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

class The3000CTFScraper():
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
        return [task.text.strip() for task in soup.select(".list-group-item-text")]


    def scoreboard(self):
        tasks = self._tasks()
        r = self._get("/rankingpp")
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        trs = soup.select("table tbody tr")

        teams = []
        for tr in trs:
            tds = tr.find_all("td")
            teams.append({
                "pos": int(tds[0].text.strip()),
                "team": tds[2].text.strip(),
                "score": int(tds[3].text.strip()),
                "taskStats": {task["title"]:None for task in tr.select("i.las")},
            })

        return {"standings": teams, "tasks": tasks}
