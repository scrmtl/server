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
    import { mapActions } from "vuex";
    export default {
        props: ["id"],
        components: {
            AppBar
        },
        methods:{
            ...mapActions("board", {
            fetchBoards: "fetchList"
            }),
            fetchData() {
                return this.fetchBoards({ customUrlFnArgs: this.id });
            },
        },
        computed:{

        },
        created() {
            this.fetchData();
            this.$router.push("");
        }
    }
</script>

<style lang="css" scoped>
@import "../main.css";

</style>