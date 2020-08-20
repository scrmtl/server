/* eslint-disable */
<template id="app">
  <v-app>
    <v-system-bar>
      <SystemBar/>
    </v-system-bar>
    <v-app-bar>
      <AppBar/>
    </v-app-bar>
    <v-content>
      <router-view/>
    </v-content>
    <v-footer>
      <span>v-footer</span>
    </v-footer>
    <v-bottom-navigation>
      <span>v-bottom-navigation</span>
    </v-bottom-navigation>
  </v-app>
</template>

<script>

import SystemBar from "@/components/SystemBar.vue"
import AppBar from "@/components/AppBar.vue"

export default {
  name: "App",

  components: {
    SystemBar,
    AppBar,  
  },

  methods: {
    
  },

  data: () => ({
    //
  })
};
</script>

<style lang="css" scoped>
@import "/main.css";


</style>
