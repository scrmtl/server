<template>
  <v-container fluid class="tabbody">
    <v-row>

      <v-col lg="4"  >
        <MyTasksLane />
      </v-col>
    </v-row>
    
  </v-container>
</template>

<script>
  import MyTasksLane from "@/components/MyTasksLane.vue";
  export default {
        
    components: {
      MyTasksLane,
    },
  }
</script>

<style lang="css" scoped>
@import "../main.css";

</style>