<template>
  <v-content class="tabbody tab-content">
    <v-container fluid class="pl-10">
       <v-row>
          <div v-for="lane in laneList" :key="lane.id">
            <Lane v-bind:lane="lane"></Lane>
          </div>
      </v-row>
    </v-container>
  </v-content>
</template>

<script>
import Lane from "@/components/Lane.vue";
import { mapGetters, mapActions, mapState } from "vuex";
export default {
  data: () => ({}),
  props: ["SprintBacklogBoard"],
  components: {
    Lane
  },
  computed: {
    ...mapGetters("lane", {
      laneList: "list"
    }),

    ...mapState([
      "route" // vuex-router-sync
    ])
  },

  methods: {
    ...mapActions("lane", {
      fetchLanes: "fetchList"
    }),

    fetchData() {
      return this.fetchLanes({customUrlFnArgs: this.SprintBacklogBoard.id});
    }
  },

  watch: {
    $route: "fetchData"
  },

  created() {
    this.fetchData();
  },
  mounted: function() {
    this.fetchData();
    setInterval(
      function() {
        this.fetchData();
      }.bind(this),
      10000
    );
  }
};
</script>

<style lang="css" scoped>
@import "../main.css";
</style>