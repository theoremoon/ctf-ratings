<template>
    <div style="height: 100%;">
        <div class="filterbox">
            <input type="text" v-model="filter" placeholder="filter">
        </div>
        <div class="row head" style="height: 3rem;">
            <div class="team-pos">Rank</div>
            <div class="team-rating">Rating</div>
            <div class="team-name">Team</div>
        </div>
        <virtual-list 
            class="scroller"
            data-key="name"
            :data-sources="filteredTeams"
            :data-component="teamRow"
            >
        </virtual-list>
    </div>
</template>

<script>
import {mapGetters} from "vuex";
import teamRow from "@/components/teamRow.vue";
export default {
    data() {
        return {
            teamRow: teamRow,
            filter: '',
        }
    },
    methods: {
        round(x, d) {
            return Math.round(x * Math.pow(10, d)) / Math.pow(10, d);
        },
    },
    computed: {
        ...mapGetters(['teams']),
        teamWithPos() {
            return this.teams.map((x, i) => ({
                ...x,
                pos: i+1,
            }));
        },
        filteredTeams() {
            if (this.filter) {
                return this.teamWithPos.filter(x => x.name.includes(this.filter));
            } else {
                return this.teamWithPos;
            }
        }
    },
}
</script>

<style scoped>
.scroller {
    height: calc(100% - 2rem - 3rem);
    overflow-y: scroll;
}

.filterbox {
}
.filterbox input[type=text]{
    text-align: center;
    display: inline-block;
    width: 100%;
    font-size: 1.5rem;
    border: none;
    border-bottom: 1px solid #f0f0f0;
}

.row {
    width: 100%;
    background-color: #f9f9f9;
    border-bottom: 1px solid #ccc;
    padding: 1rem 0;

}
.head {
    background-color: #f0f0f0;
    font-weight: bold;
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
