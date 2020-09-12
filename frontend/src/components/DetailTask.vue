<template>
  <div>
    <v-navigation-drawer v-model="visibleDrawer" right fixed width="800" color="secondary" dark>
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
          <v-tab>Steps</v-tab>
        </v-tabs>
        <!-- Details Tab -->
        <v-tabs-items v-model="tab" background-color="secondary" color="secondary">
          <v-tab-item>
            <v-card flat dark color="secondary" tile>
              <v-card-title>
                <span class="headline ma-0 pa-1">Task</span>
              </v-card-title>
              <v-card-text>
                <v-form ref="form" v-model="isFormValid" lazy-validation>
                  <!-- Taskname -->
                  <v-text-field
                    label="Name"
                    required
                    :rules="TaskNameRules"
                    :counter="50"
                    prepend-icon="mdi-information-outline"
                    class="ma-1"
                    v-model="localTask.name"
                  ></v-text-field>
                  <v-textarea
                    label="Description"
                    prepend-icon="mdi-information-outline"
                    outlined
                    height="70"
                    class="ma-1"
                    v-model="localTask.description"
                  ></v-textarea>
                  <v-chip-group column>
                    <v-chip
                      v-for="(label_item, i) in localTask.labels"
                      :key="i"
                      :color="label_item.color"
                      v-text="label_item.title"
                    ></v-chip>
                  </v-chip-group>
                </v-form>
              </v-card-text>
            </v-card>

            <v-card v-if="!this.selectedTask.visableCreate" flat dark color="secondary" tile>
              <v-card-title class="title">
                <span class="headline ma-4">Assigned users</span>
                <v-btn icon>
                  <v-icon color="link">mdi-dots-horizontal</v-icon>
                </v-btn>
              </v-card-title>
              <v-card-text>
                <section class="avatars-group grid pa-3">
                  <div
                    v-for="avatar in allAssignedUsers"
                    :key="`avatar-id-${avatar.id}`"
                    class="avatars-group__item"
                  >
                    <v-menu open-delay="1500" open-on-hover :nudge-width="200" offset-y>
                      <template v-slot:activator="{ on, attrs }">
                        <div v-bind="attrs" v-on="on">
                          <ProfileAvatar :avatar="avatar" />
                        </div>
                      </template>
                      <ProfileTooltip :avatar="avatar" />
                    </v-menu>
                  </div>
                </section>
              </v-card-text>
            </v-card>
          </v-tab-item>
          <!-- Step Tab -->
          <v-tab-item>
            <v-card flat dark color="secondary" tile>
              <v-list-item-group>
                <v-list-item v-for="steplist in selectedTask.details.steplists" :key="steplist">
                  <Steplist v-bind:steplistId="steplist" />
                </v-list-item>
              </v-list-item-group>
            </v-card>
          </v-tab-item>
        </v-tabs-items>
        <!-- actions -->
        <div>
          <v-btn color="link" text @click="close()">Close</v-btn>
          <v-btn v-if="!this.selectedTask.visableCreate" color="link" text @click="confirm()">Save</v-btn>
          <v-btn
            v-if="this.selectedTask.visableCreate"
            color="link"
            :disabled="!isFormValid"
            text
            @click="addTask()"
          >Create</v-btn>
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
    <v-dialog v-model="deleteDialog" persistent class="mx-auto" width="600" dark>
      <v-card color="tabbody" shaped>
        <v-card-text class="headline pt-10">
          <span class="ml-12">Möchten Sie den Task wirklich löschen?</span>
        </v-card-text>
        <v-card-actions class="ml-10 pb-10 pt-10">
          <v-btn width="250" outlined color="error" @click="deleteTask()">Ja</v-btn>
          <v-btn width="250" outlined color="primary" @click="deleteDialog = false">Nein</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>
<script>
import ProfileAvatar from "@/components/Profile/ProfileAvatar.vue";
import ProfileTooltip from "@/components/Profile/ProfileTooltip.vue";
import Steplist from "@/components/Steplist.vue";
import { mapActions, mapGetters, mapState } from "vuex";
export default {
  name: "DetailTask",
  data: () => ({
    tab: null,
    deleteDialog: false,
    taskNamedStatus: "New",
    localTask: {},
    projectNameRules: [
      v => !!v || "Name is required",
      v => (v && v.length <= 50) || "Name must be less than 50 characters"
    ]
  }),
  components: {
    ProfileAvatar,
    ProfileTooltip,
    Steplist
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

    addTask() {},

    saveTask() {},

    deleteTask() {},

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
      plattformUserById: "byId",
      plattformUsersByIdArray: "byIdArray"
    }),
    ...mapGetters("projectRole", {
      listProjectRoles: "list",
      projectRoleById: "byId"
    }),
    ...mapGetters("steplist", {
      steplistById: "byId"
    }),

    allAssignedUsers() {
      return this.plattformUsersByIdArray(this.localTask.assigned_users) &&
        this.plattformUsersByIdArray(this.localTask.assigned_users).length > 0
        ? this.plattformUsersByIdArray(
            this.localTask.assigned_users
          ).sort((a, b) => a.username.localeCompare(b.alt))
        : null;
    },

    visibleDrawer: {
      get() {
        return this.selectedTask.visableDetail;
      },
      set(newValue) {
        this.selectedTask.visableDetail = newValue;
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