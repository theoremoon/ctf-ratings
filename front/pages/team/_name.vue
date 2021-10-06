<template>
    <div>
        <h1><ratecolor :rating="rating">{{ teamname }}</ratecolor></h1>
        <table>
        <thead>
            <tr>
            <th></th>
                <th>Event</th>
                <th>Rank</th>
                <th>Performance</th>
                <th>Rating</th>
                <th>AHC Rating <fa icon="question-circle" title="AHC Rating is based on rating system of AtCoder Heuristic Contest" /></th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="ev in history">
                <td><date :date="events.filter(e => e.name === ev.event)[0].date" /></td>
                <td>
                    <NuxtLink :to="{name: 'event-name', params: {name: ev.event}}">{{ ev.event }}</NuxtLink>
                    <span style="font-size: 0.9em">
                        <NuxtLink :to="{name: 'team-name-ctf', params:{ name: teamname, ctf: ev.event} }">tasks</NuxtLink>
                    </span>
                </td>
                <td>{{ ev.rank }}</td>
                <td><ratecolor :rating="ev.perf">{{ ev.perf }}</ratecolor></td>
                <td><ratecolor :rating="ev.rating">{{ round(ev.rating, 2) }}</ratecolor></td>
                <td><ratecolor :rating="ev.ahc_rating">{{ round(ev.ahc_rating, 2) }}</ratecolor></td>
            </tr>
        </tbody>
        </table>

        <nuxt-child />

    </div>

</template>

<script>
import {mapGetters} from "vuex";
export default {
    methods: {
        round(x, d) {
            return Math.round(x * Math.pow(10, d)) / Math.pow(10, d);
        }
    },
    computed: {
        ...mapGetters(['teams', 'events']),
        team() {
            return this.teams.filter(t => t.name === this.teamname)[0];
        },
        teamname() {
            return this.$route.params.name;
        },
        history() {
            let h = this.team.history.slice();
            h.reverse()
            return h;
        },
        rating() {
            return this.history[0].rating
        }
    }
}
</script>
