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

class CTFxScraper():
    def __init__(self, url, **kwargs):
        self.url = url
        cookies = SimpleCookie()
        if "cookies" in kwargs:
            cookies.load(kwargs["cookies"])

        if "session" in kwargs:
            cookies["login_tokens"] = kwargs["session"]

        self.cookiejar = requests.cookies.RequestsCookieJar()
        self.cookiejar.update(cookies)

    def _get(self, path):
        s = requests.Session()
        retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 501, 502, 503, 504])
        s.mount("http://", HTTPAdapter(max_retries=retries))
        s.mount("https://", HTTPAdapter(max_retries=retries))
        return s.get(urljoin(self.url, path), cookies=self.cookiejar)

    def _categories(self):
        logger.warning("getting categories...")
        r = self._get("/challenges")
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        categories = soup.select("#categories-menu a")
        logger.warning("done")
        return [cat["href"] for cat in categories]

    def _category_task_ids(self, path):
        logger.warning("getting {}".format(path))
        r = self._get(path)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        cards = soup.select(".ctfx-card-head")
        logger.warning("done")
        return [card.find("a")["href"] for card in cards]

    def _task(self, path):
        logger.warning("getting {}".format(path))
        r = self._get(path)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        taskname = soup.select_one(".typewriter").text.strip()
        trs = soup.select(".challenge-table tbody tr")
        teams = []
        for tr in trs:
            teams.append(tr.select_one(".team-name").text)
        logger.warning("done")
        return taskname, teams

    def scoreboard(self):
        logger.warning("getting scoreboard...")
        r = self._get("/json?view=scoreboard")
        r.raise_for_status()
        standings = [t | {"taskStats": {}} for t in r.json()["standings"] if t["score"] > 0]
        logger.warning("done")

        task_ids = []
        categories = self._categories()
        for category in categories:
            task_ids.extend(self._category_task_ids(category))

        tasks = []
        for task_id in task_ids:
            taskname, teams = self._task(task_id)
            tasks.append(taskname)
            for t in teams:
                for i in range(len(standings)):
                    if standings[i]["team"] == t:
                        standings[i]["taskStats"][taskname] = None

        return {"standings": standings, "tasks": tasks}
