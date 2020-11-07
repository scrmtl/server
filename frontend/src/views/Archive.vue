<template>
  <v-main class="tabbody tab-content">
    <v-col>
      
      <v-timeline>
        <v-timeline-item
          small
          fill-dot
          color="tabbody"
        >
          <template v-slot:icon>
            <v-btn fab small icon color="link" >
              <v-icon>mdi-plus-circle-outline</v-icon>
            </v-btn>
          </template>
        </v-timeline-item>
        
        <v-timeline-item
          v-for="sprint in listSprints" :key="sprint.number"
          small
          fill-dot
          
        >
          <template v-slot:icon>
            <v-btn fab small color="link" class="white--text" >{{sprint.number}}</v-btn>
            
          </template>

        </v-timeline-item>

      </v-timeline>
    </v-col>
    <v-col>
      <!-- Hier kommt dann das weitere... /-->
      <v-text>
        Hier kommt der Graph
      </v-text> 
    </v-col>
    <v-col>
      Hier die 4 Statisik-Werte
    </v-col>
  </v-main>
</template>

<script>
import { mapGetters } from 'vuex';
export default {
  data: () => ({
    selectedSprintName: "No sprint selected"
  }),
  components: {
  },
  methods:{
    

  },
  computed:{
    ...mapGetters("sprint", {
      listSprints: "list"
    }),
  }
};
</script>

<style lang="css" scoped>
@import "../main.css";
</style>