import data from "../../ctf.json";


export const state = () => {
    const events = data["events"];
    const teams = data["teams"];
    let eventMap = {};
    let teamList = [];
    let solveMap = {};

    for (const e of events) {
        eventMap[e.name] = e;
    }

    for (const team of Object.keys(teams)) {
        const history = teams[team].slice();
        history.sort((a, b) => eventMap[b["event"]].date -  eventMap[a["event"]].date);
        teamList.push({
            "name": team,
            "history": history,
            "rating": history[0]["rating"],
        });
    }

    for (const t of teamList) {
        for (const h of t.history) {
            const ev = h["event"];
            if (!solveMap.hasOwnProperty(ev)) {
                solveMap[ev] = {};
            }
            for (const s of h["solves"]) {
                if (!solveMap[ev].hasOwnProperty(s)) {
                    solveMap[ev][s] = [];
                }
                solveMap[ev][s].push(t.name);
            }
        }
    }

    return {
        events, teams, eventMap, teamList, solveMap
    };
}

export const getters = {
    events(state) { return state.events },
    teams(state) { return state.teams },
    eventMap(state) { return state.eventMap },
    teamList(state) { return state.teamList },
    solveMap(state) { return state.solveMap },
}
