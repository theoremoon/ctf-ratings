import json
from lib.perf import PerfomanceCalculator
from lib.difficulty import calc_difficulty
from typing import List


def main():
    with open("./ctf.json", "r") as f:
        ctf = json.load(f)

    events = sorted(ctf["events"].values(), key=lambda x:x["date"])
    cur_data = {"teams": {}, "events": {}}
    for ev in events:
        print("[+]", "Recalculating about {}".format(ev["name"]))
        eventname= ev["name"]
        team_solves = {t["name"]:t["events"][eventname]["solves"] for t in ctf["teams"].values() if eventname in t["events"]}
        team_standings: List[str] = sorted([t for t in team_solves.keys()], key=lambda x: len(team_solves[x]), reverse=True)

        perf = PerfomanceCalculator(cur_data["teams"])
        team_perfs = perf.calc_performance(team_standings)

        team_updates = {}
        for i in range(len(team_standings)):
            t = team_standings[i]
            p = team_perfs[i]
            rating = perf.calc_new_rating(t, p)
            team_updates[t] = {
                "event": eventname,
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
                cur_data["teams"][t] = {"name": t, "events": {}, "rating": 0}
            cur_data["teams"][t]["events"][eventname] = update
            cur_data["teams"][t]["rating"] = update["rating"]

        cur_data["events"][eventname] = ev

    with open("./ctf.json", "w") as f:
        json.dump(cur_data, f, ensure_ascii=False)

if __name__ == "__main__":
    main()


