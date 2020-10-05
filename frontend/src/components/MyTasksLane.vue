<template>
  <v-card 
  class="lane" 
  max-width="420" 
  elevation="5"
  max-height="100vh"
  >
    <v-card-title class="navbar white--text">
      My Tasks
    </v-card-title>
    <v-card-text
    class="lane-body scroll" 
    v-if="allFetched" 
    max-height="200"
    >
      <v-row v-for="task in listTasks" :key="task.id">
        <v-col>
          <Task v-bind:task="task" v-bind:task_index="task.id" />
        </v-col>
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
    allFetched: false
  }),
  components: {
    Task
  },
  computed: {
    ...mapGetters("task", {
      listTasks: "list"
    }),
    ...mapGetters("session", {
      listSession: "list"
    }),

    ...mapState([
      "route" // vuex-router-sync
    ])
  },

  methods: {
    ...mapActions("task", {
      fetchTasks: "fetchList"
    }),
    ...mapActions("label", {
      fetchLabels: "fetchList"
    }),
    ...mapActions("session", {
      fetchSession: "fetchList"
    }),

    fetchData() {
      this.fetchSession({ customUrlFnArgs: { all: false } }).then(resp => {
        if (resp.status === 200) {
          this.fetchTasks({
            customUrlFnArgs: { byUser: this.listSession.shift().id }
          }).then(resp => {
            if (resp.status === 200) {
              this.fetchLabels({
                customUrlFnArgs: {}
              }).then(resp => {
                this.allFetched = true;
                return resp;
              });
            }
            return resp;
          });
        }
        return resp;
      });
    }
  },

  watch: {
    $route: "fetchData",
    listTasks(val, prev) {
      if (val.id === prev.id) return;
      console.log("watch listTasks Getter: " + val + prev);
      this.fetchData();
    }
  },

  created() {
    this.fetchData();
  },
  mounted() {
    this.fetchData();
  }
};
</script>

<style lang="css" >
@import "../main.css";
</style>