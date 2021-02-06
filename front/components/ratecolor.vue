<template>
    <span :style="{color: rateColor(rating)}"><slot /></span>
</template>

<script>
export default {
    props: ['rating'],
    methods: {
        rateColor(rating) {
            if (rating < 400) {
                return 'gray';
            }
            if (rating < 800) {
                return 'brown';
            }
            if (rating < 1200) {
                return 'green';
            }
            if (rating < 1600) {
                return 'skyblue';
            }
            if (rating < 2000) {
                return 'blue';
            }
            if (rating < 2300) {
                return 'yellow';
            }
            if (rating < 2800) {
                return 'orange';
            }
            return 'red';
        }
    }
}
</script>
