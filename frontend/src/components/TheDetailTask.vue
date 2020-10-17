<template>
  <div>
    <v-navigation-drawer
      v-model="visibleDrawer"
      right
      app
      temporary
      hide-overlay
      width="600"
      color="secondary"
      dark
    >
      <v-container>
        <v-tabs
          v-model="tab"
          dark
          background-color="secondary"
          slider-color="link"
          centered
          grow
          tile
        >
          <v-tab>Details</v-tab>
          <v-tab v-if="!selectedTask.visableCreate">Steps</v-tab>
        </v-tabs>
        <!-- Details Tab -->
        <v-tabs-items
          v-model="tab"
          background-color="secondary"
          color="secondary"
        >
          <v-tab-item>
            <v-card flat dark color="secondary" tile>
              <v-card-title>
                <span class="headline ma-0 pa-1">{{ localTask.name }}</span>
              </v-card-title>
              <v-card-text>
                <v-container grid-list-md>
                  <v-row align="center">
                    <v-col>
                      <v-form ref="form" v-model="isFormValid" lazy-validation>
                        <!-- Taskname -->
                        <v-text-field
                          label="Name"
                          required
                          :rules="taskNameRules"
                          :counter="50"
                          prepend-icon="mdi-information-outline"
                          class="ma-1"
                          v-model="localTask.name"
                        ></v-text-field>
                        <!-- Task description -->
                        <v-textarea
                          label="Description"
                          prepend-icon="mdi-information-outline"
                          required
                          outlined
                          class="ma-1"
                          v-model="localTask.description"
                        ></v-textarea>
                      </v-form>
                    </v-col>
                  </v-row>
                  <v-row align="center">
                    <v-col>
                      <v-autocomplete
                        v-model="this.taskNamedStatus"
                        :items="availableStatus"
                        :readonly="this.selectedTask.visableCreate"
                        outlined
                        dense
                        label="Status"
                      ></v-autocomplete>
                    </v-col>
                    <v-col>
                      <v-autocomplete
                        v-model="localTask.storypoints"
                        :items="availableStorypoints"
                        outlined
                        dense
                        label="Story points"
                      ></v-autocomplete>
                    </v-col>
                  </v-row>
                  <v-row v-if="!selectedTask.visableCreate" align="center">
                    <Label v-bind:task="localTask"></Label>
                  </v-row>
                  <v-row align="center">
                    <v-card
                      v-if="!this.selectedTask.visableCreate"
                      flat
                      dark
                      color="secondary"
                      tile
                    >
                      <v-card-title class="title">
                        <span class="headline">Assigned users</span>
                        <v-btn icon @click="assignedUserDialog = true">
                          <v-icon color="link">mdi-dots-horizontal</v-icon>
                        </v-btn>
                        <AssignedUserManagement
                          @close-dialog="assignedUserDialog = false"
                          @add-user="addAssignedUser($event)"
                          @remove-user="deleteAssignedUser($event)"
                          :assignedUsers="allAssignedUsers"
                          :availableUsers="allAvaiblableUsers"
                          :dialog="assignedUserDialog"
                          :dialogName="'Assigned users'"
                          
                        />
                      </v-card-title>
                      <v-card-text>
                        <v-row>
                          <v-col
                            v-for="avatar in allAssignedUsers"
                            :key="`avatar-id-${avatar.id}`"
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
                          </v-col>
                        </v-row>
                      </v-card-text>
                    </v-card>
                  </v-row>
                </v-container>
              </v-card-text>
            </v-card>
          </v-tab-item>
          <!-- Step Tab -->
          <v-tab-item v-if="!selectedTask.visableCreate">
            <v-card flat dark color="secondary" tile>
              <v-card-text>
                <v-row align="center">
                  <v-col>
                    <v-list>
                      <v-list-group
                        value="true"
                        v-for="steplist in selectedTask.details.steplists"
                        :key="steplist"
                      >
                        <template v-slot:activator>
                          <v-list-item-content>
                            <v-list-item-title class="white--text"
                              >Default Steplist</v-list-item-title
                            >
                          </v-list-item-content>
                        </template>
                        <Steplist v-bind:steplistId="steplist" />
                      </v-list-group>
                    </v-list>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-tab-item>
        </v-tabs-items>
        <!-- actions -->
        <div>
          <v-btn color="link" text @click="close()">Close</v-btn>
          <v-btn
            v-if="!this.selectedTask.visableCreate"
            color="link"
            text
            @click="confirm()"
            >Save</v-btn
          >
          <v-btn
            v-if="this.selectedTask.visableCreate"
            color="link"
            :disabled="!isFormValid"
            text
            @click="addTask()"
            >Create</v-btn
          >
          <v-btn
            v-if="!this.selectedTask.visableCreate"
            color="error"
            text
            absolute
            right
            @click="deleteDialog = true"
          >
            <v-icon left>mdi-bucket-outline</v-icon>Delete
          </v-btn>
        </div>
      </v-container>
    </v-navigation-drawer>

    <!-- Delete Dialog -->
    <v-dialog
      v-model="deleteDialog"
      persistent
      class="mx-auto"
      width="600"
      dark
    >
      <v-card color="tabbody" shaped>
        <v-card-text class="headline pt-10">
          <span class="ml-12">Möchten Sie den Task wirklich löschen?</span>
        </v-card-text>
        <v-card-actions class="ml-10 pb-10 pt-10">
          <v-btn width="250" outlined color="error" @click="deleteTaskFn"
            >Ja</v-btn
          >
          <v-btn
            width="250"
            outlined
            color="primary"
            @click="deleteDialog = false"
            >Nein</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>
<script>
import ProfileAvatar from "@/components/Profile/ProfileAvatar.vue";
import ProfileTooltip from "@/components/Profile/ProfileTooltip.vue";
import Steplist from "@/components/Steplist.vue";
import Label from "@/components/Label.vue";
import AssignedUserManagement from "@/components/AssignedUserManagement.vue";
import { mapActions, mapGetters, mapState } from "vuex";
export default {
  name: "DetailTask",
  data: () => ({
    tab: null,
    availableStatus: [
      "New",
      "Planned",
      "Not Started",
      "In Progress",
      "Done",
      "Accepted"
    ],
    availableStorypoints: [0, 1, 2, 3, 5, 8, 13, 21, 34, 55],
    deleteDialog: false,
    assignedUserDialog: false,
    taskNamedStatus: "New",
    localTask: {},
    isFormValid: null,
    taskNameRules: [
      v => !!v || "Name is required",
      v => (v && v.length <= 50) || "Name must be less than 50 characters"
    ]
  }),
  components: {
    ProfileAvatar,
    ProfileTooltip,
    Steplist,
    Label,
    AssignedUserManagement
  },
  methods: {
    ...mapActions("label", {
      fetchLabel: "fetchList",
      createLabel: "create",
      updateLabel: "update",
      deleteLabel: "destroy"
    }),
    ...mapActions("task", {
      createTask: "create",
      fetchSingleTask: "fetchSingle",
      updateTask: "update",
      deleteTask: "destroy"
    }),
    ...mapActions("user", {
      fetchPlattformUsers: "fetchList"
    }),

    close() {
      this.$store.commit("hideTaskDetail");
    },

    confirm() {
      this.saveTask();
      this.$store.commit("hideTaskDetail");
    },
    addAssignedUser(userId){
      if(!this.localTask.assigned_users.includes(userId)){
        this.localTask.assigned_users.push(userId);
      }
      else{
        this.$store.commit("showSystemAlert", {message: "User " + this.plattformUserById(userId).username +" already assigned" , category: "error"});
      }
    },

    addTask() {
      this.createTask({
        data: {
          name: this.localTask.name,
          description: this.localTask.description,
          storypoints: this.localTask.storypoints,
          lane: this.localTask.lane,
          feature: this.localTask.feature
        },
        customUrlFnArgs: {}
      }).then(
        function(value) {
          if (!(value.data.id === undefined)) {
            this.fetchSingleTask({
              id: value.data.id,
              customUrlFnArgs: {}
            });
          }
        }.bind(this)
      );
      this.close();
    },

    saveTask() {
      this.updateTask({
        id: this.localTask.id + "/",
        data: {
          name: this.localTask.name,
          description: this.localTask.description,
          storypoints: this.localTask.storypoints,
          assigned_users: this.localTask.assigned_users,
          status: this.localTask.status,
          lane: this.localTask.lane,
          sprint: this.localTask.sprint,
          feature: this.localTask.feature,
          labels: this.localTask.labels
          // steplists: this.localTask.steplists
        },
        customUrlFnArgs: {}
      }).then(
        function(value) {
          if (!(value.data.id === undefined)) {
            this.fetchSingleTask({
              id: value.data.id,
              customUrlFnArgs: {}
            });
          }
        }.bind(this)
      );
    },

    deleteAssignedUser(userId){
      this.localTask.assigned_users.splice(this.localTask.assigned_users.findIndex(user => user === userId), 1)
    },

    deleteTaskFn() {
      this.deleteDialog = false;
      this.deleteTask({
        id: this.localTask.id + "/",
        customUrlFnArgs: {}
      });
      this.close();
    },

    GetTaskStatus(namedStatus) {
      var status = "AC";
      switch (namedStatus) {
        case "New":
        case "Active":
          status = "AC";
          break;
        case "Archived":
          status = "AR";
          break;
      }
      return status;
    },

    GetTaskNamedStatus(status) {
      var namedStatus = "New";
      switch (status) {
        case "NW":
          namedStatus = "New";
          break;
        case "PL":
          namedStatus = "Planned";
          break;
        case "NS":
          namedStatus = "Not Started";
          break;
        case "DO":
          namedStatus = "Done";
          break;
        case "IP":
          namedStatus = "In Progress";
          break;
        case "AC":
          namedStatus = "Accepted";
          break;
      }
      return namedStatus;
    }
  },
  computed: {
    ...mapState(["selectedTask"]),
    ...mapGetters("user", {
      listPlattfromUsers: "list",
      plattformUsersbyIdArrayWithDetails: "byIdArrayWithDetails",
      plattformUsersbyProjectId: "byProjectId",
      plattformUserById: "byId"
    }),
    ...mapGetters("projectRole", {
      listProjectRoles: "list",
      projectRoleById: "byId"
    }),
    ...mapGetters("steplist", {
      steplistById: "byId"
    }),

    allAssignedUsers() {
      return this.plattformUsersbyIdArrayWithDetails(this.localTask.assigned_users, this.localTask.project);
    },

    allAvaiblableUsers(){
      return this.plattformUsersbyProjectId(this.localTask.project);
    },

    visibleDrawer: {
      get() {
        return this.selectedTask.visableDetail;
      },
      set(newValue) {
        if (newValue) {
          this.$store.commit("showTaskDetail");
        } else {
          this.$store.commit("hideTaskDetail");
        }
      }
    }
  },
  created() {
    this.fetchLabel();
    this.localTask = this.selectedTask.details;
    this.taskNamedStatus = this.GetTaskNamedStatus(this.localTask.status);
  },

  updated() {
    this.localTask = this.selectedTask.details;
    this.taskNamedStatus = this.GetTaskNamedStatus(this.localTask.status);
  }
};
</script>
<style lang="css" scoped>
@import "../main.css";
@import "./Profile/profile.css";
</style>