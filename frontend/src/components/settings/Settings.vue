<template>
  <v-row justify="center">
    <v-dialog
      v-model="dialog"
      fullscreen
      hide-overlay
      scrollable
      transition="dialog-bottom-transition"
    >
      <v-card color="tabbody">
        <v-toolbar dark color="tabbody">
          <v-btn icon dark @click="close">
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title>Settings</v-toolbar-title>
          <v-spacer></v-spacer>
        </v-toolbar>
        <v-card-text>
          <!-- Setting components -->
          <General />
          <v-divider></v-divider>
          <PlattformUserManagement />
          <v-divider dark></v-divider>
          <LabelManagement />
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script>
import PlattformUserManagement from "@/components/settings/PlattformUserManagement.vue";
import LabelManagement from "@/components/settings/LabelManagement.vue";
import General from "@/components/settings/General.vue";
export default {
  name: "Settings",
  props: {
    dialog: { type: Boolean, default: false },
  },
  components: {
    PlattformUserManagement,
    LabelManagement,
    General,
  },
  methods: {
    close() {
      this.$emit("close-dialog");
    },
  },
};
</script>

<style lang="css">
@import "../../main.css";
</style>