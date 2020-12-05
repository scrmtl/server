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
          <v-tab :disabled="visableCreate">Steps</v-tab>
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
                <span class="headline ma-0 pa-1">{{ name }}</span>
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
                          :readonly="status === 'DO' || status === 'AC' || readOnly"
                          v-model="name"
                        ></v-text-field>
                        <!-- Task description -->
                        <v-textarea
                          label="Description"
                          prepend-icon="mdi-information-outline"
                          required
                          outlined
                          :readonly="status === 'DO' || status === 'AC' || readOnly"
                          class="ma-1"
                          v-model="description"
                        ></v-textarea>
                      </v-form>
                    </v-col>
                  </v-row>
                  <v-row align="center">
                    <v-col>
                      <v-autocomplete
                        v-model="taskNamedStatus"
                        :items="availableStatus"
                        :readonly="disableStatusChange"
                        :disabled="disableStatusChange"
                        outlined
                        dense
                        label="Status"
                      ></v-autocomplete>
                    </v-col>
                    <v-col>
                      <v-autocomplete
                        v-model="storypoints"
                        :items="availableStorypoints"
                        :disabled="status === 'DO' || status === 'AC' || readOnly"
                        outlined
                        dense
                        label="Story points"
                      ></v-autocomplete>
                    </v-col>
                  </v-row>
                  <v-row align="center">
                    <v-col>
                      <v-text-field
                        v-model="this.plannedSprintNumber"
                        disabled
                        readonly
                        outlined
                        dense
                        label="Sprint No."
                      ></v-text-field>
                    </v-col>
                    <v-col>
                      <v-text-field
                        v-model="this.plannedSprintStart"
                        disabled
                        readonly
                        outlined
                        dense
                        label="Sprint start Date"
                      ></v-text-field>
                    </v-col>
                    <v-col>
                      <v-text-field
                        v-model="this.plannedSprintEnd"
                        disabled
                        readonly
                        outlined
                        dense
                        label="Sprint due date"
                      ></v-text-field>
                    </v-col>          
                  </v-row>
                  <v-row align="start">
                    <v-col>
                      <v-text-field
                        v-model="this.plannedSprintVersion"
                        disabled
                        readonly
                        outlined
                        dense
                        label="Planned product version"
                      ></v-text-field>
                    </v-col>
                  </v-row>
                  <v-row v-if="!visableCreate" align="center">
                    <Label ></Label>
                  </v-row>
                  <v-row align="center">
                    <v-card
                      v-if="!visableCreate"
                      flat
                      dark
                      color="secondary"
                      tile
                    >
                      <v-card-title class="title">
                        <span class="headline">Assigned users</span>
                        <v-btn 
                          :disabled="readOnly" 
                          icon 
                          @click="assignedUserDialog = true" 
                          class="hidden-sm-and-down"
                        >
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
          <v-tab-item :disabled="visableCreate">
            <v-card flat dark color="secondary" tile>
              <v-card-text>
                <v-row align="center">
                  <v-col>
                    <v-list :disabled="readOnly" >
                      <v-list-group
                        value="true"
                        v-for="steplist in steplists"
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
          <v-btn
            color="link" 
            text 
            @click="close()"
          >Close</v-btn>
          <v-btn
            v-if="!visableCreate && !readOnly"
            color="link"
            text
            @click="confirm()"
            >Save</v-btn>
          <v-btn
            v-if="visableCreate"
            color="link"
            :disabled="!isFormValid"
            text
            @click="addTask()"
            >Create</v-btn
          >
          <v-btn
            v-if="!visableCreate && this.sprint == null"
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
import { mapActions, mapGetters } from "vuex";
import { mapFields } from "vuex-map-fields";
export default {
  name: "TheDetailTask",
  data: () => ({
    tab: null,
    availableStorypoints: [0, 1, 2, 3, 5, 8, 13, 21, 34, 55],
    deleteDialog: false,
    assignedUserDialog: false,
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
    ...mapActions("lane", {
      fetchSingleLane: "fetchSingle",
    }),
    ...mapActions("user", {
      fetchPlattformUsers: "fetchList"
    }),

    close() {
      this.$store.commit("selected/hideTaskDetail");
    },

    confirm() {
      this.saveTask();
      this.$store.commit("selected/hideTaskDetail");
    },
    addAssignedUser(userId){
      if(!this.assigned_users.includes(userId)){
        this.assigned_users.push(userId);
      }
      else{
        this.$store.commit("showSystemAlert", {message: "User " + this.plattformUserById(userId).username +" already assigned" , category: "error"});
      }
    },

    addTask() {
      this.createTask({
        data: {
          name: this.name,
          description: this.description,
          storypoints: this.storypoints,
          lane: this.lane,
          feature: this.feature,
          status: "NW"
        },
        customUrlFnArgs: {}
      }).then(
        function(value) {
          if (!(value.data.id === undefined)) {
            this.fetchSingleTask({
              id: value.data.id,
              customUrlFnArgs: {}
            })
            this.fetchSingleLane({
              id: this.lane, 
              customUrlFnArgs: {}
            }) 
          }
          this.close();
        }.bind(this)
      );
      
    },

    saveTask() {
      
      var data = {
        name: this.name,
        feature: this.feature,
      }
      // Declined Workflow
      // If the task declined from PO, is a workflow nessesary
      if(this.status === "DE"){
        var lanes = this.laneByName("Ready (for next Sprints)");
        if(lanes.length > 0){
          data.status = "NW"
          data.lane = lanes.shift().id
          data.sprint = null
        }
      }
      // normal save
      else{
        data.description = this.description;
        data.storypoints = this.storypoints;
        data.assigned_users = this.assigned_users;
        data.status = this.status;
        data.lane = this.lane;
        data.sprint = this.sprint;
        data.labels = this.labels;
      }

      this.updateTask({
        id: this.id,
        data,
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
      this.assigned_users.splice(this.assigned_users.findIndex(user => user === userId), 1)
    },

    deleteTaskFn() {
      this.deleteDialog = false;
      this.deleteTask({
        id: this.id + "/",
        customUrlFnArgs: {}
      });
      this.close();
    },

    
  },
  computed: {
    // See more under Two-way Computed Property https://vuex.vuejs.org/guide/forms.html
    // Implementation with https://github.com/maoberlehner/vuex-map-fields
    // the string after the last dot (e.g. `id`) is used
    // for defining the name of the computed property.
    ...mapFields("selected", [
      "task.details.id",
      "task.details.lane",
      "task.details.feature",
      "task.details.status",
      "task.details.name",
      "task.details.storypoints",
      "task.details.steplists",
      "task.details.labels",
      "task.details.sprint",
      "task.details.project",
      "task.details.description",
      "task.details.assigned_users",
      "task.visableDetail",
      "task.visableCreate",
      "task.readOnly",
    ]),
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
    ...mapGetters("sprint", {
      sprintById: "byId"
    }),
    ...mapGetters("lane", {
      laneByName: "byName"
    }),

    plannedSprintNumber(){
      if(this.sprint != null){
        return this.sprintById(this.sprint).number
      }
      else{
        return "Task not planned"
      }      
    },
    plannedSprintStart(){ 
      if(this.sprint != null){
        return this.sprintById(this.sprint).start
      }
      else{
        return "Task not planned"
      }  
    },

    plannedSprintVersion(){
      if(this.sprint != null){
        return this.sprintById(this.sprint).version
      }
      else{
        return "Task not planned"
      }
    },

    plannedSprintEnd(){
      if(this.sprint != null){
        return this.sprintById(this.sprint).end
      }
      else{
        return "Task not planned"
      }
    },

    allAssignedUsers() {
      return this.plattformUsersbyIdArrayWithDetails(this.assigned_users, this.project);
    },

    allAvaiblableUsers(){
      return this.plattformUsersbyProjectId(this.project);
    },
    disableStatusChange(){
      if(this.visableCreate){
        return true;
      }
      else if(this.readOnly){
        return true;
      }
      else if(this.status === "DO" || this.status === "AC" || this.status === "DE"){
        return false;
      }
      else{
        return true;
      }
    },
    availableStatus(){
      if(this.status === "DO" || this.status === "AC" || this.status === "DE"){
        return [
          "Done",
          "Accepted",
          "Declined"
        ]
      }
      else{
        return [
          "New",
          "Planned",
          "Not Started",
          "In Progress",
          "Done",
          "Accepted",
          "Declined"
        ]
 
      }
    },

    taskNamedStatus: {
      get() {
        var namedStatus = "New";
        switch (this.status) {
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
          case "DE":
            // If the task declined from PO, is a workflow nessesary
            namedStatus = "Declined";
            break;
        }
        return namedStatus;
      },
      set(value) {
        var status = "NW";
        switch (value) {
          case "NW":
            status = "NW";
            break;
          case "Planned":
            status = "PL";
            break;
          case "Not Started":
            status = "NS";
            break;
          case "Done":
            status = "DO";
            break;
          case "In Progress":
            status = "IP";
            break;
          case "Accepted":
            status = "AC";
            break;
          case "Declined":
            // If the task declined from PO, is a workflow nessesary
            status = "DE";
            break;
        }
        this.status = status;
      }
    },

    visibleDrawer: {
      get() {
        return this.visableDetail;
      },
      set(newValue) {
        if (newValue) {
          this.$store.commit("selected/showTaskDetail");
        } else {
          this.$store.commit("selected/hideTaskDetail");
        }
      }
    }
  },
  watch:{
    visibleDrawer(val, prev){
      if(val === prev) return;
    },
  },

  created() {
    this.fetchLabel();
  },

  updated() {
    
  }
};
</script>
<style lang="css" scoped>
  @import "../main.css";
  @import "./Profile/profile.css";
</style>