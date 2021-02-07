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
                        <td><NuxtLink :to="{name: 'team-name', params: {name: t.name}}"><ratecolor :rating="t.performance">{{ t.name }}</ratecolor></NuxtLink></td>
                        <td>{{ t.performance }}</td>
                    </tr>
                </tbody>
            </table>


            <div>
                <NuxtChild />
                <div class="challenges">
                    <challengepanel :challenge="c" :challengeid="c.id" :eventname="eventname" v-for="c in challenges" :key="c.id"/>
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
        ...mapGetters(['teams', 'events', 'solveMap']),
        eventname() {
            return this.$route.params.name;
        },
        event() {
            return this.events[this.eventname];
        },
        playedTeams() {
            const ts = Object.values(this.teams).filter(t=> t.events.hasOwnProperty(this.eventname)).map(t => ({name: t.name, ...t.events[this.eventname]}));
            ts.sort((a, b) => b.performance - a.performance)
            return ts;
        },
        challenges() {
            const cs = Object.entries(this.event.challenges).map(c => ({...c[1], solves: this.solves(c[0]), id: c[0]}));
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
