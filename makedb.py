import json
from lib.perf import calc_performance, calc_new_rating, calc_new_ahc_rating
from lib.difficulty import calc_difficulty
from lib.types import Team, History, Event
from pathlib import Path

def jsonEncoder(x):
    try:
        return x.toJSON()
    except:
        return x.__dict__

ts = []
for p in Path("./data/teams/").glob("*.json"):
    with open(p) as f:
        ts.append( json.load(f) )

team_index = {}
for i, t in enumerate(ts):
    for name in [t["name"]] + t["aliases"]:
        if name in team_index:
            raise ValueError("name [{}] is duplicated".format(name))
        team_index[name] = i
teams = [Team(t["name"], t["country"])  for t in ts]


es = []
for p in Path("./data/events/").glob("*.json"):
    with open(p) as f:
        es.append( json.load(f) )
es = sorted(es, key=lambda e: e["date"])

events = []
for e in es:
    print("[+]", "calculating about {}".format(e["name"]))

    e["standings"] = sorted(e["standings"], key=lambda t: t["pos"])  # sort teams by pos

    # get past performances of teams
    team_perfs = []
    indices = []
    for t in e["standings"]:
        if t["team"] not in team_index:
            teams.append(Team(t["team"], ""))
            team_index[ t["team"] ] = len(teams) - 1

        index = team_index[ t["team"] ]
        team_perfs.append(teams[index].past_perfs())

    # calc performance
    perfs = calc_performance(team_perfs)

    # calc rating and save
    for i in range(len(perfs)):
        t = e["standings"][i]
        index = team_index[ t["team"] ]
        rating = calc_new_rating(team_perfs[i], perfs[i])
        ahc_rating = calc_new_ahc_rating(team_perfs[i], perfs[i])
        teams[index].history.append(History(
            e["name"],
            i+1,
            perfs[i],
            rating,
            list(t["taskStats"].keys()),
            ahc_rating,
        ))

    # calc challenge difficulties
    tasks = []
    for task in e["tasks"]:
        solve_teams = [e["standings"][i]["team"] for i in range(len(e["standings"])) if task in e["standings"][i]["taskStats"]]
        solve_team_perfs = [teams[team_index[t]].aperf() for t in solve_teams]
        unsolve_team_perfs = [e["standings"][i]["team"] for i in range(len(e["standings"])) if task not in e["standings"][i]["taskStats"]]
        unsolve_team_perfs = [teams[team_index[t]].aperf() for t in unsolve_team_perfs]

        diff = calc_difficulty(solve_team_perfs, unsolve_team_perfs)
        tasks.append({"name": task, "difficulty": diff})

    # save event
    events.append(Event(e["name"], e["date"], {t["name"]:t["difficulty"] for t in tasks}))

teams = sorted(teams, key=lambda x: x.history[-1].new_rating, reverse=True)
with open("ctf.json", "w") as f:
    json.dump({
        "teams": teams,
        "events": events,
    }, f, default=jsonEncoder, ensure_ascii=False)

