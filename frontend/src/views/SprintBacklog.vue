<template>
    <v-row dense>
      <v-col dense class="d-flex flex-nowrap overflow-x-auto" >
        <div class="ma-4" v-for="lane in listBoardLanes" :key="lane.numbering">
          <Lane v-bind:lane="lane"></Lane>
        </div>
      </v-col>
    </v-row>
</template>

<script>
import Lane from "@/components/Lanes/Lane.vue";
import { mapGetters } from "vuex";
export default {
  data: () => ({
    selectedBoard: {}
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
      var board = this.boardByType("SP", this.$route.params.id);
      if( board !== undefined){
        return this.lanesByIdArray(board.lanes);
      }
      else{
        return [];
      }
    }
  },
  updated(){

  },
  created(){
    
  },

  // mounted() {
  //   this.fetchData();
  //   setInterval(
  //     function() {
  //       this.fetchData();
  //     }.bind(this),
  //     10000
  //   );
  // }
};
</script>

<style lang="css" scoped>
@import "../main.css";

</style>