<template>
  <div>
    <v-hover>
      <template v-slot="{ hover }">
        <v-card class="task mt-4" min-width="300" height="160" :elevation="hover ? 14 : 5">
          <div class="task-header2 task">
            <span class="task-name" @click="showDialog()">{{task.name}}</span>
            <v-spacer></v-spacer>
            <span class="task-status">
              <!-- Card Status: New -->
              <v-tooltip bottom v-if="task.status === 'NW'">
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
              <v-tooltip bottom v-else-if="task.status === 'NS'">
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
              <!-- Card Status: Planned -->
              <v-tooltip bottom v-else-if="task.status === 'PL'">
                <template v-slot:activator="{ on, attrs }">
                  <v-icon
                    class="task-status-icons"
                    color="tabbody"
                    v-bind="attrs"
                    v-on="on"
                  >mdi-notebook</v-icon>
                </template>
                <span>Status: not started</span>
              </v-tooltip>
              <!-- Card Status: In Pogress -->
              <v-tooltip bottom v-else-if="task.status === 'IP'">
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
              <v-tooltip bottom v-else-if="task.status === 'DO'">
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
              <v-tooltip bottom v-else-if="task.status ==='AC'">
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
                  <span>Planned implementation</span>
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
                  <!-- Use Images -->
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
                  <!-- Steps -->
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-icon
                        class="task-status-icons ml-1"
                        color="tabbody"
                        v-bind="attrs"
                        v-on="on"
                      >mdi-check-box-multiple-outline</v-icon>
                    </template>
                    <span>open steps</span>
                  </v-tooltip>
                  <span>{{task.number_of_open_steps}} / {{task.number_of_steps}}</span>
                </div>
              </div>
            </div>
            <!-- assigned Users -->
            <div v-for="user in task.assigned_users" :key="user" class="task-user task">
              <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
              <v-avatar color="red" size="36" v-bind="attrs" v-on="on">
                <span class="white--text headline">{{GetUserInitial(user)}}</span>
              </v-avatar>
              </template>
              <span>{{UsersById(user).username}}</span>
              </v-tooltip>
            </div>
            <div>
              <v-chip-group column class="ml-2">
              <v-chip
                v-for="(label, i) in task.labels"
                :key="i"
                :color="label.color"
                v-text="label.title"
                
              ></v-chip>
            </v-chip-group>
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
import {mapGetters} from "vuex";
export default {
  data: () => ({}),
  props: ["task"],
  components: {
    DetailView
  },

  methods: {
    
    showDialog() {
      this.$store.commit("showDetailView");
      this.$store.commit("setDetailTask", this.task);
    },
    GetUserInitial(id){
      var inital = "AA";
      var user = this.UsersById(id)
      inital = user.username.substring(0,2);
      return inital;
    }
  },
  computed:{
    ...mapGetters("user", {
      UsersById: "byId"
    }),
    

  }

};
</script>

<style lang="css" scoped>
@import "../main.css";
</style>