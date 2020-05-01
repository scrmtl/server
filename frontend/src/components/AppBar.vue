<template>
  <v-app-bar app color="appbar" dark>
    <v-app-bar-nav-icon></v-app-bar-nav-icon>
    <v-toolbar-title>Scrum-Tool</v-toolbar-title>
    <v-spacer></v-spacer>
    <v-icon>mdi-account-circle</v-icon>
    <span>
      Username
      <br />
      Profil
    </span>
    <template v-slot:extension >
      <v-tabs background-color="navbar">
        <v-tab title="Home">
          <v-icon>mdi-home</v-icon>
        </v-tab>
        <v-tab-item >
            <HomeComponent/>
        </v-tab-item>
        <v-tab title="Product Backlog">
          Product Backlog
        </v-tab>
        <v-tab-item>
          <ProductBacklog />
        </v-tab-item>
        <v-tab title="Sprint Planing">
          Sprint Planing
        </v-tab>
        <v-tab-item>
          <SprintPlaning />
        </v-tab-item>
        <v-tab title="Sprint Backlog">
          Sprint Backlog
        </v-tab>
        <v-tab-item>
          <SprintBacklog />
        </v-tab-item>
        <v-tab title="Statistik">
          Statistik
        </v-tab>
        <v-tab-item>
          <Statistic />
        </v-tab-item>
        <v-spacer></v-spacer>
        <div class="navbar-icons">
          <span class="icons">
            <v-icon>mdi-magnify</v-icon>
          </span>
          <span class="icons">
            <v-icon>mdi-refresh</v-icon>
          </span>
          <span class="icons">
            <v-icon>mdi-cogs</v-icon>
          </span>
          <span class="icons">
            <v-icon>mdi-help-circle-outline</v-icon>
          </span>
        </div>
      </v-tabs>
    </template>
  </v-app-bar>
</template>

<script>
import ProductBacklog from "@/components/ProductBacklog.vue";
import SprintPlaning from "@/components/SprintPlaning.vue";
import SprintBacklog from "@/components/SprintBacklog.vue";
import Statistic from "@/components/Statistic.vue";
import HomeComponent from "@/components/HomeComp.vue";

export default {
  components: {
    ProductBacklog,
    SprintPlaning,
    SprintBacklog,
    Statistic,
    HomeComponent
  },
  methods: {
    
  }
};
</script>

<style lang="css">
.navbar-icons {
  padding-top: 10px;
  padding-right: 12px;
}
.icons {
  padding-left: 12px;
}

</style>
