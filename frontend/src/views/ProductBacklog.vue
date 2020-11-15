<template>
  <v-row no-gutters>
    <v-col dense class="d-flex flex-nowrap overflow-x-auto">
      <div class="ma-4" v-for="lane in listBoardLanes" :key="lane.numbering">
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
    // boardLanes: Array
  }),
  components: {
    Lane
  },
  methods: {

  },
  computed: {
    ...mapGetters("lane", {
      listLanes: "list",
      lanesByIdArray: "byIdArray"
    }),
    ...mapGetters("board", {
      listBoards: "list",
      boardByType: "byType"
    }),
    listBoardLanes(){
      var board = this.boardByType("PB", this.$route.params.id);
      if( board !== undefined){
        return this.lanesByIdArray(board.lanes);
      }
      else{
        return [];
      }
    }
  },
  mounted() {  
  }
};
</script>

<style lang="css" scoped>
@import "../main.css";
</style>