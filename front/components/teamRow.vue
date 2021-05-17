<template>
    <div class="row">
        <div class="team-pos">{{ source.pos }}</div>
        <div class="team-rating">{{ round(source.rating, 2) }}</div>
        <div class="team-name"><NuxtLink :to="{name: 'team-name', params: {name: source.name}}"><ratecolor :rating="source.rating">{{ source.name }}</ratecolor></NuxtLink></div>
    </div>
</template>

<script>
export default {
    props: ['source'],
    methods: {
        round(x, d) {
            return Math.round(x * Math.pow(10, d)) / Math.pow(10, d);
        },
    },
}
</script>

<style scoped>

.row {
    width: 100%;
    background-color: #f9f9f9;
    border-bottom: 1px solid #ccc;
    padding: 1rem 0;

}
.team-pos {
    display: inline-block;
    width: 4rem;
    padding-right: 1rem;
    text-align: right;
}
.team-rating {
    display: inline-block;
    width: 7rem;
    padding-right: 1rem;
    text-align: right;
}
.team-name {
    display: inline-block;
}
</style>
</style>
