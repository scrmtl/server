<template>
  <v-alert
    :value="systemAlert.visible"
    
    dense
    dismissible
    :type="systemAlert.category"
    @input="closeAlert"
  >
    {{systemAlert.message}}
  </v-alert>
</template>

<script>
import {mapState } from "vuex";
export default { 
  methods: {
    closeAlert() {
      this.$store.commit("hideSystemAlert");
    },
  },
  computed:{
    ...mapState(["systemAlert"]),
  }
}
</script>

<style>

</style>