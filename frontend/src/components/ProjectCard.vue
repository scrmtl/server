<template>
  <div>
    <v-hover>
      <template v-slot="{ hover }">
        <v-card class="navbar projectCard" max-width="350" dark shaped :elevation="hover ? 24 : 1">
          <router-link 
          :to="{name: 'ProjectDashboard', params: {id: project.id }}"
          style="text-decoration: none; color: inherit;"
          >
          <v-list-item 
          three-line
          >
            <v-list-item-content>
              <v-list-item-title class="headline mb-1">{{project.name}}</v-list-item-title>
              <v-list-item-subtitle>
                <span>{{project.description}}</span>
              </v-list-item-subtitle>
            </v-list-item-content>

            <v-list-item-avatar tile size="100" color="transparent">
              <v-progress-circular
                :rotate="-90"
                :size="100"
                :width="15"
                :value="valueCard"
                color="link"
              >{{ valueCard }}</v-progress-circular>
            </v-list-item-avatar>
          </v-list-item>
          </router-link>
          <v-card-actions>
            <v-btn text outlined color="link" @click="showProjectDetail()">Details</v-btn>         
            <v-spacer></v-spacer>
            <v-spacer></v-spacer>
            <v-btn text color="link" v-if="project.status === 'AC'" >ACTIVE</v-btn>
            <v-btn text color="grey" v-else-if="project.status === 'AR'" >ARCHIVED</v-btn>
          </v-card-actions>
        </v-card>
      </template>
    </v-hover>
    
  </div>
</template>

<script>

import {  mapActions } from "vuex";
export default {
  props: ["project"],
  data() {
    return {
      valueCard: "50/100",
      valueDetail: "30/100",
    };
  },
  
  components: {
    
  },

  methods: {
    ...mapActions("projectUser", {
      fetchProjectUsers: "fetchList"
    }),

    showProjectDetail() {
      this.$store.commit("selected/showProjectDetail", false);
      this.$store.commit("selected/setProjectDetail", this.project);
    },
  },
  computed:{

  },
  created(){
    
  }
};
</script>

<style lang="css" scoped>
@import "../main.css";
</style>