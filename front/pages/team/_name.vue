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
            </tr>
        </thead>
        <tbody>
            <tr v-for="ev in history">
                <td><date :date="eventMap[ev.event].date" /></td>
                <td><NuxtLink :to="{name: 'team-name-ctf', params:{ name: teamname, ctf: ev.event} }">{{ ev.event }}</NuxtLink></td>
                <td>{{ ev.rank }}</td>
                <td><ratecolor :rating="ev.performance">{{ ev.performance }}</ratecolor></td>
                <td><ratecolor :rating="ev.rating">{{ round(ev.rating, 2) }}</ratecolor></td>
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
        ...mapGetters(['teams', 'eventMap']),
        team() {
            return this.teams[this.teamname]
        },
        teamname() {
            return this.$route.params.name;
        },
        history() {
            const history = this.team.slice();
            history.sort((a, b) => this.eventMap[b.event].date - this.eventMap[a.event].date);

            return history;
        },
        rating() {
            return this.history[0].rating
        }
    }
}
</script>
