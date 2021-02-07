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
</style>
