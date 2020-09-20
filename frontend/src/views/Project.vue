<template>
<div>

    <AppBar v-bind:id="id"/>

    <router-view></router-view>

    


</div>
               
</template>

<script>
    import AppBar from "@/components/AppBar";
    import { mapActions, mapGetters } from "vuex";
    export default {
        props: ["id"],
        components: {
            AppBar
        },
        methods:{
            ...mapActions("board", {
            fetchBoards: "fetchList"
            }),
            ...mapGetters("board", {
                listBoards:"list"
            }),
            fetchData() {
                this.fetchBoards({ customUrlFnArgs: this.id });
                this.listBoards;
            },
        },
        computed:{

        },
        created() {
            this.fetchData();
            
        }
    }
</script>

<style lang="css" scoped>
@import "../main.css";

</style>