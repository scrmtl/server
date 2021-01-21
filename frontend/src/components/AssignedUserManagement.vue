<template>
  <v-dialog
    v-model="visibleDialog"
    scrollable
    persistent
    max-width="1200"
    transition="dialog-transition"
  >
    <v-card color="tabbody" dark>
      <v-card-title> {{ dialogName }} </v-card-title>
      <v-card-text>
        <v-data-table
          :headers="headers"
          :items="assignedUsers"
          sort-by="username"
          no-data-text="No user assigned"
          class="tabbody"
          dark
        >
          <template v-slot:top>
            <v-row>
              <v-col>
                <v-autocomplete
                  outlined
                  dense
                  label="Search User"
                  v-model="selectedUser"
                  :items="availableUsers"
                  :filter="nameUsernameFilter"
                  item-text="username"
                  item-value="id"
                  clearable
                  placeholder="Start typing to search user"
                >
                  <template v-slot:item="data">
                    <v-list-item-content>
                      <v-list-item-title
                        v-html="data.item.username"
                      ></v-list-item-title>
                      <v-list-item-subtitle
                        v-html="data.item.name"
                      ></v-list-item-subtitle>
                    </v-list-item-content>
                  </template>
                </v-autocomplete>
              </v-col>

              <v-col>
                <v-btn
                  outlined
                  color="link"
                  text
                  @click="addAssignedUser(selectedUser)"
                  :disabled="typeof selectedUser !== 'number'"
                >
                  <v-icon left>mdi-plus-circle-outline</v-icon>Add User/s
                </v-btn>
              </v-col>
            </v-row>
          </template>
          <template v-slot:[`item.role`]="{ item }">
            <v-select
              :items="availableRoles"
              :value="item.role.role_name"
              :readonly="!roleEditing"
              @change="updateRole($event, item)"
            ></v-select>
          </template>
          <template v-slot:[`item.actions`]="{ item }">
            <v-icon small @click="removeUser(item)">
              mdi-delete
            </v-icon>
          </template>
        </v-data-table>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="link" outlined small @click="close"> CLOSE </v-btn>
      </v-card-actions>
    </v-card>

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
          <span class="ml-12"
            >Remove the user form the project?</span
          >
        </v-card-text>
        <v-card-actions class="ml-10 pb-10 pt-10">
          <v-btn width="250" outlined color="error" @click="removeAssignedUser()"
            >Yes</v-btn
          >
          <v-btn width="250" outlined @click="deleteDialog = false">No</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-dialog>
</template>

<script>
import { mapGetters, mapActions } from "vuex";
export default {
  name: "AssignedUserManagement",
  props: {
    dialog: { type: Boolean, default: false },
    dialogName: { type: String, default: "Assigned user" },
    color: { type: String, default: "" },
    roleEditing: { type: Boolean, default: false },
    assignedUsers: { type: Array },
    availableUsers: { type: Array },
  },
  data: () => ({
    headers: [
      { text: "Benutzername", value: "plattform_user.username" },
      { text: "Name", value: "plattform_user.name" },
      { text: "Role", value: "role" },
      { text: "Actions", value: "actions", sortable: false },
    ],
    availableRoles: ["product owner", "developer", "scrum master"],
    selectedUser: {},
    deleteDialog: false,
    deleteUser: null,
  }),
  components: {},

  methods: {
    ...mapActions("projectUser", {
      fetchUser: "fetchList",
      updateProjectUser: "update",
    }),
    ...mapActions("projectRole", {
      fetchRoles: "fetchList",
    }),

    close() {
      this.$emit("close-dialog");
    },
    removeAssignedUser() {
      if (this.deleteUser !== null) {
        console.log(this.deleteUser.id);
        this.$emit("remove-user", this.deleteUser.id);
      }
    },
    addAssignedUser(user) {
      this.$emit("add-user", user);
      this.selectedUser = {};
    },
    updateRole(newRole, item) {
      this.updateProjectUser({
        id: item.id,
        data: { role: this.byRoleName(newRole) },
        customUrlFnArgs: {},
      });
    },
    nameUsernameFilter(item, queryText) {
      const textOne = item.name.toLowerCase();
      const textTwo = item.username.toLowerCase();
      const searchText = queryText.toLowerCase();
      return (
        textOne.indexOf(searchText) > -1 || textTwo.indexOf(searchText) > -1
      );
    },

    removeUser(user) {
      this.deleteUser = user;
      this.deleteDialog = true;
    },
  },
  computed: {
    ...mapGetters("projectRole", {
      byRoleName: "byName",
    }),
    visibleDialog: {
      get() {
        return this.dialog;
      },
      set(newValue) {
        if (newValue) {
          return this.dialog;
        } else {
          this.$emit("close-dialog");
        }
      },
    },
  },
};
</script>

<style lang="css" scoped>
@import "../main.css";
</style>