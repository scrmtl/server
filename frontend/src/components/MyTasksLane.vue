<template>

  <v-card class="lane " max-width="420"  elevation="5">
    <v-card-title class="navbar white--text" >
      My Tasks
    </v-card-title>
    <v-card-text class="lane-body"  >
        <v-row  v-for="task in listTasks" :key="task.id">
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
  data: () => ({}),
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
    ...mapActions("session", {
      fetchSession: "fetchList"
    }),

    fetchData() {
      this.fetchSession({ customUrlFnArgs: {all: false}})
        .then(resp => {
          if(resp.status === 200){
            this.fetchTasks({
              customUrlFnArgs: { byUser: this.listSession.shift().id }})
          }
        }
      )
    }
  },

  watch: {
    $route: "fetchData"
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