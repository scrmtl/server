<template>
    <v-content class="tabbody tab-content">
    <v-app-bar>
      <AppBar v-bind:id="id"/>
    </v-app-bar>
    <router-view></router-view>
    
  </v-content>
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