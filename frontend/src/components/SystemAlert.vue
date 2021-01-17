<template>
  <v-snackbar
    app
    :value="systemAlert.visible"  
    :timeout="7000"
    left
    multi-line
    :color="StatusColor"
    @input="closeAlert"
  >
    {{systemAlert.message}}
    <template v-slot:action="{ attrs }">
        <v-btn
          text
          v-bind="attrs"
          @click="closeAlert"
        >
          CLOSE
        </v-btn>
      </template>
  </v-snackbar>
</template>

<script>
import {mapState } from "vuex";
export default { 
   data: () => ({
    show: false,
  }),
  
  methods: {
    closeAlert() {
      this.$store.commit("hideSystemAlert");
    },
  },
  computed:{
    ...mapState(["systemAlert"]),

    StatusColor(){
      var color
      switch (this.systemAlert.category) {
        case "info":
          color = "light-blue darken-3";
          break;
        case "warning":
          color = "amber darken-3";
          break;
        case "success":
          color = "green darken-3";
          break;
        case "error":
          color = "red darken-3";
          break;
        default:
          color = "grey darken-3";
          break;
      }
      return color;
    }
  },
}
</script>

<style>

</style>