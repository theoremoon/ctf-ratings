<template>
    <span :style="{color: rateColor(rating), fontWeight: 'bold'}"><slot /></span>
</template>

<script>
export default {
    props: ['rating'],
    methods: {
        rateColor(rating) {
            if (rating < 400) {
                return '#808080';
            }
            if (rating < 800) {
                return '#804000';
            }
            if (rating < 1200) {
                return '#008000';
            }
            if (rating < 1600) {
                return '#00c0c0';
            }
            if (rating < 2000) {
                return '#0000ff';
            }
            if (rating < 2400) {
                return '#c0c000';
            }
            if (rating < 2800) {
                return '#ff8000';
            }
            return '#ff0000';
        }
    }
}
</script>
