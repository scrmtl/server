<template>
    <div>
        <v-card
        class="lane"
        min-width="340"
        elevation="5"
      >
      <div class="lane-header">
      <p dark>Meine Tasks</p> 
      </div>
        <v-card-text class="lane-body pa-2">
            <Task/>
            <Task/>
            <Task/>
            <Task/>
        </v-card-text>
        <v-card-actions class="lane-extended">

        </v-card-actions>
    </v-card>
    </div>
</template>

<script>
import Task from "@/components/Task.vue"

export default {
    data: () => ({
       
  }),
  components: {
      Task
  }  
}
</script>

<style lang="css" scoped>
@import "../main.css";

</style>