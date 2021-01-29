<template>
  <v-snackbar
    app
    :value="visible"
    :timeout="7000"
    left
    multi-line
    :color="StatusColor"
    @input="closeAlert"
  >
    {{ message }}
    <template v-slot:action="{ attrs }">
      <v-btn
        v-if="linkVisible"
        text
        color="link"
        :to="{ name: linkDestination }"
        >{{ linkName }}
      </v-btn>
      <v-btn text v-bind="attrs" @click="closeAlert">CLOSE</v-btn>
    </template>
  </v-snackbar>
</template>

<script>
import { mapFields } from "vuex-map-fields";
export default {
  data: () => ({
    show: false,
  }),
  methods: {
    closeAlert() {
      this.$store.commit("hideSystemAlert");
    },
  },
  computed: {
    // See more under Two-way Computed Property https://vuex.vuejs.org/guide/forms.html
    // Implementation with https://github.com/maoberlehner/vuex-map-fields
    // the string after the last dot (e.g. `id`) is used
    // for defining the name of the computed property.
    ...mapFields([
      "systemAlert.category",
      "systemAlert.linkName",
      "systemAlert.linkVisible",
      "systemAlert.linkDestination",
      "systemAlert.message",
      "systemAlert.visible",
    ]),

    StatusColor() {
      var color;
      switch (this.category) {
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
    },
  },
};
</script>

<style></style>
