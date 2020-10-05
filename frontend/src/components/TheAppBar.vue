/* eslint-disable */
<template>
  <v-app-bar color="navbar" dense flat app  absolute >
    <v-tabs background-color="transparent" slider-color="link"
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
        { id: 1, name: "Dashboard", route: `/project/${this.id}` },
        { id: 2, name: "Product Backlog", route: `/project/${this.id}/ProductBacklog` },
        { id: 3, name: "Sprint Planing", route: `/project/${this.id}/SprintPlaning` },
        { id: 4, name: "Sprint Backlog", route: `/project/${this.id}/SprintBacklog` },
        { id: 5, name: "Archive", route: `/project/${this.id}/Archive` },
        { id: 6, name: "Statistic", route: `/project/${this.id}/Statistic`},
        
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
