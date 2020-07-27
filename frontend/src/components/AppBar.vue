<template>
  <v-app-bar color="navbar" dark absolute class="appBar">
    <v-tabs
    background-color="transparent"
    dark
    grow
    >
    <v-tab to="Home">
      Home
    </v-tab>
    <v-tab to="ProductBacklog">
      Product Backlog
    </v-tab>
    <v-tab to="SprintPlaning">
      Sprint Planing
    </v-tab>
    <v-tab to="SprintBacklog">
      Sprint Backlog
    </v-tab>
    <v-tab to="Statistic">
      Statistic
    </v-tab>
    <v-tab to="Archive">
      Archive
    </v-tab>
  </v-tabs>
  </v-app-bar>
</template>

<script>
//import Home from "@/views/Home.vue"
//import ProductBacklog from "@views/ProductBacklog.vue"

export default {
  components: {

  },
  methods: {    
  }
};
</script>

<style lang="css" scoped>
@import "../main.css";

</style>
