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
import { mapGetters } from 'vuex';
import Lane from "@/components/Lane.vue";
export default {
  data: () => ({

  }),
  components: {
    Lane
  },
  methods:{

  },
  computed:{
    ...mapGetters("lane", {
      listLanes: "list",
      lanesByIdArray: "byIdArray"
    }),
    ...mapGetters("board", {
      listBoards: "list",
      boardByType: "byType"
    }),
    listBoardLanes(){
      return this.lanesByIdArray(this.boardByType("PB").lanes);
    }

  },
  updated(){

  },
  created(){
    
  }

};

</script>

<style lang="css" scoped>
@import "../main.css";

</style>