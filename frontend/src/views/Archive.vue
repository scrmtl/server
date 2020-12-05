<template>
  <v-row no-gutters>
    <v-col dense class="d-flex flex-nowrap overflow-x-auto">
      <div class="ma-4" v-for="sprint in listArchivedSprintLanes" :key="sprint.number">
        <ArchiveLane v-bind:sprint="sprint"></ArchiveLane>
      </div>
    </v-col>
  </v-row>
</template>

<script>
import ArchiveLane from "@/components/ArchiveLane.vue";
import { mapGetters } from 'vuex';
export default {
  components: {
    ArchiveLane
  },
  computed: {
    ...mapGetters("sprint", {
      sprintsbyProjectId: "byProjectId",
      listSprints: "list"
    }),
    listArchivedSprintLanes(){
      var sprints = this.listSprints;
      if( sprints !== undefined){
        return sprints.filter(sprint => sprint.status === "DO");
      }
      else{
        return [];
      }
    }
  },
};
</script>

<style lang="css" scoped>
@import "../main.css";
</style>