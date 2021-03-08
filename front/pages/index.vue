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
                <tr v-for="(t, i) in teamlist" :key="t.name">
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
    data() {
        return {teamlist: []}
    },
    created() {
        this.progressive(this.teams);
    },
    methods: {
        round(x, d) {
            return Math.round(x * Math.pow(10, d)) / Math.pow(10, d);
        },
        progressive(xs) {
            const N = 1000;
            this.teamlist.splice(0, this.teamlist.length);
            let i = 0;
            const id = setInterval(() => {
                this.teamlist.push(...xs.slice(i, i+N));
                i += N;
                if (i >= xs.length) {
                    clearInterval(id)
                }
            }, 500)
        },
    },
    computed: {
        ...mapGetters(['teams']),
    },
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
