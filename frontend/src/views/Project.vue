<template>
<v-container fluid class="tabbody">
    <v-row>
        <AppBar v-bind:id="id"/>
    </v-row>
    <v-row>
        <router-view></router-view>
    </v-row>
    
  </v-container>


    

               
</template>

<script>
    import AppBar from "@/components/TheAppBar";
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