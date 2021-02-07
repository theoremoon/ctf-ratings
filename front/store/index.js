import data from "../../ctf.json";


export const state = () => {
    const events = data["events"];
    const teams = data["teams"];

    let solveMap = {};
    for (const t of Object.values(teams)) {
        for (const ev of Object.values(t.events)) {
            if (!solveMap.hasOwnProperty(ev.event)) {
                solveMap[ev.event] = {};
            }
            for (const s of ev.solves) {
                if (!solveMap[ev.event].hasOwnProperty(s)) {
                    solveMap[ev.event][s] = [];
                }
                solveMap[ev.event][s].push(t.name);
            }
        }
    }

    return {
        events, teams, solveMap
    };
}

export const getters = {
    events(state) { return state.events },
    teams(state) { return state.teams },
    solveMap(state) { return state.solveMap },
}
