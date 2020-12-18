<template>
  <v-row no-gutters>
    <v-col dense class="d-flex flex-nowrap overflow-x-auto">
      <div class="ma-4" v-for="lane in listBoardLanes" :key="lane.numbering">
        <Lane v-bind:lane="lane" allowedAdd></Lane>
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
    checkWritePermisson(){
      //only POs can change PB
      console.log(this.listSession)
      console.log(this.projectUserByRole("product owner"))
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
    }),
    ...mapGetters("session", {
      listSession: "list",
    }),
    ...mapGetters("projectUser", {
      projectUserByRole: "byRole",
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
    this.checkWritePermisson();
  }
};
</script>

<style lang="css" scoped>
@import "../main.css";
</style>