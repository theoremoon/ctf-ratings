<template>
    <div class="challenges">
        <challengepanel :challenge="c" :eventname="eventname" v-for="c in challenges" :key="c" />
    </div>
</template>

<script>
import {mapGetters} from "vuex";
export default {
    computed: {
        ...mapGetters(['teams', 'events']),
        eventname() {
            return this.$route.params.ctf;
        },
        teamname() {
            return this.$route.params.name;
        },
        team() {
            return this.teams.filter(t => t.name === this.teamname)[0];
        },
        challenges() {
            if (!this.eventname) {
                return [];
            }

            return this.team.history.filter(e => e.event === this.eventname)[0].tasks;
        },
    }
}
</script>

<style>
.challenges {
    display: flex;
}
</style>
