<template>
  <v-content class="tabbody tab-content">
    <v-container fluid class="pl-10">
       <v-row>
          <div v-for="lane in laneList" :key="lane.id">
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
      
      if(!this.selectedBoard){
        this.selectedBoard = this.boardList.filter(x => x.board_type === "SB").shift();;
      }
      return this.selectedBoard.id;
    },

    fetchData() {
      this.fetchLanes({ customUrlFnArgs: this.getBoardId()});

    }
  },
  computed: {
    ...mapGetters("lane", {
      laneList: "list"
    }),
    ...mapGetters("board", {
      boardList: "list"
    }),
  },

  created() {
    this.fetchData();
  },

  mounted() {
    this.fetchData();
    setInterval(
      function() {
        this.fetchData();
      }.bind(this),
      10000
    );
  }
};
</script>

<style lang="css" scoped>
@import "../main.css";
</style>