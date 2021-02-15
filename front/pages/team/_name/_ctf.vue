<template>
    <div class="challenges">
        <challengepanel :challengeid="c_id" :challenge="c" :eventname="eventname" v-for="(c, c_id) in challenges" :key="c_id" />
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
        challenges() {
            if (!this.eventname) {
                return [];
            }

            return Object.fromEntries(this.teams[this.teamname].events[this.eventname].solves.map(cid => [cid, this.events[this.eventname].challenges[cid]]));
        },
    }
}
</script>
