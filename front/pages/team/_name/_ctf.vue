<template>
    <div class="challenges">
        <challengepanel :challengeid="c_id" :challenge="c" :eventname="eventname" v-for="(c, c_id) in challenges" :key="c_id" />
    </div>
</template>

<script>
import {mapGetters} from "vuex";
export default {
    computed: {
        ...mapGetters(['teams', 'eventMap']),
        eventname() {
            return this.$route.params.ctf;
        },
        challenges() {
            if (!this.eventname) {
                return [];
            }
            return this.eventMap[this.eventname].challenges;
        },
    }
}
</script>
