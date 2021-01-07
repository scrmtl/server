<template>
  <v-hover>
    <template v-slot="{ hover }">
      <v-card
        class="task my-2 flex-nowrap"
        min-width="350"
        max-width="350"
        :elevation="hover ? 14 : 5"
        @click="showTaskDetail()"
        draggable
        @dragstart="pickupTask($event, task.id, task.name, task.feature, task.numbering, task.lane, task.sprint, plannedSprint.status, task.storypoints, task.status)"
        
      >
        <v-card-title>
          <span class="tabbody--text">{{ task.name }}</span>
          <v-spacer></v-spacer>
          <div>
            <!-- Card Status: New -->
            <v-tooltip bottom v-if="task.status === 'NW'">
              <template v-slot:activator="{ on, attrs }">
                <v-icon color="tabbody" v-bind="attrs" v-on="on"
                  >mdi-new-box</v-icon
                >
              </template>
              <span>Status: new</span>
            </v-tooltip>
            <!-- Card Status: Not Started -->
            <v-tooltip bottom v-else-if="task.status === 'NS'">
              <template v-slot:activator="{ on, attrs }">
                <v-icon color="tabbody" v-bind="attrs" v-on="on"
                  >mdi-coffee</v-icon
                >
              </template>
              <span>Status: not started</span>
            </v-tooltip>
            <!-- Card Status: Planned -->
            <v-tooltip bottom v-else-if="task.status === 'PL'">
              <template v-slot:activator="{ on, attrs }">
                <v-icon color="tabbody" v-bind="attrs" v-on="on"
                  >mdi-notebook</v-icon
                >
              </template>
              <span>Status: Card in Sprint planned</span>
            </v-tooltip>
            <!-- Card Status: In Pogress -->
            <v-tooltip bottom v-else-if="task.status === 'IP'">
              <template v-slot:activator="{ on, attrs }">
                <v-icon color="tabbody" v-bind="attrs" v-on="on"
                  >mdi-circle-slice-4</v-icon
                >
              </template>
              <span>Status: In Progress</span>
            </v-tooltip>
            <!-- Card Status: Done -->
            <v-tooltip bottom v-else-if="task.status === 'DO'">
              <template v-slot:activator="{ on, attrs }">
                <v-icon color="tabbody" v-bind="attrs" v-on="on"
                  >mdi-beaker-check</v-icon
                >
              </template>
              <span>Status: Done</span>
            </v-tooltip>
            <!-- Card Status: Accepted-->
            <v-tooltip bottom v-else-if="task.status === 'AC'">
              <template v-slot:activator="{ on, attrs }">
                <v-icon color="tabbody" v-bind="attrs" v-on="on"
                  >mdi-bookmark-check</v-icon
                >
              </template>
              <span>Status: Accepted</span>
            </v-tooltip>
          </div>
        </v-card-title>
        <v-card-text class="">
          <v-row dense>
            <v-col >
              <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                  <v-icon 
                    v-if="plannedSprint.start !== ''"
                    color="tabbody" 
                    v-bind="attrs" 
                    v-on="on"
                    >mdi-calendar-range</v-icon
                  >
                </template>
                <span>Planned implementation</span>
              </v-tooltip>
              <span>{{plannedSprint.start}}</span>
            </v-col>
            <v-col cols="auto"></v-col>
            <v-col cols="3">
              <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                  <v-icon
                    class="task-status-icons ml-1"
                    color="tabbody"
                    v-bind="attrs"
                    v-on="on"
                    >mdi-chart-bubble</v-icon
                  >
                </template>
                <span>Story Points</span>
              </v-tooltip>
              <span>{{ task.storypoints }}</span>
            </v-col>
            <v-col cols="3">
              <!-- Steps -->
              <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                  <v-icon
                    class="task-status-icons ml-1"
                    color="tabbody"
                    v-bind="attrs"
                    v-on="on"
                    >mdi-check-box-multiple-outline</v-icon
                  >
                </template>
                <span>open steps</span>
              </v-tooltip>
              <span
                >{{ task.number_of_steps - task.number_of_open_steps }} /
                {{ task.number_of_steps }}</span
              >
            </v-col>
          </v-row>
          <v-row dense>
            <div
              v-for="avatar in avatarsStackedLimited"
              :key="`avatar-id-${avatar.id}`"
              class="pa-1"
            >
              <v-menu
                open-delay="1500"
                open-on-hover
                :nudge-width="200"
                offset-y
              >
                <template v-slot:activator="{ on, attrs }">
                  <div v-bind="attrs" v-on="on">
                    <ProfileAvatar :avatar="avatar" />
                  </div>
                </template>
                <ProfileTooltip :avatar="avatar" />
              </v-menu>
            </div>
            <v-col align-self="center" v-if="task.assigned_users.length > 5">
              <v-avatar color="primary" size="32px">
                <span class="white--text">
                  +{{ task.assigned_users.length - 5 }}
                </span>
              </v-avatar>
            </v-col>
          </v-row>
          <v-row dense>
            <v-col>
              <v-chip-group column v-if="task.labels">
                <v-chip
                  v-for="label in task.labels"
                  :key="label"
                  :color="labelById(label).color"
                  v-text="labelById(label).title"
                  text-color="white--text"
                  small
                ></v-chip>
              </v-chip-group>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>
    </template>
  </v-hover>
</template>

<script>
import { mapGetters } from "vuex";
import ProfileAvatar from "@/components/Profile/ProfileAvatar.vue";
import ProfileTooltip from "@/components/Profile/ProfileTooltip.vue";

export default {
  data: () => ({
    dialog: null
  }),
  props: ["task"],
  components: {
    ProfileAvatar,
    ProfileTooltip
  },

  methods: {
    showTaskDetail() {
      this.$store.commit("selected/setTaskDetail", this.task);
      if(this.$route.path.endsWith("Archive")){
        this.$store.commit("selected/showTaskDetailWithReadOnly", false);
      }
      else if(this.$route.path.endsWith("ProductBacklog") && !this.allowedChanges){
        this.$store.commit("showSystemAlert", {
          message: "You are not a PO. Read only access in Product backlog",
          category: "warning"
        });
        this.$store.commit("selected/showTaskDetailWithReadOnly", false);
      }
      else{
        this.$store.commit("selected/showTaskDetail", false);
      }
    },
    GetUserInitial(id) {
      var inital = "AA";
      var user = this.UsersById(id);
      inital = user.username.substring(0, 2);
      return inital;
    },
    pickupTask(e, taskId, taskName, taskFeatureId, taskNumbering, fromLane, sprint, sprintStatus, storypoints, taskStatus){
      e.dataTransfer.effectAllowed = "move";
      e.dataTransfer.dropEffect = "move";
      e.dataTransfer.setData("task-id", taskId);
      e.dataTransfer.setData("task-name", taskName);
      e.dataTransfer.setData("task-status", taskStatus);
      e.dataTransfer.setData("task-feature-id", taskFeatureId);
      e.dataTransfer.setData("task-numbering", taskNumbering);
      e.dataTransfer.setData("task-sprint-id", sprint);
      e.dataTransfer.setData("task-sprint-status", sprintStatus);
      e.dataTransfer.setData("task-storypoints", storypoints);
      e.dataTransfer.setData("from-lane", fromLane);
      
    },
  },
  computed: {
    ...mapGetters("user", {
      UsersById: "byId",
      usersByIdArray: "byIdArray",
      usersbyIdArrayWithDetails: "byIdArrayWithDetails"
    }),
    ...mapGetters("label", {
      labelById: "byId"
    }),
    ...mapGetters("sprint", {
      sprintById: "byId"
    }),
     ...mapGetters("session", {
      listSession: "list"
    }),
    ...mapGetters("projectUser",{
      listProjectUser: "list"
    }),
    allowedChanges(){
      var allowed = false;
      // role id 1 is always product owner
      var productOwnersInProject = this.listProjectUser.filter(projectUser => projectUser.role === 1 && projectUser.project == this.task.project);
      if(this.listSession !== undefined && productOwnersInProject !== undefined){
        if (productOwnersInProject.find(po => po.plattform_user === this.listSession[0].id) !== undefined){
          allowed = true;
        }
        else{
          allowed = false;
        }
      }
      return allowed;
    },

    plannedSprint(){ 
      var sprintInfo = {
        start: "",
        end: "",
        status: "",
      }
      if(this.task.sprint != null){
        sprintInfo.start = this.sprintById(this.task.sprint).start;
        sprintInfo.end = this.sprintById(this.task.sprint).end;
        sprintInfo.status = this.sprintById(this.task.sprint).status;
        return sprintInfo
      }
      else{
        return sprintInfo
      }  
    },

    avatarsSorted() {
      return this.usersbyIdArrayWithDetails(this.task.assigned_users, this.task.project);
    },
    avatarsStackedLimited() {
      return this.avatarsSorted && this.avatarsSorted.length > 0
        ? this.avatarsSorted.slice(0, 5)
        : null;
    }
  }
};
</script>

<style lang="css" scoped>
@import "../main.css";
@import "./Profile/profile.css";
</style>