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
          <template v-slot:top>
            <v-row >
              <v-col>
                <v-autocomplete
                  outlined
                  dense
                  label="Search User"
                  v-model="selectedUser"
                  :items="availableUsers"
                  :filter="nameUsernameFilter"
                  clearable
                >
                  <template v-slot:item="data">
                    <v-list-item-avatar>
                      <ProfileAvatar :avatar="data.item"/>
                    </v-list-item-avatar>
                    <v-list-item-content>
                      <v-list-item-title v-html="data.item.username"></v-list-item-title>
                      <v-list-item-subtitle v-html="data.item.name"></v-list-item-subtitle>
                    </v-list-item-content>
                  </template>
                </v-autocomplete>
              </v-col>
              
              <v-col>
                <v-btn 
                  outlined 
                  color="link"
                  text
                  
                >
                  <v-icon left>mdi-plus-circle-outline</v-icon>Add User/s
                </v-btn>
              </v-col>
            </v-row>
            
            
          </template>
          <template v-slot:[`item.role`]="{ item }">
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
    assignedUsers: Array,
    roleEditing: { type: Boolean, default: false },
  },
  data: () => ({
    headers: [
      { text: "Benutzername", value: "plattform_user.username" },
      { text: "Name", value: "plattform_user.name" },
      { text: "Role", value: "role.role_name" },
      { text: "Actions", value: "actions", sortable: false }
    ],
    availableRoles: [],
    availableUsers: [],
    selectedUser: [],
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
        data: { role: this.byRoleName(newRole) }
      });
    },

    nameUsernameFilter (item, queryText, itemText) {
        const textOne = item.name.toLowerCase()
        const textTwo = item.username.toLowerCase()
        const searchText = queryText.toLowerCase()
        console.log(itemText);
        return textOne.indexOf(searchText) > -1 ||
          textTwo.indexOf(searchText) > -1
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