<template>
  <v-list
    three-line
    subheader
    dark
    color="tabbody"
  >
    <v-subheader class="subtitle-1">General</v-subheader>
    <v-list-item>
      <v-list-item-action>
        <v-checkbox v-model="notifications"></v-checkbox>
      </v-list-item-action>
      <v-list-item-content>
        <v-list-item-title>Notifications</v-list-item-title>
        <v-list-item-subtitle>Notify me about updates at planning poker</v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>
  </v-list> 
</template>

<script>
export default {
  name: "General",
  data: () =>({
    notifications: false,
  })
}
</script>

<style>

</style>