<template>
    <div class="challenge">
        <h3 class="challenge-name"><NuxtLink :to="{name: 'event-name-id', params: {name: eventname, id: challengeid}}">{{ challenge.name }}</NuxtLink></h3>
        <div class="challenge-body">
            <div v-if="'solves' in challenge"><span style="font-size: 1.5rem;">{{ challenge.solves.length }}</span> solves</div>
            <div>difficulty:<span style="font-size: 1.5rem;"><ratecolor :rating="challenge.difficulty">{{ challenge.difficulty }}</ratecolor></span></div>
            <div class="challenge-categories"><span v-for="cat in challenge.categories">{{ cat }}</span></div>
        </div>
    </div>
</template>

<script>
export default {
    props: ['challenge', 'eventname', 'challengeid']
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
