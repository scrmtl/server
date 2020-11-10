<template>
  <v-row no-gutters>
    <v-col dense class="d-flex flex-nowrap overflow-x-auto">
      <div class="ma-4" v-for="lane in boardLanes" :key="lane.numbering">
        <Lane v-bind:lane="lane"></Lane>
      </div>
    </v-col>
  </v-row>
</template>

<script>
import { mapGetters } from "vuex";
import Lane from "@/components/Lane.vue";
export default {
  data: () => ({
    boardLanes: Array
  }),
  components: {
    Lane
  },
  methods: {
    listBoardLanes() {
      let projectId = this.listBoards.shift().project;
      console.log(projectId);
      return this.lanesByIdArray(this.boardByType("PB", projectId).lanes);
    }
  },
  computed: {
    ...mapGetters("lane", {
      listLanes: "list",
      lanesByIdArray: "byIdArray"
    }),
    ...mapGetters("board", {
      listBoards: "list",
      boardByType: "byType"
    })
  },
  mounted() {
    let projectId = this.listBoards.shift().project;
    let laneIds = this.boardByType("PB", projectId).lanes;
    this.boardLanes = this.lanesByIdArray(laneIds);
  }
};
</script>

<style lang="css" scoped>
@import "../main.css";
</style>