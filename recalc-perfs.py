import json
from lib.perf import PerfomanceCalculator
from lib.difficulty import calc_difficulty
from typing import List


def main():
    with open("./ctf.json", "r") as f:
        ctf = json.load(f)

    events = sorted(ctf["events"], key=lambda x:x["date"])
    cur_data = {"teams": {}, "events": []}
    for ev in events:
        print("[+]", "Recalculating about {}".format(ev["name"]))
        team_solves = [(t, e["solves"]) for t, es in ctf["teams"].items() for e in es if e["event"] == ev["name"]]
        team_standings: List[str] = [t[0] for t in sorted(team_solves, key=lambda x: len(x[1]), reverse=True)]
        team_solves = {t[0]:t[1] for t in team_solves}

        perf = PerfomanceCalculator(cur_data["teams"])
        team_perfs = perf.calc_performance(team_standings)

        team_updates = {}
        for i in range(len(team_standings)):
            t = team_standings[i]
            p = team_perfs[i]
            rating = perf.calc_new_rating(t, p)
            team_updates[t] = {
                "event": ev["name"],
                "performance": p,
                "rating": rating,
                "solves": team_solves[t],
                "rank": i+1,
            }

        for c_id in ev["challenges"].keys():
            diff = calc_difficulty(c_id, [t for t in team_updates.values()])
            ev["challenges"][c_id]["difficulty"] = diff

        for t, update in team_updates.items():
            if t not in cur_data["teams"]:
                cur_data["teams"][t] = []
            cur_data["teams"][t].append(update)

        cur_data["events"].append(ev)

    with open("./ctf.json", "w") as f:
        json.dump(cur_data, f, ensure_ascii=False)

if __name__ == "__main__":
    main()


