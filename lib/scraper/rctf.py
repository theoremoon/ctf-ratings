import requests
from urllib.parse import urljoin
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from http.cookies import SimpleCookie
from tqdm import tqdm

class RCTFScraper():
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
        retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 501, 502, 503, 504])
        s.mount("http://", HTTPAdapter(max_retries=retries))
        s.mount("https://", HTTPAdapter(max_retries=retries))
        return s.get(urljoin(self.url, path), cookies=self.cookiejar, headers={"Authorization": "Bearer {}".format(self.token)}, **kwargs)

    def _scoreboard(self):
        total = 0
        cur_rows = []
        while True:
            r = self._get("/api/v1/leaderboard/now", params={"limit": 100, "offset": len(cur_rows)})
            r.raise_for_status()
            data = r.json()["data"]
            total = data["total"]
            cur_rows.extend(data["leaderboard"])
            print("[+] {}/{}".format(len(cur_rows), total))
            if len(cur_rows) >= total:
                break
        return [{
            "pos": i+1,
            "team": row["name"],
            "score": row["score"],
            "id": row["id"],
        } for i, row in enumerate(cur_rows)]

    def _team_tasks(self, team_id: str):
        r = self._get("/api/v1/users/{}".format(team_id))
        r.raise_for_status()
        data = r.json()["data"]
        return {s["id"]:{
            "points": s["points"],
            "time": s["createdAt"],
        } for s in data["solves"]}

    def _tasks(self):
        r = self._get("/api/v1/challs")
        r.raise_for_status()
        data = r.json()["data"]
        return [d["id"] for d in data]

    def scoreboard(self):
        tasks = self._tasks()
        teams = self._scoreboard()
        for i in tqdm(range(len(teams))):
            teams[i]["taskStats"] = self._team_tasks(teams[i]["id"])

        return {"tasks": tasks, "standings": teams}
