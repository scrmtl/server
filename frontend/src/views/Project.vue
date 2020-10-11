<template>
<v-container fluid class="tabbody">

    <v-row class="d-flex" dense>
        <v-col cols="12">
            <router-view></router-view>
        </v-col>
    </v-row>
    
  </v-container>


    

               
</template>

<script>

    import { mapActions, mapGetters } from "vuex";
    export default {
        props: ["id"],
        components: {
            
        },
        methods:{
            ...mapActions("board", {
            fetchBoards: "fetchList"
            }),
            ...mapActions("lane", {
            fetchLanes: "fetchList"
            }),
            ...mapActions("task", {
            fetchTasks: "fetchList"
            }),
            ...mapGetters("board", {
                listBoards:"list"
            }),
            fetchData() {
                this.fetchBoards({ customUrlFnArgs: this.id });
                this.fetchLanes({ customUrlFnArgs: this.id });
                this.fetchTasks({customUrlFnArgs: { projectId: this.id } })
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