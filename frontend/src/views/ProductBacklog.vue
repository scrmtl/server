<template>
  <v-row no-gutters>
    <v-col dense class="d-flex flex-nowrap overflow-x-auto">
      <div class="ma-4" v-for="lane in listBoardLanes" :key="lane.numbering">
        <Lane v-bind:lane="lane" :allowedAdd="allowedChanges"></Lane>
      </div>
    </v-col>
  </v-row>
</template>

<script>
import { mapGetters } from "vuex";
import Lane from "@/components/Lanes/Lane.vue";
export default {
  data: () => ({
    // boardLanes: Array
  }),
  components: {
    Lane,
  },
  methods: {},
  computed: {
    ...mapGetters("lane", {
      listLanes: "list",
      lanesByIdArray: "byIdArray",
    }),
    ...mapGetters("board", {
      listBoards: "list",
      boardByType: "byType",
    }),
    ...mapGetters("projectUser", {
      listProjectUser: "list",
    }),
    ...mapGetters(["getUserinfo"]),
    allowedChanges() {
      var allowed = false;
      // role id 1 is always product owner
      var productOwnersInProject = this.listProjectUser.filter(
        (projectUser) =>
          projectUser.role == 1 && projectUser.project == this.$route.params.id
      );
      if (
        this.getUserinfo !== undefined &&
        productOwnersInProject !== undefined
      ) {
        if (
          productOwnersInProject.find(
            (po) => po.plattform_user == this.getUserinfo.userId
          ) !== undefined
        ) {
          allowed = true;
        } else {
          allowed = false;
        }
      }
      return allowed;
    },

    listBoardLanes() {
      var board = this.boardByType("PB", this.$route.params.id);
      if (board !== undefined) {
        return this.lanesByIdArray(board.lanes);
      } else {
        return [];
      }
    },
  },
  mounted() {
    if (!this.allowedChanges) {
      this.$store.commit("showSystemAlert", {
        message: "You are not a PO. Read only access in Product backlog",
        category: "warning",
      });
    }
  },
};
</script>

<style lang="css" scoped>
@import "../main.css";
</style>
