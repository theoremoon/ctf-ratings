<template>
    <ul>
        <li v-for="s in solvers">
            <NuxtLink :to="{name: 'team-name', params: {name: s}}">{{ s }}</NuxtLink>
        </li>
    </ul>
</template>

<script>
import {mapGetters} from "vuex";
export default {
    methods: {
        solves(challenge_id) {
        }
    },
    computed: {
        ...mapGetters(['solveMap']),
        eventname() {
            return this.$route.params.name;
        },
        challengeid() {
            return this.$route.params.id;
        },
        solvers() {
            if (!this.challengeid) {
                return [];
            }
            const solves = this.solveMap[this.eventname][this.challengeid];
            if (!solves) {
                return [];
            }
            return solves;
        }
    }
}
</script>

