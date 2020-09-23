<template>

  <v-container fluid class="tabbody">
    <v-row >
      <v-col v-for="lane in listLanes" :key="lane.id">
        <Lane v-bind:lane="lane"></Lane>
      </v-col>
    </v-row>
  </v-container>


</template>

<script>
import { mapGetters, mapActions } from 'vuex';
import Lane from "@/components/Lane.vue";
export default {
  data: () => ({

  }),
  components: {
    Lane
  },
  methods:{
    ...mapActions("lane", {
            fetchLanes: "fetchList"
            }),

    getBoardId(){
      var boards = this.listBoards;
      var selectedBoard = boards.filter(x => x.board_type === "PB").shift();
      var boardId = selectedBoard.id
      return boardId;
    },

    fetchData() {
        this.fetchLanes({ customUrlFnArgs: this.boardByType("PB").id });
    },
  },
  computed:{
    ...mapGetters("lane", {
      listLanes: "list"
    }),
    ...mapGetters("board", {
      listBoards: "list",
      boardByType: "byType"
    }),
  },
  updated(){

  },
  created(){
    this.fetchData();
  }

};

</script>

<style lang="css" scoped>
@import "../main.css";

</style>