<template>
  <div>
    <v-card class="lane" min-width="344" elevation="5" max-width="auto">
      <div class="lane-header">
        <p dark>Meine Tasks</p>
      </div>
      <v-card-text class="lane-body pa-2">
        <div v-for="task in taskList" :key="task.id">
          <Task v-bind:task="task" 
          v-bind:task_index="task.id"/>
        </div>
      </v-card-text>
      <v-card-actions class="lane-extended"></v-card-actions>
    </v-card>
  </div>
</template>

<script>
import Task from "@/components/Task.vue";
//import for CRUD operations
import { mapGetters, mapActions, mapState } from "vuex";

export default {
  data: () => ({}),
  components: {
    Task
  },
  computed: {
    ...mapGetters("task", {
      taskList: "list"
    }),

    ...mapState([
      "route" // vuex-router-sync
    ])
  },

  methods: {
    ...mapActions("task", {
      fetchTasks: "fetchList"
    }),

    fetchData() {
      return this.fetchTasks();
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