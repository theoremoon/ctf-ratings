from typing import List, Dict
from lib.perf import avg_perf

class History():
    def __init__(self, event: str, rank: int, perf: float, new_rating: float, tasks: List[str], ahc_rating: float):
        self.event = event
        self.rank = rank
        self.perf = perf
        self.new_rating = new_rating
        self.tasks = tasks
        self.ahc_rating = ahc_rating

    def toJSON(self)->Dict:
        return {"event": self.event, "rank": self.rank, "perf": self.perf, "rating": self.new_rating, "tasks": self.tasks, "ahc_rating": self.ahc_rating}


class Team():
    def __init__(self, name: str, country: str):
        self.name = name
        self.country = country
        self.history: List[History] = []

    def past_perfs(self)->List[float]:
        return [h.perf for h in self.history]

    def aperf(self)->float:
        return avg_perf(self.past_perfs())

    def toJSON(self)->Dict:
        return {
            "name": self.name,
            "country": self.country,
            "history": [h.toJSON() for h in self.history],
            "rating": self.history[-1].new_rating
        }

class Event():
    def __init__(self, name: str, date: int, tasks: Dict[str,float]):
        self.name = name
        self.date = date
        self.tasks = tasks

    def toJSON(self)->Dict:
        return self.__dict__


