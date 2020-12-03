/* eslint-disable */
<template>
  <v-app>
    <SystemBar v-if="this.$store.getters.isLoggedIn" />
    <TheNavigation v-if="this.$store.getters.isLoggedIn"/>
    <DetailProject v-if="this.$store.getters.isLoggedIn" />
    <DetailTask v-if="this.$store.getters.isLoggedIn" />
    <DetailSprint v-if="this.$store.getters.isLoggedIn" />
    <!-- v-main is necessary. Do not use v-content -->
    <v-main class="tabbody">
      <router-view />
    </v-main>
    <SystemAlert/>

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
import DetailSprint from "@/components/TheDetailSprint.vue";
import TheNavigation from "@/components/TheNavigation.vue";
import SystemAlert from "@/components/SystemAlert.vue";
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
    DetailSprint,
    TheNavigation,
    SystemAlert
  },

  methods: {
    
  },

  computed:{
    
  },
  created() {
    Axios.interceptors.response.use(function (response){
        return response;
      },
      function (error) {
        console.log(error);
        if (error.status === 401 && error.detail === "Anmeldedaten fehlen.") {
             this.$store.dispatch("logout");
        }
        // return Promise.reject(error);
        // else if(response.status === 403){
        //   console.log("Error from interceptor");
        //   console.log(response);
        //   this.$store.commit("showSystemAlert", {
        //         message: "Permission denied",
        //         category: "error"
        //       });
        // }
        // return new Promise(() => {
        //   if (err.status === 401 && err.detail === "Anmeldedaten fehlen") {
        //     this.$store.dispatch("logout");
        //   }
        //   throw err;
        // });
        // return response;
      });

    Axios.interceptors.request.use(config => {
      if (
        (config.method === "post" || config.method === "patch") &&
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
