<template>
  <div>
    <v-navigation-drawer
      v-model="visibleDrawer"
      right
      app
      temporary
      hide-overlay
      width="600"
      color="navbar"
      dark
    >
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
              <v-card-title>
                <span class="headline">{{ name }}</span>
              </v-card-title>
              <v-card-text>
                <v-form ref="form" v-model="isFormValid" lazy-validation>
                  <!-- Projectname -->
                  <v-row align="center">
                    <v-col>
                      <v-text-field
                        label="Project name"
                        required
                        :rules="[rules.required]"
                        :counter="50"
                        prepend-icon="mdi-information-outline"
                        v-model="name"
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
                            v-model="start"
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
                          v-model="start"
                          no-title
                          scrollable
                          :readonly="!this.visableCreate"
                        >
                          <v-spacer></v-spacer>
                          <v-btn
                            text
                            color="primary"
                            @click="calendar1menu = false"
                            >Cancel</v-btn
                          >
                          <v-btn
                            text
                            color="primary"
                            @click="calendar1menu = false"
                            >OK</v-btn
                          >
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
                            v-model="end"
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
                          v-model="end"
                          no-title
                          scrollable
                          :readonly="!visableCreate"
                        >
                          <v-spacer></v-spacer>
                          <v-btn
                            text
                            color="primary"
                            @click="calendar2menu = false"
                            >Cancel</v-btn
                          >
                          <v-btn
                            text
                            color="primary"
                            @click="calendar2menu = false"
                            >OK</v-btn
                          >
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
                        :readonly="!visableCreate"
                        persistent-hint
                        hint="in calendar days (not workdays)"
                        prepend-icon="mdi-information-outline"
                        v-model="sprint_duration"
                      ></v-text-field>
                    </v-col>
                  </v-row>
                </v-form>
                <!-- Projectdiscription -->
                <v-row align="center">
                  <v-col>
                    <v-textarea
                      label="Project description"
                      prepend-icon="mdi-information-outline"
                      outlined
                      min-height="70"
                      v-model="description"
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
                      v-model="dor"
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
                      v-model="dod"
                    ></v-textarea>
                  </v-col>
                </v-row>
                <!-- Template for creation -->
                <v-row align="center" v-if="visableCreate">
                  <v-col>
                    <v-combobox
                      :items="templateProjectItems"
                      clearable
                      placeholder="Start typing to Search"
                      v-model="selectedProjectTemplate"
                      item-text="name"
                      item-value="id"
                      label="Template Projects"
                    ></v-combobox>
                  </v-col>
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
                      prepend-icon="mdi-circle-edit-outline"
                      v-model="projectNamedStatus"
                    ></v-select>
                  </v-col>
                </v-row>
                <!-- Project as template -->
                <v-row>
                  <v-checkbox
                    input-value="false"
                    label="Use this project as template"
                    v-model="is_template"
                  ></v-checkbox>
                </v-row>
              </v-card-text>
            </v-card>
            <v-card
              v-if="!visableCreate"
              flat
              dark
              color="navbar"
              tile
            >
              <v-card-title class="title">
                <span class="headline">Assigned project users</span>
                <v-btn icon @click="userManagementDialog = true">
                  <v-icon color="link">mdi-dots-horizontal</v-icon>
                </v-btn>
                <AssignedUserManagement
                  @close-dialog="userManagementDialog = false"
                  @add-user="addProjectUser($event)"
                  @remove-user="deleteProjectUser($event)"
                  :assignedUsers="allAssignedUsers"
                  :availableUsers="listPlattfromUsers"
                  :dialog="userManagementDialog"
                  :dialogName="'Assigned project users'"
                  roleEditing
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
          </v-tab-item>
        </v-tabs-items>
        <div>
          <v-btn color="link" text @click="close()">Close</v-btn>
          <v-btn
            v-if="!visableCreate"
            color="link"
            text
            @click="confirm()"
            >Save</v-btn
          >
          <v-btn
            v-if="visableCreate"
            color="link"
            :disabled="!isFormValid"
            text
            @click="addProject()"
            >Create</v-btn
          >
          <v-btn
            v-if="!visableCreate"
            color="error"
            text
            absolute
            right
            @click="deleteProjectDialog = true"
          >
            <v-icon left>mdi-bucket-outline</v-icon>Delete
          </v-btn>
        </div>
      </v-container>
    </v-navigation-drawer>
    <!-- Delete Dialog -->
    <v-dialog
      v-model="deleteProjectDialog"
      persistent
      class="mx-auto"
      width="600"
      dark
    >
      <v-card color="tabbody" shaped>
        <v-card-text class="headline pt-10">
          <span class="ml-12">Do you want to remove the project?</span>
        </v-card-text>
        <v-card-actions class="ml-10 pb-10 pt-10">
          <v-btn width="250" outlined color="error" @click="deleteProject()"
            >Yes</v-btn
          >
          <v-btn
            width="250"
            outlined
            color="primary"
            @click="deleteProjectDialog = false"
            >No</v-btn
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import ProfileAvatar from "@/components/Profile/ProfileAvatar.vue";
import ProfileTooltip from "@/components/Profile/ProfileTooltip.vue";
import AssignedUserManagement from "@/components/AssignedUserManagement.vue";
import { mapActions, mapGetters } from "vuex";
import { mapFields } from "vuex-map-fields";
export default {
  name: "TheDetailProject",
  data: () => ({
    tab: null,
    calendar1menu: false,
    calendar2menu: false,
    deleteProjectDialog: false,
    userManagementDialog: false,
    isFormValid: null,
    templateProjectItems: [],
    selectedProjectTemplate: null,
    completedSprints: 0,
    projectNamedStatus: "Active",
    //localProject: {},
    rules: {
      required: value => !!value || "Required",
      maxCharacter: value => value.length <= 50 || "Max 50 characters",
      duration: value => {
        const pattern = /^([0-9]{1,3})$/;
        return pattern.test(value) || "Invalid Duration";
      }
    }
  }),
  components: {
    ProfileAvatar,
    ProfileTooltip,
    AssignedUserManagement
  },
  methods: {
    ...mapActions("project", {
      updateProject: "update",
      destroyProject: "destroy",
      createProject: "create",
      fetchSingleProject: "fetchSingle",
      fetchProjects: "fetchList"
    }),

    ...mapActions("projectUser", {
      fetchProjectUser: "fetchList",
      createProjectUser: "create",
      destroyProjectUser: "destroy"
    }),
    ...mapActions("projectRole", {
      fetchProjectRoles: "fetchList"
    }),
    ...mapActions("user", {
      fetchPlattformUsers: "fetchList"
    }),

    close() {
      this.$store.commit("selected/hideProjectDetail");
    },

    confirm() {
      this.saveProject();
      this.$store.commit("selected/hideProjectDetail");
    },

    addProjectUser(projectUserId) {
      console.log(projectUserId)
      this.createProjectUser({
        data: {
          plattform_user: projectUserId,
          // Standard role developer
          role: 3,
          project: this.id
        }
      })
        .then(value => {
          console.log(value)
          this.fetchSingleProject({ id: this.id,
              customUrlFnArgs: {} }).then(res => {
                this.$store.commit("selected/setProjectDetail", res.data);
          })
          return value;
        })
        .catch(error => {
          console.log(error)
          if (error.response.data.non_field_errors.length > 0) {
            this.$store.commit("showSystemAlert", {
              message:
                error.response.data.non_field_errors[
                  error.response.data.non_field_errors.length - 1
                ],
              category: "error"
            });
          }
        });
    },

    addProject() {
      this.createProject({
        data: {
          name: this.name,
          description: this.description,
          start: this.start,
          end: this.end,
          sprint_duration: this.sprint_duration,
          dor: this.dor,
          dod: this.dod,
          status: this.GetProjectStatus(this.projectNamedStatus),
          project_users: this.project_users,
          is_template: this.is_template
        },
        customUrlFnArgs: { templateId: this.selectedProjectTemplate.id }
      })
      .then(
        () => {
          this.fetchProjects({ customUrlFnArgs: {} });
          this.$store.commit("selected/hideProjectDetail");
          this.$store.commit("showSystemAlert", {
            message: "Create " + this.name,
            category: "info"
          });
        }
      );

      
    },

    GetProjectStatus(namedStatus) {
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

    GetProjectNamedStatus(status) {
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

    saveProject() {
      this.updateProject({
        id: this.id,
        data: {
          id: this.id,
          name: this.name,
          description: this.description,
          status: this.GetProjectStatus(this.projectNamedStatus),
          dor: this.dor,
          dod: this.dod,
          project_users: this.project_users,
          is_template: this.is_template
        },
        customUrlFnArgs: {}
      });
    },

    deleteProject() {
      this.deleteProjectDialog = false;
      this.destroyProject({
        id: this.id,
        customUrlFnArgs: {}
      });
      this.$store.commit("showSystemAlert", {
        message: "Delete Project " + this.name,
        category: "info"
      });
      this.close();
    },

    deleteProjectUser(projectUserId) {
      this.destroyProjectUser({ id: projectUserId }).then(() => {
        this.fetchSingleProject({ id: this.id, customUrlFnArgs: {} }).then(res => {
          this.$store.commit("selected/setProjectDetail", res.data);
        });
      });
    }
  },
  computed: {
    ...mapGetters("projectUser", {
      listProjectUsers: "list",
      projectUserById: "byId",
      projectUsersByIdArray: "byIdArray",
      projectUsersbyIdArrayWithDetails: "byIdArrayWithDetails"
    }),
    ...mapGetters("projectRole", {
      listProjectRoles: "list",
      projectRoleById: "byId"
    }),
    ...mapGetters("user", {
      listPlattfromUsers: "list",
      plattformUserById: "byId"
    }),
    ...mapGetters("project", {
      listTemplateProjects: "byTemplates"
    }),

    allAssignedUsers() {
      return this.projectUsersbyIdArrayWithDetails(
        this.project_users
      );
    },

    visibleDrawer: {
      get() {
        return this.visableDetail;
      },
      set(value) {
        if (value) {
          this.$store.commit("selected/showProjectDetail");
        } else {
          this.$store.commit("selected/hideProjectDetail");
        }
      }
    },

    // See more under Two-way Computed Property https://vuex.vuejs.org/guide/forms.html
    // Implementation with https://github.com/maoberlehner/vuex-map-fields
    ...mapFields("selected", [
      "project.details.id",
      "project.details.status",
      "project.details.name",
      "project.details.dod",
      "project.details.dor",
      "project.details.start",
      "project.details.end",
      "project.details.description",
      "project.details.sprint_duration",
      "project.details.is_template",
      "project.details.project_users",
      "project.visableDetail",
      "project.visableCreate",
    ])


  },
  watch: {
    visibleDrawer(val, prev) {
      if (val === prev) return;
      this.templateProjectItems = this.listTemplateProjects();
      this.projectNamedStatus = this.GetProjectNamedStatus(this.status);
    },
  },

  created() {
    this.fetchProjectUser();
    this.fetchProjectRoles();
  }
};
</script>

<style lang="css" scoped>
  @import "../main.css";
  @import "./Profile/profile.css";
</style>