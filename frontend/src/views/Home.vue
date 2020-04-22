<template>
  <div>
    <AppBar />
    <template>
    <v-content>
        <router-view />
    </v-content>
      
    </template>
  </div>
</template>

<script>
import AppBar from "@/components/AppBar.vue";

export default {
  components: {
    AppBar
  }
};
</script>

<style lang="css" scoped></style>
