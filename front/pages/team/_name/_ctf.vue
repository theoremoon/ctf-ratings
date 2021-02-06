<template>
    <div class="challenges">
        <div v-for="(c, c_id) in challenges" :key="c.name">
            <h3 class="challenge-name"><NuxtLink :to="{name: 'event-name-id', params: {name: eventname, id: c_id}}">{{ c.name }}</NuxtLink></h3>
            <div class="challenge-body">
            </div>
        </div>
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
