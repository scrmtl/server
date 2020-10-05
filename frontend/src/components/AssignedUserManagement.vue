<template>
  <v-dialog
    v-model="dialog"
    scrollable  
    persistent
    max-width="1200"
    transition="dialog-transition"
  >
    <v-card color="tabbody" dark>
      <v-card-title> {{dialogName}} </v-card-title>
      <v-card-text>
        <v-data-table
          :headers="headers"
          :items="assignedUsers"
          sort-by="username"
          no-data-text="No user assigned"
          class="tabbody"
          dark
        >
          <template v-slot:[`item.group`]="{ item }">
            <v-select
              :items="availableRoles"
              :value="item.role.name"
              @change="updateRole($event, item)"
            ></v-select>
          </template>
          <template v-slot:[`item.actions`]="{item}">
            <v-icon
              small
              @click="removeAssignedUser(item)"
            >
              mdi-delete
            </v-icon>
          </template>
        </v-data-table>
        
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn 
          color="link" 
          outlined 
          small 
          @click="close">
          CLOSE
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapGetters, mapActions } from 'vuex';
export default {
  name: "AssignedUserManagement",
  props: {
    dialog: { type: Boolean, default: false },
    dialogName: { type: String, default: "Assigned user" },
    color: { type: String, default: ""},
    assignedUsers: Array
  },
  data: () => ({
    headers: [
      { text: "Benutzername", value: "username" },
      { text: "Name", value: "name" },
      { text: "Role", value: "role" },
      { text: "Actions", value: "actions", sortable: false }
    ],
    availableRoles: []
  }),

  methods:{
    ...mapActions("projectUser", {
      fetchUser: "fetchList",
      updateProjectUser: "update"
    }),
    ...mapActions("projectRole", {
      fetchRoles: "fetchList"
    }),
    
    close() {
      this.$emit("close-dialog");
    },
    removeAssignedUser(user){
      this.$emit("remove-user", user);
    },
    addAssignedUser(user){
      this.$emit("add-user", user);
    },
    updateRole(newRole, item) {
      this.updateProjectUser({
        id: item.id,
        data: { role: [this.byRoleName(newRole)] }
      });
    },
  },
  computed:{
    ...mapGetters("projectRole",{
        byRoleName: "byName"
    })
  }
}
</script>

<style lang="css" scoped>
  @import "../main.css";
</style>