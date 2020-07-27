<template>
  <div>
    <v-dialog v-model="visible" persistent class="task mt-4" elevation="5" max-width="600px">
      <v-card class="task mt-4">
        <div class="task-header2 task">
          <v-card-title class="task-name">Task Name</v-card-title>
        </div>
        <v-card-text></v-card-text>
        <v-card-actions>
          <v-btn background-color="error" outlined color="error" @click="close()">Close</v-btn>
          <v-btn background-color="link" outlined color="link" @click="confirm()">Confirm</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>


<script>
import { mapState } from "vuex";

export default {
  name: "DetailView",
  data: () => ({}),

  created: function() {
    this.$store.commit("hideDetailView");
  },

  computed: {
    ...mapState({
      visible: "detailViewVisable"
    })
  },

  methods: {
    confirm() {
      this.$store.commit("hideDetailView");
    },

    close() {
      this.$store.commit("hideDetailView");
    }
  }
};
</script>