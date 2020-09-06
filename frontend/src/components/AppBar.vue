/* eslint-disable */
<template>
  <v-app-bar color="navbar" dark absolute class="appBar">
    <v-tabs class="tabs" background-color="transparent" slider-color="link"
    dark centered grow v-model="activeTab">
      <v-tab v-for="tab in tabs" :key="tab.id" :to="tab.route" exact>{{ tab.name }}</v-tab>     
    </v-tabs>
  </v-app-bar>
</template>

<script>

export default {
  props: ["id"],
  data() {
    return {
      activeTab: `/project/${this.id}`,
      tabs: [
        { id: 1, name: "Product Backlog", route: `/project/${this.id}/ProductBacklog` },
        { id: 2, name: "Sprint Planing", route: `/project/${this.id}/SprintPlaning` },
        { id: 3, name: "Sprint Backlog", route: `/project/${this.id}/SprintBacklog` },
        { id: 4, name: "Archive", route: `/project/${this.id}/Archive` },
        { id: 5, name: "Statistic", route: `/project/${this.id}/Statistic`},
        
      ]
    };
  },
  components: {

  },
  methods: {
       
  },
  computed:{

  }
};

</script>

<style lang="css" scoped>
@import "../main.css";

</style>
