<template>
    <div class="challenge">
        <h3 class="challenge-name">{{ challenge }}</h3>
        <div class="challenge-body">
            <div><span style="font-size: 1.5rem;">{{ solveCount }}</span> solves</div>
            <div>difficulty:<span style="font-size: 1.5rem;"><ratecolor :rating="difficulty">{{ difficulty }}</ratecolor></span></div>
        </div>
    </div>
</template>

<script>
import {mapGetters} from "vuex";
export default {
    props: ['challenge', 'eventname'],
    computed: {
        ...mapGetters(['teams', 'events']),
        solveCount() {
            return this.teams.flatMap(t => t.history.filter(e => e.event === this.eventname)).filter(e => e.tasks.includes(this.challenge)).length;
        },
        difficulty() {
            return this.events.filter(e => e.name === this.eventname)[0].tasks[this.challenge];
        }
    }

}
</script>

<style scoped>

.challenge {
    max-width: 15rem;
    min-width: 10rem;
    background-color: #eeeeee;
    margin: 1rem;
    border-radius: 5px;
}
.challenge-name {
    border-radius: 5px 5px 0 0;
    margin: 0;
    padding: 0.25rem 0.5rem;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
    background-color: #dddddd;
}
.challenge-body {
    padding: 0.25rem;
    min-height: 5rem;
}
.challenge-categories {
}
.challenge-categories>span {
    display: inline-block;
    background-color: #aaaaaa;
    border-radius: 2px;
    margin: 0.25rem;
    padding: 0 0.25rem;
}
</style>
