<template>

    <v-row dense>
      <v-col dense class="d-flex flex-nowrap overflow-x-auto" >
        <div class="ma-4" v-for="lane in listLanes" :key="lane.id">
          <Lane v-bind:lane="lane"></Lane>
        </div>
      </v-col>
    </v-row>
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

    fetchData() {
      this.fetchLanes({ customUrlFnArgs: this.boardByType("SP").id });
    },
  },
  computed: {
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