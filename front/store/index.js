import data from "../../ctf.json";


export const state = () => {
    const events = data["events"];
    const teams = data["teams"];

    return {
        events, teams
    };
}

export const getters = {
    events(state) { return state.events },
    teams(state) { return state.teams },
}
