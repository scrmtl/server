<template>
  <v-card tile flat>
    <v-card-title class="navbar white--text"
      >Project Information
      <v-btn class="hidden-sm-and-down" icon @click="showProjectDetail()">
        <v-icon color="link">mdi-dots-horizontal</v-icon>
      </v-btn>
    </v-card-title>
    <v-card-text class="navbar">
      <v-row align="center">
        <v-col>
          <v-text-field
            label="Project name"
            readonly
            dark
            outlined
            dense
            :value="projectInformation.name"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row align="center">
        <!-- Project start -->
        <v-col>
          <v-text-field
            label="Project start"
            readonly
            dark
            outlined
            dense
            :value="projectInformation.start"
          ></v-text-field>
        </v-col>
        <!-- Project end -->
        <v-col>
          <v-text-field
            label="Project end"
            readonly
            dark
            outlined
            dense
            :value="projectInformation.end"
          ></v-text-field>
        </v-col>
      </v-row>
      <!-- Sprint duration -->
      <v-row align="center">
        <v-col>
          <v-text-field
            label="Sprint duration"
            readonly
            dark
            outlined
            dense
            :value="projectInformation.sprint_duration"
          ></v-text-field>
        </v-col>
      </v-row>
      <!-- Projectdiscription -->
      <v-row align="center">
        <v-col>
          <v-textarea
            label="Project description"
            readonly
            dark
            outlined
            min-height="70"
            :value="projectInformation.description"
          ></v-textarea>
        </v-col>
      </v-row>
      <!-- Definition of Ready -->
      <v-row align="center">
        <v-col>
          <v-textarea
            label="Definition of Ready"
            readonly
            dark
            outlined
            min-height="70"
            :value="projectInformation.dor"
          ></v-textarea>
        </v-col>
      </v-row>
      <!-- Definition of Done -->
      <v-row align="center">
        <v-col>
          <v-textarea
            label="Definition of Done"
            readonly
            dark
            outlined
            min-height="70"
            :value="projectInformation.dod"
          ></v-textarea>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  name: "ProjectInformation",
  data: () => ({}),

  computed: {
    ...mapGetters("project", {
      projectById: "byId",
    }),

    projectInformation() {
      var project = this.projectById(this.$route.params.id);
      return project;
    },
  },

  methods: {
    showProjectDetail() {
      this.$store.commit("selected/showProjectDetail", false);
      this.$store.commit(
        "selected/setProjectDetail",
        this.projectById(this.$route.params.id)
      );
    },
  },
};
</script>

<style></style>
