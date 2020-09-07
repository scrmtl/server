/* eslint-disable */
<template id="app">
  <v-app>
    <v-system-bar>
      <SystemBar/>
    </v-system-bar>

    <v-content>
      <router-view/>
    </v-content>
  </v-app>
</template>

<script>

import SystemBar from "@/components/SystemBar.vue"


export default {
  name: "App",

  components: {
    SystemBar,  
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
