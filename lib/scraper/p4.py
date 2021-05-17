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

class p4CTFScraper():
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

        tasks = [task.text.strip() for task in soup.select(".header-task")]
        trs = soup.select("table tbody tr")

        teams = []
        for tr in trs:
            teams.append({
                "pos": int(tr.select_one(".column-index").text.strip().rstrip(".")),
                "team": tr.select_one(".column-nick").select("span")[1].text.strip(),
                "score": int(tr.select_one(".column-total").text.strip()),
                "taskStats": {task["data-task"]:{
                    "time": int(task["data-solved_at"]),
                }for task in tr.select(".column-solve")},
            })

        return {"standings": teams, "tasks": tasks}
