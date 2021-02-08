import requests
import time
from urllib.parse import urljoin
from lib.scraper import IScraper

class JustCTFScraper(IScraper):
    def __init__(self, url, **kwargs):
        self.url = url

    def _scoreboard(self):
        r = requests.get(urljoin(self.url, "/api/v1/scoreboard"))
        r.raise_for_status()
        data = r.json()
        return data

    def _task(self):
        r = requests.get(urljoin(self.url, "/api/v1/tasks"))
        r.raise_for_status()
        data = r.json()
        return data

    def teams_chals(self):
        scoreboard = self._scoreboard()
        team_standings = [t["team"]["name"] for t in scoreboard]
        team_ids = {t["team"]["name"]:[str(task["id"]) for task in t["team"]["task_solved"]] for t in scoreboard}
        challenges = {str(task["id"]):{"name":task["name"], "categories":task["categories"]} for task in self._task()}

        return team_standings, team_ids, challenges

