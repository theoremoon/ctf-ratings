<template>
<table>
<thead>
    <tr>
        <th>Event</th>
        <th>Date</th>
    </tr>
</thead>
<tbody>
    <tr v-for="e in events_by_date">
        <td><NuxtLink :to="{name: 'event-name', params: {name: e.name}}">{{ e.name }}</NuxtLink></td>
        <td><date :date="e.date" /></td>
    </tr>
</tbody>
</table>
</template>

<script>
import {mapGetters} from "vuex";
export default {
    computed: {
        ...mapGetters(['teams', 'events']),
        events_by_date() {
            if (!this.events) {
                return [];
            }
            let es = this.events.slice();
            es.sort((a, b) => b.date - a.date);
            return es;
        },
    }
}
</script>

<style></style>
