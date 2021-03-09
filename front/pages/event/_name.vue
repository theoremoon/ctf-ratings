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
                    <tr v-for="(t, i) in playedTeams" :key="t.name">
                        <td style="text-align: right; padding-right: 1rem;">{{ i + 1 }}</td>
                        <td style="max-width: 30rem;"><NuxtLink :to="{name: 'team-name', params: {name: t.name}}"><ratecolor :rating="t.perf">{{ t.name }}</ratecolor></NuxtLink></td>
                        <td>{{ t.perf }}</td>
                    </tr>
                </tbody>
            </table>


            <div>
                <NuxtChild />
                <div class="challenges">
                    <challengepanel :challenge="c.name" :eventname="eventname" v-for="c in challenges" :key="c.name"/>
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
        ...mapGetters(['teams', 'events']),
        eventname() {
            return this.$route.params.name;
        },
        event() {
            return this.events.filter(e => e.name === this.eventname)[0];
        },
        playedTeams() {
            const ts = this.teams.
                filter(t => t.history.filter(e => e.event === this.eventname).length > 0).
                map(t => ({name: t.name, ...( t.history.filter(e => e.event === this.eventname)[0] )}));
            ts.sort((a, b) => b.perf - a.perf)
            return ts;
        },
        challenges() {
            const cs = Object.entries(this.event.tasks).map(([k,v]) => ({name: k, difficulty: v}))
            cs.sort((a, b) => b.difficulty - a.difficulty);
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
</style>
