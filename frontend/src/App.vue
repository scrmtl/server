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
import DetailSprint from "@/components/Sprint/TheDetailSprint.vue";
import TheNavigation from "@/components/TheNavigation.vue";
import SystemAlert from "@/components/SystemAlert.vue";
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
    logout() {
      console.log("Error 401 detected")
      this.$store.dispatch("logout").then(() => {
        this.$router.push("/login");
      });
    },
    createSystemAlert(message, category){
      this.$store.commit("showSystemAlert", {
        message: message,
        category: category
      });
    }
  },

  computed:{
    
  },
  mounted() {
   
  }
};
</script>

<style lang="css" >
  @import "/main.css";
</style>
