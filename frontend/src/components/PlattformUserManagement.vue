<template>
  <v-dialog persistent scrollable v-model="dialog" max-width="1500">
    <v-card color="tabbody" dark flat>
      <v-card-title class="headline">Plattform user management</v-card-title>
      <v-divider></v-divider>
        <v-card-text>
          
        
        <v-data-table
          :headers="headers"
          :items="allUserInfo()"
          sort-by="username"
          class="tabbody"
          
        >
          <template v-slot:[`item.group`]="{ item }">
            <v-select
              :items="groupNames"
              :value="item.group.name"
              @change="updateGroup($event, item)"
            ></v-select>
          </template>
          <template v-slot:top>
            <v-toolbar flat color="tabbody">
              <v-dialog v-model="createUser" persistent max-width="1200">
                <template v-slot:activator="{ on, attrs }">
                  <v-spacer></v-spacer>
                  <v-btn
                    color="link"
                    class="mb-2"
                    v-bind="attrs"
                    v-on="on"
                    small
                    outlined
                    >add user
                  </v-btn>
                </template>
                <!-- Add plttform user dialog -->
                <v-card class="tabbody" dark >
                  <v-card-title>
                    <span class="headline">Add new plattform user</span>
                  </v-card-title>

                  <v-card-text>
                    <v-row>
                      <v-col cols="12" sm="6" md="4">
                        <v-text-field
                          v-model="editedItem.username"
                          label="Benutzername"
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" sm="6" md="4">
                        <v-text-field
                          v-model="editedItem.email"
                          label="E-Mail"
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" sm="6" md="4">
                        <v-text-field
                          v-model="editedItem.name"
                          label="Name"
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" sm="6" md="4">
                        <v-text-field
                          v-model="editedItem.password"
                          label="Passwort"
                          :rules="passwordRules"
                          :type="showPassword ? 'text' : 'password'"
                          prepend-icon="mdi-lock"
                          :append-icon="
                            showPassword ? 'mdi-eye' : 'mdi-eye-off'
                          "
                          @click:append="showPassword = !showPassword"
                          @keydown.enter="login()"
                          required
                        ></v-text-field>
                      </v-col>
                      <v-col cols="12" sm="6" md="4">
                        <v-text-field
                          v-model="editedItem.repeated_password"
                          label="Passwort wiederholen"
                          :rules="passwordRules"
                          :type="showPassword ? 'text' : 'password'"
                          prepend-icon="mdi-lock"
                          :append-icon="
                            showPassword ? 'mdi-eye' : 'mdi-eye-off'
                          "
                          @click:append="showPassword = !showPassword"
                          @keydown.enter="login()"
                          required
                        ></v-text-field>
                      </v-col>
                    </v-row>
                  </v-card-text>

                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="link" text v-on:click="createUser = false"
                      >CANCEL</v-btn
                    >
                    <v-btn color="link" text v-on:click="saveUser"
                      >SAVE</v-btn
                    >
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </v-toolbar>
          </template>
          <template v-slot:actions="{ item }">
            <v-icon small class="mr-2" @click="editItem(item)"
              >mdi-pencil</v-icon
            >
            <v-icon small @click="deleteItem(item)">mdi-delete</v-icon>
          </template>
          <template v-slot:no-data>
            <v-btn color="link" @click="fetchAll">RESET</v-btn>
          </template>
        </v-data-table>
      </v-card-text>
      <v-divider></v-divider>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="link" class="mr-2" outlined small @click="close"
          >CLOSE
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex";
export default {
  name: "PlattformUserManagement",
  props: {
    dialog: { type: Boolean, default: false },
  },
  created() {
    this.fetchAll();
  },
  data: () => ({
    fetchErrors: [],
    user: "",
    groupNames: [],
    showPassword: false,
    passwordRules: [v => !!v || "password is required"],
    createUser: false,
    headers: [
      { text: "User name", value: "username" },
      { text: "E-Mail", value: "email" },
      { text: "Name", value: "name" },
      { text: "Projects", value: "project" },
      { text: "Rights", value: "group", sortable: false }
    ],
    editedIndex: -1,
    editedItem: {
      name: "",
      email: "",
      username: "",
      password: "",
      repeated_password: ""
    },
    defaultItem: {
      name: "Max Mustermann",
      email: "Max.Mustermann@mail.com",
      username: "maxMuster"
    }
  }),
  methods: {
    ...mapActions("registration", {
      registerUser: "create"
    }),
    ...mapActions("user", {
      fetchUser: "fetchList",
      updateUser: "update"
    }),
    ...mapActions("group", {
      fetchGroups: "fetchList"
    }),
    fetchAll() {
      this.fetchUser().catch(error => {
        this.fetchErrors.push(error);
      });
      this.fetchGroups()
        .catch(error => {
          this.fetchErrors.push(error);
        })
        .then(() => {
          var listgroupsvalues = [];
          this.listGroups.forEach(group => {
            listgroupsvalues.push(group.name);
          });
          this.groupNames = listgroupsvalues;
        });
    },
    updateGroup(newGroup, item) {
      this.updateUser({
        id: item.id,
        data: { groups: [this.byGroupName(newGroup)] }
      }).then(() => this.fetchAll());
    },
    saveUser() {
      this.registerUser({
        data: {
          name: this.editedItem.name,
          email: this.editedItem.email,
          username: this.editedItem.username,
          password1: this.editedItem.password,
          password2: this.editedItem.repeated_password
        }
      }).then(() => this.fetchAll());
      let setAll = (obj, val) => Object.keys(obj).forEach(k => (obj[k] = val));
      setAll(this.editedItem, "");
      this.createUser = false;
    },
    close() {
      this.$emit("close-dialog");
    },
    allUserInfo() {
      var data = [];
      var groupId;
      Object.values(this.listPlatformUsers).forEach(pUser => {
        groupId = Object.values(pUser.groups).shift();
        if (!(groupId === undefined)) {
          var group = this.groupById(groupId);
          data.push({
            name: pUser.name,
            email: pUser.email,
            username: pUser.username,
            group: group,
            id: pUser.id
          });
        } else {
          this.fetchErrors.push("undefined groupId");
        }
      });
      return data;
    }
  },
  computed: {
    ...mapState({
      userinfos: "Userinfo"
    }),
    ...mapGetters("user", {
      listPlatformUsers: "list"
    }),
    ...mapGetters("group", {
      groupById: "byId",
      listGroups: "list",
      byGroupName: "byName"
    })
  }
};
</script>

<style lang="css">
@import "../main.css";
</style>
    