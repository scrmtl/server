<template>
  <v-card min-width="385" max-width="420">
    <v-card-title class="navbar white--text">
      <div>
        {{ selectedSprintName }}
      </div>
      <v-spacer></v-spacer>
      <v-menu offset-y close-on-click>
        <template v-slot:activator="{ on }">
          <v-btn dark icon v-on="on" class="icon" height="32">
            <v-icon>mdi-dots-vertical</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item 
            v-for="(menuItem, i) in menu" :key="i" 
            @click="menuItem.action"
          >
          <v-list-item-icon>
            <v-icon v-text="menuItem.icon"></v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title v-text="menuItem.text"></v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        </v-list>
      </v-menu>
    </v-card-title>
    <v-card-subtitle class="navbar white--text">
      {{ selectedSprintInfo }}
    </v-card-subtitle>
    <v-card-text class="lane-body  flex-column" >
      <v-row justify="center"  class="" v-for="task in sprintLaneTask" :key="task.id">
        <Task v-bind:task="task" />
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
import Task from "@/components/Task.vue";
import { mapGetters } from 'vuex';
export default {
  data: () => ({
    selectedSprintName: "No sprint selected",
    selectedSprintInfo: "",
    item: 1,
    menu: [
      { text: "Create new sprint", icon: 'mdi-plus-circle-outline', action: "createSprint" },
      { text: "Sprint details", icon: 'mdi-information-outline', action: "showSprintDetails" },
    ],
  }),
  components: {
    Task
  },
  methods:{
    createSprint(){
      console.log("Create Sprint")
    },
    showSprintDetails(){
      console.log("show Sprint detail")
    }

  },
  computed:{
    ...mapGetters(
      {sprintDetails: "getSprintDetails"}),
    
    sprintLaneTask(){
      return [];
    },


  },
  watch:{
    sprintDetails(newSprint){
      console.log(newSprint)
      this.selectedSprintName = "Sprint " + newSprint.number;
      this.selectedSprintInfo = "(" + newSprint.start + " to " + newSprint.end + ")"
    }
  }

}
</script>

<style lang="css" scoped>
  @import "../main.css";
</style>