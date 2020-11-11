/* eslint-disable */
<template>
  <v-app>
    <SystemBar v-if="this.$store.getters.isLoggedIn" />
    <TheNavigation/>
    <DetailProject v-if="this.$store.getters.isLoggedIn" />
    <DetailTask v-if="this.$store.getters.isLoggedIn" />
    <!-- v-main is necessary. Do not use v-content -->
    <v-main class="tabbody">
      <router-view />
    </v-main>
    <v-footer color="appbar" class="white--text" app>
      <span>dark, cool, easy</span>
      <v-spacer></v-spacer>
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>
import SystemBar from "@/components/TheSystemBar.vue";
import DetailProject from "@/components/TheDetailProject.vue";
import DetailTask from "@/components/TheDetailTask.vue";
import TheNavigation from "@/components/TheNavigation.vue";
import Axios from "axios";
export default {
  name: "App",
  data: () => ({
    //
  }),
  components: {
    SystemBar,
    DetailProject,
    DetailTask, 
    TheNavigation
  },

  methods: {
    
  },

  computed:{
    
  },
  created() {
    Axios.interceptors.response.use((response) => {
      if (response.status === 401 && response.detail === "Anmeldedaten fehlen") {
          this.$store.dispatch("logout");
      }
      else if(response.status === 403){
        console.log(response);
      }
      // return new Promise(() => {
      //   if (err.status === 401 && err.detail === "Anmeldedaten fehlen") {
      //     this.$store.dispatch("logout");
      //   }
      //   throw err;
      // });
      return response;
    });

    Axios.interceptors.request.use(config => {
      // console.log(config);
      if (
        (config.method === "post") | (config.method === "patch") &&
        config.url[config.url.length - 1] !== "/" &&
        !config.url.includes("/?")
      ) {
        config.url += "/";
      }
      return config;
    });
  }
};
</script>

<style lang="css" >
@import "/main.css";
</style>
