<template>
  <div>
    <v-navigation-drawer 
    v-model="visibleDrawer"  
    right
    app
    temporary
    
    width="600" 
    color="navbar" 
    dark>

      <v-container> 
          <v-tabs
            v-model="tab"
            dark
            background-color="navbar"
            slider-color="link"
            centered
            grow
            tile
          >
            <v-tab>Details</v-tab>
            <v-tab>Settings</v-tab>
          </v-tabs>

          <v-tabs-items v-model="tab" background-color="navbar" color="navbar">
            <v-tab-item>
              <v-card flat dark color="navbar" tile>
                <v-card-text>
                  <v-form
                  ref="form"
                  v-model="isFormValid"
                  lazy-validation
                  >
                    <!-- Projectname -->
                    <v-row align="center">
                      <v-col>
                        <v-text-field
                          label="Project name"
                          required
                          :rules="[rules.required, rules.counter]"
                          :counter="50"
                          prepend-icon="mdi-information-outline"
                          v-model="localProject.name"
                        ></v-text-field>
                      </v-col>
                    </v-row>
                    <!-- Project start -->
                    <v-row align="center">
                      <v-col>
                        <v-menu
                          ref="menu"
                          v-model="calendar1menu"
                          :close-on-content-click="false"
                          transition="scale-transition"
                          offset-y
                          min-width="290px"
                        >
                          <template v-slot:activator="{ on, attrs }">
                            <v-text-field
                              v-model="localProject.start"
                              label="Project start"
                              hint="YYYY-MM-DD"
                              prepend-icon="mdi-calendar-range"
                              required
                              :rules="[rules.required]"
                              persistent-hint
                              readonly
                              v-bind="attrs"
                              v-on="on"
                            ></v-text-field>
                          </template>
                          <v-date-picker 
                            v-model="localProject.start" 
                            no-title 
                            scrollable 
                            :readonly="!this.selectedProject.visableCreate">
                            <v-spacer></v-spacer>
                            <v-btn text color="primary" @click="calendar1menu = false">Cancel</v-btn>
                            <v-btn text color="primary" @click="calendar1menu = false">OK</v-btn>
                          </v-date-picker>
                        </v-menu>
                      </v-col>
                    </v-row>
                    <!-- Project end -->
                    <v-row align="center">
                      <v-col>
                        <v-menu
                          ref="menu"
                          v-model="calendar2menu"
                          :close-on-content-click="false"
                          transition="scale-transition"
                          offset-y
                          min-width="290px"
                        >
                          <template v-slot:activator="{ on, attrs }">
                            <v-text-field
                              v-model="localProject.end"
                              label="Project end"
                              hint="YYYY-MM-DD"
                              prepend-icon="mdi-calendar-range"
                              required
                              readonly
                              :rules="[rules.required]"
                              persistent-hint
                              v-bind="attrs"
                              v-on="on"
                            ></v-text-field>
                          </template>
                          <v-date-picker 
                            v-model="localProject.end" 
                            no-title 
                            scrollable 
                            :readonly="!this.selectedProject.visableCreate">
                            <v-spacer></v-spacer>
                            <v-btn text color="primary" @click="calendar2menu = false">Cancel</v-btn>
                            <v-btn text color="primary" @click="calendar2menu = false">OK</v-btn>
                          </v-date-picker>
                        </v-menu>
                      </v-col>
                    </v-row>
                    <!-- Sprint duration -->
                    <v-row align="center">
                      <v-col>
                        <v-text-field
                          label="Sprint duration"
                          required
                          :rules="[rules.required, rules.duration]"
                          :counter="3"
                          :readonly="!this.selectedProject.visableCreate"
                          persistent-hint
                          hint="in calendar days (not workdays)"
                          prepend-icon="mdi-information-outline"
                          v-model="localProject.sprint_duration"
                        ></v-text-field>
                      </v-col>
                    </v-row>
                    <!-- Projectdiscription -->
                    <v-row align="center">
                      <v-col>
                        <v-textarea
                          label="Project description"
                          prepend-icon="mdi-information-outline"
                          outlined
                          min-height="70"
                          v-model="localProject.description"
                        ></v-textarea>
                      </v-col>
                    </v-row>
                    <!-- Definition of Ready -->
                    <v-row align="center">
                      <v-col>
                        <v-textarea
                          label="Definition of Ready"
                          prepend-icon="mdi-information-outline"
                          outlined
                          min-height="70"
                          class="ma-1"
                          v-model="localProject.dor"
                        ></v-textarea>
                      </v-col>
                    </v-row>
                    <!-- Definition of Done -->
                    <v-row align="center">
                      <v-col>
                        <v-textarea
                          label="Definition of Done"
                          prepend-icon="mdi-information-outline"
                          outlined
                          min-height="70"
                          class="ma-0"
                          v-model="localProject.dod"
                        ></v-textarea>
                      </v-col>
                    </v-row>
                  </v-form>
                    
                </v-card-text>
              </v-card>
              <!-- Project Sprint Infos -->
              <v-card v-if="!this.selectedProject.visableCreate"
                flat
                dark
                color="navbar"
                tile>
                <v-card-text>
                  <span class="headline ma-4">Sprintinformationen</span>
                  <v-row>
                    <div class="ma-4">
                      <v-progress-circular
                        :rotate="-90"
                        :size="100"
                        :width="15"
                        :value="finshedSprints"
                        color="link"
                      >{{ finshedSprints }}/{{localProject.numOfSprints}}</v-progress-circular>
                    </div>
                    <div class="ma-4">
                      <p>Finished sprints: {{finshedSprints}}</p>
                      <p>Sprint duration in calendar days: {{localProject.sprint_duration}}</p>
                      <p>Number of Sprints: {{localProject.numOfSprints}}</p>
                    </div>
                  </v-row>
                </v-card-text> 
              </v-card>
            </v-tab-item>
            <!-- Settings Tab -->
            <v-tab-item>
                <v-card flat dark color="navbar" tile>
                  <v-card-text>
                    <v-row align="center">
                      <v-col>
                        <v-select
                          :items="['Active', 'Archived']"
                          label="Status"
                          :readonly="this.selectedProject.visableCreate"
                          prepend-icon="mdi-circle-edit-outline"
                          v-model="this.projectNamedStatus"

                        ></v-select>
                      </v-col>
                    </v-row>
                  </v-card-text>
                </v-card>              
                <v-card 
                  v-if="!this.selectedProject.visableCreate" 
                  flat 
                  dark 
                  color="navbar" 
                  tile>
                  <v-card-title class="title">
                    <span class="headline">Assigned project users</span>
                    <v-btn icon>
                        <v-icon color="link" >mdi-dots-horizontal</v-icon>
                    </v-btn>
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
                            <ProfileAvatar :avatar="avatar"/>
                            </div>
                          </template>
                          <ProfileTooltip :avatar="avatar" />
                        </v-menu>
                      </v-col>
                    </v-row>
                  </v-card-text>
                </v-card>
            </v-tab-item>
          </v-tabs-items>
          <div>
          <v-btn color="link" text @click="close()">Close</v-btn>
            <v-btn v-if="!this.selectedProject.visableCreate" color="link" text @click="confirm()">Save</v-btn>
            <v-btn v-if="this.selectedProject.visableCreate" color="link" :disabled="!isFormValid" text @click="addProject()">Create</v-btn>
            <v-btn v-if="!this.selectedProject.visableCreate" color="error" text absolute right @click="deleteDialog = true">
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
          <span class="ml-12">Möchten Sie das Projekt wirklich löschen?</span> 
        </v-card-text>
        <v-card-actions class="ml-10 pb-10 pt-10">
          <v-btn width="250" outlined color="error" @click="deleteProject()">Ja</v-btn>
          <v-btn width="250" outlined color="primary" @click="deleteDialog = false">Nein</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import ProfileAvatar from "@/components/Profile/ProfileAvatar.vue";
import ProfileTooltip from "@/components/Profile/ProfileTooltip.vue";
import {mapActions, mapGetters, mapState } from "vuex";
export default {
  name: "DetailProject",
  data: () => ({
    tab: null,
    calendar1menu: false,
    calendar2menu: false,
    deleteDialog: false,    
    isFormValid: null,
    finshedSprints: 0,
    projectNamedStatus: "New",
    localProject: {},
    rules: {
      required: value => !!value || 'Required',
      counter: value => value.length <= 20 || 'Max 50 characters',
      duration: value => {
        const pattern = /^([0-9]{1,3})$/
        return pattern.test(value) || 'Invalid Duration'
      }
    },
    projectNameRules: [
        v => !!v || 'Name is required',
        v => (v && v.length <= 50) || 'Name must be less than 50 characters',
      ],
    projectSprintDurationRules: [
      v => !!v || 'Duration is required',
    ]
  }),
  components: {
    ProfileAvatar,
    ProfileTooltip
  },
  methods: {
    ...mapActions("project", {
      updateProject: "update",
      destroyProject: "destroy",
      createProject: "create"
    }),

    ...mapActions("projectUser", {
      fetchProjectUser: "fetchList",
      createProjectUser: "create",
      destroyProjectUser: "delete"

    }),
    ...mapActions("projectRole", {
      fetchProjectRoles: "fetchList",

    }),
    ...mapActions("user", {
      fetchPlattformUsers: "fetchList",
    }),
    
    close(){
      this.$store.commit("hideProjectDetail");
    },

    confirm() {
      this.saveProject();
      this.$store.commit("hideProjectDetail");
    },

    
    addProject(){
      this.createProject({
        data: {
          name: this.localProject.name,
          description: this.localProject.description,
          start: this.localProject.start,
          end: this.localProject.end,
          sprint_duration: this.localProject.sprint_duration,
          dor: this.localProject.dor,
          dod: this.localProject.dod,
          status: this.GetProjectStatus(this.projectNamedStatus),
          project_users: this.localProject.project_users
        }
      })
    },

    GetProjectStatus(namedStatus){
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

    GetProjectNamedStatus(status){
      var namedStatus = "Active";
      switch (status) {
        case "AC":
          namedStatus = "Active";
          break;
        case "AR":
          namedStatus = "Archived";
          break;
      }
      return namedStatus;
    },

    


    // GetAllProjectUsers(){
    //   var data = [];
    //   var plattformUser;
    //   try {
    //     Object.values(this.listProjectUsers).forEach(projectUser =>
    //       {
    //         plattformUser = Object.values(this.plattformUserById(projectUser.plattform_user)).shift();

    //         data.push({
    //         name: plattformUser.name,
    //         email: plattformUser.email,
    //         username: plattformUser.username,
    //         role: this.projectRoleById(projectUser.role).role_name
    //         });
    //       }
    //     )
    //     console.log(data);
    //   } catch (error) {
    //     if (this.listProjectRoles === undefined) {
    //       this.fetchProjectRoles();
    //     }
    //     if (this.listPlattformUsers === undefined) {
    //       this.fetchPlattformUsers();
    //     }
    //   }
    //   return data;
    // },

    saveProject() {
      this.updateProject({
        id: this.localProject.id + "/",
        data: {
          id: this.localProject.id,
          name: this.localProject.name,
          description: this.localProject.description,
          status: this.GetProjectStatus(this.projectNamedStatus),
          dor: this.localProject.dor,
          dod: this.localProject.dod
        }
      });
    },

    deleteProject() {
      this.deleteDialog = false;
      this.destroyProject({
        id: this.localProject.id + "/"
      });
      this.close();
    }
  },
  computed: {
    ...mapState(["selectedProject"]),
    ...mapGetters("projectUser", {
      listProjectUsers: "list",
      projectUserById: "byId",
      projectUsersByIdArray: "byIdArray"
    }),
    ...mapGetters("projectRole", {
      listProjectRoles: "list",
      projectRoleById: "byId"
    }),
    ...mapGetters("user", {
      listPlattfromUsers: "list",
      plattformUserById: "byId",
    }),
    
    allAssignedUsers(){
      
      var projectUsers = this.projectUsersByIdArray(this.localProject.project_users);
      var assignedUsers = [];
      if (projectUsers && projectUsers.length > 0){
        projectUsers.forEach(prjUser => {
          var plattformUser = this.plattformUserById(prjUser.plattform_user);
          assignedUsers.push(
            {
              id: plattformUser.id,
              email: plattformUser.email,
              name: plattformUser.name,
              username: plattformUser.username,
              role: this.projectRoleById(prjUser.role).role_name,
            }
          )
        })
      }
      console.log(assignedUsers);
      return assignedUsers;
    },

    visibleDrawer: {
      get() {
        return this.selectedProject.visableDetail;
      },
      set(newValue) {
        this.selectedProject.visableDetail = newValue;
      }
    }
  },

  created() {
    this.fetchProjectUser();
    this.fetchProjectRoles();
    this.localProject = this.selectedProject.details;
    this.projectNamedStatus = this.GetProjectNamedStatus(this.localProject.status);
  },

  updated() {
    this.localProject = this.selectedProject.details;
    this.projectNamedStatus = this.GetProjectNamedStatus(this.localProject.status);

  },
  
};
</script>

<style lang="css" scoped>
  @import "../main.css";
  @import './Profile/profile.css';
</style>