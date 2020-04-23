<template>
  <div class="tabbody tab-content">
    <v-card max-width="280" height="850" color="lanbody" raised="10" class="lane">
      <v-toolbar color="border" height="50">
        <v-app-bar-nav-icon></v-app-bar-nav-icon>

        <v-toolbar-title>Example Lane</v-toolbar-title>

        <v-spacer></v-spacer>

        <v-btn icon>
          <v-icon>mdi-dots-vertical</v-icon>
        </v-btn>
      </v-toolbar>
      <v-container>Lorem Ipsum</v-container>
    </v-card>
  </div>
</template>

<script>
export default {};
</script>

<style lang="css" scoped>
.tab-content {
  height: 1000px;
}
.lane {
  padding: 0;
}
</style>
