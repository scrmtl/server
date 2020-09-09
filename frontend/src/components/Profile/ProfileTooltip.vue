<template>

    <v-layout column>
      <span class="font-weight-medium">{{ avatar.username }}</span>
      <span>{{ avatar.email }}</span>
    </v-layout>
    
</template>
<script>
export default {
  props: {
    avatar: {
      default: () => {},
      type: Object
    }
  },
  
}
</script>
<style lang="css" scoped>
@import './profile.css';
</style>