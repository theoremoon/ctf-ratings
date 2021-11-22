import requests
from urllib.parse import urljoin
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from http.cookies import SimpleCookie

class N1CTFScraper():
    def __init__(self, url, **kwargs):
        self.url = url

        cookies = SimpleCookie()
        if "cookies" in kwargs and kwargs["cookies"]:
            cookies.load(kwargs["cookies"])

        self.cookiejar = requests.cookies.RequestsCookieJar()
        self.cookiejar.update(cookies)
        self.token = kwargs["token"]  # type: str

    def _get(self, path, **kwargs):
        s = requests.Session()
        s.verify = False
        retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 501, 502, 503, 504])
        s.mount("http://", HTTPAdapter(max_retries=retries))
        s.mount("https://", HTTPAdapter(max_retries=retries))
        return s.get(urljoin(self.url, path), cookies=self.cookiejar, headers={"Authorization": "Bearer {}".format(self.token)}, **kwargs)

    def _scoreboard(self):
        page = 1
        teams = []
        while True:
            r = self._get("/api/scoreboard", params={"page": page})
            r.raise_for_status()
            data = r.json()
            challs = {chall["id"]:chall["title"] for chall in data["challs"] }
            for _, team in data["teams"].items():
                teams.append({
                    "team": team["name"],
                    "pos": team["rank"],
                    "score": team["totalScore"],
                    "id": team["id"],
                    "taskStats": {challs[cid]:None for cid in team["solveds"] }
                })
            total = data["total"]
            print("[+] {}/{}".format(len(teams), total))
            if len(teams) >= total:
                break

            page += 1
        return teams

    def _tasks(self):
        r = self._get("/api/challenges")
        r.raise_for_status()
        data = r.json()
        return data["challs"] # {id: x, title: "y", class: "z"}

    def scoreboard(self):
        tasks = self._tasks()
        teams = self._scoreboard()
        taskinfo = {
            task["title"]:{
                "category": task["class"],
                "tags": [],
            }
            for task in tasks
        }

        return {"tasks": [t["title"] for t in tasks], "standings": teams, "taskinfo": taskinfo}
