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
import { mapGetters, mapActions } from 'vuex';
import Lane from "@/components/Lane.vue";
export default {
  data: () => ({}),
  components: {
    Lane
  },
  methods:{
    ...mapActions("lane", {
            fetchLanes: "fetchList"
            }),

     getBoardId(){
      var ret = this.boardList.filter(x => x.board_type === "PB").shift().id;
      console.log(ret);
      return ret;
    },

    fetchData() {
        return this.fetchLanes({ customUrlFnArgs: this.getBoardId() });
    },
  },
  computed:{
    ...mapGetters("lane", {
      laneList: "list"
    }),
    ...mapGetters("board", {
      boardList: "list"
    }),
  },
  updated(){
    console.log(this.ListBoards);
  },
  created(){
    this.fetchData();
  }

};
</script>

<style lang="css" scoped>
@import "../main.css";

</style>