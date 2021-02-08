<template>
  <v-card
    class="lane"
    max-width="420"
    elevation="5"
    height="100vh-50"
    overflow-y="auto"
  >
    <v-card-title class="navbar white--text"> My Tasks </v-card-title>
    <v-card-text class="lane-body flex-column" v-if="allFetched">
      <v-row justify="center" v-for="task in listTasks" :key="task.id">
        <Task v-bind:task="task" v-bind:task_index="task.id" />
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
import Task from "@/components/Task.vue";
//import for CRUD operations
import { mapGetters, mapActions, mapState } from "vuex";
export default {
  data: () => ({
    allFetched: false,
  }),
  components: {
    Task,
  },
  computed: {
    ...mapGetters("task", {
      listTasks: "list",
    }),
    ...mapGetters(["getUserinfo"]),

    ...mapState([
      "route", // vuex-router-sync
    ]),
  },

  methods: {
    ...mapActions("task", {
      fetchTasks: "fetchList",
    }),
    ...mapActions("label", {
      fetchLabels: "fetchList",
    }),

    fetchData() {
      this.fetchTasks({
        customUrlFnArgs: { byUser: this.getUserinfo.userId },
      }).then((resp) => {
        if (resp.status === 200) {
          this.fetchLabels({
            customUrlFnArgs: {},
          }).then((resp) => {
            this.allFetched = true;
            return resp;
          });
        }
        return resp;
      });
    },
  },

  watch: {
    $route: "fetchData",
    listTasks(val, prev) {
      if (val.id === prev.id) return;
      this.fetchData();
    },
  },

  created() {
    this.fetchData();
  },
  mounted() {
    this.fetchData();
  },
};
</script>

<style lang="css">
@import "../../main.css";
</style>
