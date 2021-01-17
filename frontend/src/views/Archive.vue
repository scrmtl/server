<template>
  <v-row no-gutters>
    <v-col dense class="d-flex flex-nowrap overflow-x-auto">
      <div class="ma-4" v-for="lane in listBoardLanes" :key="lane.numbering">
        <ArchiveLane v-bind:lane="lane"></ArchiveLane>
      </div>
    </v-col>
  </v-row>
</template>

<script>
import ArchiveLane from "@/components/Lanes/ArchiveLane.vue";
import { mapGetters } from 'vuex';
export default {
  components: {
    ArchiveLane
  },
  computed: {
    ...mapGetters("sprint", {
      sprintsbyProjectId: "byProjectId",
      listSprints: "list"
    }),
    ...mapGetters("lane", {
      listLanes: "list",
      lanesByIdArray: "byIdArray"
    }),
    ...mapGetters("board", {
      listBoards: "list",
      boardByType: "byType"
    }),
    listBoardLanes(){
      var board = this.boardByType("AB", this.$route.params.id);
      if( board !== undefined){
        return this.lanesByIdArray(board.lanes);
      }
      else{
        return [];
      }
    }
    // listArchivedSprintLanes(){
    //   var board = this.boardByType("AB", this.$route.params.id);
    //   console.log(board);

    //   // var sprints = this.listSprints;
    //   // if( sprints !== undefined){
    //   //   return sprints.filter(sprint => sprint.status === "DO");
    //   // }
    //   // else{
    //   //   return [];
    //   // }
    // }
  },
};
</script>

<style lang="css" scoped>
@import "../main.css";
</style>