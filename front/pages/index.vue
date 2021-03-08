<template>
        <table>
            <thead>
                <tr>
                    <th>Rank</th>
                    <th>Team</th>
                    <th>Rating</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(t, i) in teams_by_rating" :key="t.name">
                    <td style="text-align: right; padding-right: 1rem;">{{ i + 1 }}</td>
                    <td><NuxtLink :to="{name: 'team-name', params: {name: t.name}}"><ratecolor :rating="t.rating">{{ t.name }}</ratecolor></NuxtLink></td>
                    <td>{{ round(t.rating, 2) }}</td>
                </tr>
            </tbody>
        </table>
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
        ...mapGetters(['teams']),
        teams_by_rating() {
            if (!this.teams) {
                return [];
            }
            let ts = this.teams.slice();
            ts.sort((a, b) => b.rating - a.rating);
            return ts;
        },
    }
}
</script>

<style scoped>
th,td {
    min-width: 5rem;
}
table {
    width: 100%;
}
</style>
