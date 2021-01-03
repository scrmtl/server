<template>
  <v-container fluid class="tabbody">
    <v-row class="d-flex" dense>
      <v-col cols="12">
        <router-view></router-view>
      </v-col>
    </v-row>
    <v-overlay
      :value="
        boardsIsLoading || lanesIsLoading || tasksIsLoading || sprintsIsLoading
      "
    >
      <v-progress-circular
        :size="70"
        :width="7"
        color="link"
        indeterminate
      ></v-progress-circular>
    </v-overlay>
  </v-container>
</template>

<script>
import { mapActions, mapState } from "vuex";
export default {
  props: ["id"],
  data: () => ({
    loading: false
  }),
  components: {},
  methods: {
    ...mapActions("board", {
      fetchBoards: "fetchList"
    }),
    ...mapActions("lane", {
      fetchLanes: "fetchList"
    }),
    ...mapActions("task", {
      fetchTasks: "fetchList"
    }),
    ...mapActions("sprint", {
      fetchSprints: "fetchList"
    }),
    ...mapActions("sprintStatistics", {
      fetchSprintStatistics: "fetchList"
    }),
    ...mapActions("projectStatistics", {
      fetchProjectStatistics: "fetchList"
    }),
    ...mapActions("session", {
      fetchSession: "fetchList",
    }),

    fetchData() {
      this.fetchBoards({ customUrlFnArgs: { projectId: this.id } });
      this.fetchLanes({ customUrlFnArgs: { projectId: this.id } });
      this.fetchTasks({ customUrlFnArgs: { projectId: this.id } });
      this.fetchSprints({ customUrlFnArgs: { projectId: this.id } });
      this.fetchSession({ customUrlFnArgs: { all: false } });
      this.fetchSprintStatistics();
      this.fetchProjectStatistics();
    }
  },
  computed: {
    ...mapState("board", {
      boardsIsLoading: "isFetchingList"
    }),
    ...mapState("lane", {
      lanesIsLoading: "isFetchingList"
    }),
    ...mapState("task", {
      tasksIsLoading: "isFetchingList"
    }),
    ...mapState("sprint", {
      sprintsIsLoading: "isFetchingList"
    })
  },
  created() {
    this.fetchData();
  }
};
</script>

<style lang="css" scoped>
@import "../main.css";
</style>