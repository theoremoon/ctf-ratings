<template>
    <span>{{ datestr }}</span>
</template>

<script>
export default {
    props: ['date'],
    computed: {
        datestr() {
            const d = new Date(this.date * 1000);
            const y = d.getFullYear();
            const m = ('0' + (d.getMonth() + 1)).slice(-2);
            const dt = ('0' + d.getDate()).slice(-2);
            return y+"-"+m+"-"+dt;
        }
    }
}
</script>
