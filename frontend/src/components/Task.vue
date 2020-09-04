<template>
  <div>
    <v-hover>
      <template v-slot="{ hover }">
        <v-card class="task mt-4" min-width="300" height="160" :elevation="hover ? 14 : 5">
          <div class="task-header2 task">
            <span class="task-name" @click="showDialog">{{task.name}}</span>
            <v-spacer></v-spacer>
            <span class="task-status">
              <!-- Card Status: New -->
              <v-tooltip bottom v-if="task.status = 'NW'">
                <template v-slot:activator="{ on, attrs }">
                  <v-icon
                    class="task-status-icons"
                    color="tabbody"
                    v-bind="attrs"
                    v-on="on"
                  >mdi-new-box</v-icon>
                </template>
                <span>Status: new</span>
              </v-tooltip>
              <!-- Card Status: Not Started -->
              <v-tooltip bottom v-else-if="task.status = 'NS'">
                <template v-slot:activator="{ on, attrs }">
                  <v-icon
                    class="task-status-icons"
                    color="tabbody"
                    v-bind="attrs"
                    v-on="on"
                  >mdi-coffee</v-icon>
                </template>
                <span>Status: not started</span>
              </v-tooltip>
              <!-- Card Status: In Pogress -->
              <v-tooltip bottom v-else-if="task.status = 'IP'">
                <template v-slot:activator="{ on, attrs }">
                  <v-icon
                    class="task-status-icons"
                    color="tabbody"
                    v-bind="attrs"
                    v-on="on"
                  >mdi-circle-slice-4</v-icon>
                </template>
                <span>Status: In Progress</span>
              </v-tooltip>
              <!-- Card Status: Done -->
              <v-tooltip bottom v-else-if="task.status = 'DO'">
                <template v-slot:activator="{ on, attrs }">
                  <v-icon
                    class="task-status-icons"
                    color="tabbody"
                    v-bind="attrs"
                    v-on="on"
                  >mdi-beaker-check</v-icon>
                </template>
                <span>Status: Done</span>
              </v-tooltip>
              <!-- Card Status: Accepted-->
              <v-tooltip bottom v-else-if="task.status = 'AC'">
                <template v-slot:activator="{ on, attrs }">
                  <v-icon
                    class="task-status-icons"
                    color="tabbody"
                    v-bind="attrs"
                    v-on="on"
                  >mdi-bookmark-check</v-icon>
                </template>
                <span>Status: Accepted</span>
              </v-tooltip>
            </span>
          </div>
          <v-card-text class="pa-0 task">
            <div class="task-body2 task">
              <div class="task-icons">
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-icon
                      class="task-status-icons ml-1"
                      color="tabbody"
                      v-bind="attrs"
                      v-on="on"
                    >mdi-calendar-range</v-icon>
                  </template>
                  <span>Endtime</span>
                </v-tooltip>
                <span>DD/MM/JJJJ</span>
                <div class="task-icons2">
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-icon
                        class="task-status-icons ml-1"
                        color="tabbody"
                        v-bind="attrs"
                        v-on="on"
                      >mdi-chart-bubble</v-icon>
                    </template>
                    <span>Story Points</span>
                  </v-tooltip>
                  <span>{{task.storypoints}}</span>
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-icon
                        class="task-status-icons ml-1"
                        color="tabbody"
                        v-bind="attrs"
                        v-on="on"
                      >mdi-file-image-outline</v-icon>
                    </template>
                    <span>Task: used images</span>
                  </v-tooltip>
                  <span>1</span>
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-icon
                        class="task-status-icons ml-1"
                        color="tabbody"
                        v-bind="attrs"
                        v-on="on"
                      >mdi-check-box-multiple-outline</v-icon>
                    </template>
                    <span>Task: To-Do List</span>
                  </v-tooltip>
                  <span>5/8</span>
                </div>
              </div>
            </div>
            <div class="task-user task">
              <v-avatar height="36" width="36">
                <img src="https://cdn.vuetifyjs.com/images/john.jpg" alt="John" />
              </v-avatar>
              <v-avatar height="36" width="36">
                <img src="https://cdn.vuetifyjs.com/images/john.jpg" alt="John" />
              </v-avatar>
            </div>

            <div class="task-labels2 task">
              <div class="label-backend backend">
                <span>Backend</span>
              </div>
              <div class="label-frontend frontend">
                <span>Frontend</span>
              </div>
              <div class="label-ux ui_ux">
                <span>UX/UI</span>
              </div>
              <div class="label-bug bug">
                <span>BUG</span>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </template>
    </v-hover>
    <DetailView></DetailView>
  </div>
</template>

<script>
import DetailView from "../components/DetailView";
export default {
  data: () => ({}),
  props: ["task"],
  components: {
    DetailView
  },

  methods: {
    showDialog() {
      this.$store.commit("showDetailView");
    }
  }
};
</script>

<style lang="css" scoped>
@import "../main.css";
</style>