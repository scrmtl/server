<template>
  <v-content class="tabbody tab-content">
    <v-container fluid class="pl-10">
       <v-row>
          <div v-for="lane in ListLanes" :key="lane.id">
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

  components: {
    Lane

  },
  methods:{
    getPB(){
      var ret = [];
      ret = this.ListBoards.filter(x => x.board_type === "PB");
      console.log(ret);
      return ret;
    },
    ...mapActions("lane", {
            fetchLanes: "fetchList"
            }),
    fetchData() {
        return this.fetchLanes({ customUrlFnArgs: this.getPB()[0].id });
    },
  },
  computed:{
    ...mapGetters("board", {
      ListBoards: "list"
    }),
    ...mapGetters("lane", {
      ListLanes:"list"
    })
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