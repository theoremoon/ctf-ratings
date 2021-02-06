<template>
    <div>
        <h1>{{ eventname }}</h1>
        <div class="flex">
            <table>
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Team</th>
                        <th>Performance</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(t, i) in teams" :key="t.name">
                        <td style="text-align: right; padding-right: 1rem;">{{ i + 1 }}</td>
                        <td><NuxtLink :to="{name: 'team-name', params: {name: t.name}}"><ratecolor :rating="t.performance">{{ t.name }}</ratecolor></NuxtLink></td>
                        <td>{{ t.performance }}</td>
                    </tr>
                </tbody>
            </table>


            <div>
                <NuxtChild />
                <div class="challenges">
                    <div v-for="c in challenges">
                        <h3 class="challenge-name"><NuxtLink :to="{name: 'event-name-id', params: {name: eventname, id: c.id}}">{{ c.name }}</NuxtLink></h3>
                        <div class="challenge-body">
                            <div><span style="font-size: 1.5rem;">{{ c.solves.length }}</span> solves</div>
                            <div class="challenge-categories"><span v-for="cat in c.categories">{{ cat }}</span></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>


</template>

<script>
import {mapGetters} from "vuex";
export default {
    methods: {
        solves(challenge_id) {
            const solves = this.solveMap[this.eventname][challenge_id];
            if (!solves) {
                return [];
            }
            return solves;
        }
    },
    computed: {
        ...mapGetters(['teamList', 'eventMap', 'solveMap']),
        eventname() {
            return this.$route.params.name;
        },
        event() {
            return this.eventMap[this.eventname];
        },
        teams() {
            const ts = this.teamList.flatMap(t => (
                t.history.filter(h => h.event == this.eventname).map(e => ({
                    ...e,
                    name: t.name,
                }))
            ))
            ts.sort((a, b) => b.performance - a.performance)
            return ts;
        },
        challenges() {
            const cs = Object.entries(this.event.challenges).map(c => ({
                ...c[1],
                id: c[0],
                solves: this.solves(c[0]),
            }))
            cs.sort((a, b) => a.solves.length - b.solves.length);
            return cs;
        }
    }
}
</script>

<style>
.challenges {
    display: flex;
    flex-wrap: wrap;
}
.challenges>div {
    max-width: 15rem;
    min-width: 10rem;
    background-color: #eeeeee;
    margin: 1rem;
    border-radius: 5px;
}
.challenge-name {
    border-radius: 5px 5px 0 0;
    margin: 0;
    padding: 0.25rem 0.5rem;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    background-color: #dddddd;
}
.challenge-body {
    padding: 0.25rem;
    height: 5rem;
    position: relative;
}
.challenge-categories {
    position: absolute;
    bottom: 0;
}
.challenge-categories>span {
    display: inline-block;
    background-color: #aaaaaa;
    border-radius: 2px;
    margin: 0.25rem;
    padding: 0 0.25rem;
}

</style>
