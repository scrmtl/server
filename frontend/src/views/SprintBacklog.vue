<template>
  <v-content class="tabbody tab-content">
    <v-container fluid class="pl-10">
       <v-row>
          <div v-for="lane in listLanes" :key="lane.id">
            <Lane v-bind:lane="lane"></Lane>
          </div>
      </v-row>
    </v-container>
  </v-content>
</template>

<script>
import Lane from "@/components/Lane.vue";
import { mapGetters, mapActions} from "vuex";
export default {
  data: () => ({
    selectedBoard: {}
  }),
  components: {
    Lane
  },
  methods: {
    ...mapActions("lane", {
      fetchLanes: "fetchList"
    }),
    getBoardId(){
      var boards = this.listBoards;
      var selectedBoard = boards.filter(x => x.board_type === "SP").shift();
      var boardId = selectedBoard.id;
      return boardId;
    },

    fetchData() {
      this.fetchLanes({ customUrlFnArgs: this.getBoardId() });
    },
  },
  computed: {
    ...mapGetters("lane", {
      listLanes: "list"
    }),
    ...mapGetters("board", {
      listBoards: "list"
    }),
  },
  updated(){

  },
  created(){
    this.fetchData();
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