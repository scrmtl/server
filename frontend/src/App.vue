/* eslint-disable */
<template>
  <v-app >
    
    <SystemBar/>
    <DetailProject/>
    <DetailTask/>
    <!-- v-main is necessary. Do not use v-content -->
    <v-main>
        <router-view/>      
    </v-main>
    

    <v-footer color="appbar" class="white--text" app>
      <span>dark, cool, easy</span>
      <v-spacer></v-spacer>
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>

import SystemBar from "@/components/SystemBar.vue";
import DetailProject from "@/components/DetailProject.vue";
import DetailTask from "@/components/DetailTask.vue";

export default {
  name: "App",
  data: () => ({
    //
  }),
  components: {
    SystemBar,
    DetailProject, 
    DetailTask
  },

  methods: {
    
  },
};
</script>

<style lang="css" >
@import "/main.css";


</style>
