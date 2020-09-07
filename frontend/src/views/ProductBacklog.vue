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
        this.fetchLanes({ customUrlFnArgs: this.getBoardId() });
        this.listLanes;
    },
  },
  computed:{
    ...mapGetters("lane", {
      listLanes: "list"
    }),
    ...mapGetters("board", {
      listBoards: "list"
    }),
  },
  updated(){
    this.listLanes;
  },
  created(){
    this.fetchData();
  }

};

</script>

<style lang="css" scoped>
@import "../main.css";

</style>