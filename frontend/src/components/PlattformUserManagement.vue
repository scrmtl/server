<template>
    <v-dialog v-model="value" width="1200">
    <v-card color="navbar" dark flat>
        <v-card-title class="headline">Benutzerverwaltung</v-card-title>
        <v-divider></v-divider>
        <v-card-text>
          <v-data-table
            :headers="headers"
            :items="allUserInfo()"
            sort-by="username"
            class="elevation-1"
          >
            <template v-slot:top>
              <v-toolbar flat color="navbar">
                <v-dialog v-model="createUser" max-width="700px">
                  <template v-slot:activator="{ on, attrs }">
                    <v-spacer></v-spacer>
                    <v-btn
                      color="link"
                      class="mb-2"
                      v-bind="attrs"
                      v-on="on"
                      small
                      outlined
                    >Benutzer hinzufügen</v-btn>
                  </template>
                  <v-card>
                    <v-card-title>
                      <span class="headline">{{ formTitle }}</span>
                    </v-card-title>

                    <v-card-text>
                      <v-row>
                        <v-col cols="12" sm="6" md="4">
                          <v-text-field v-model="editedItem.username" label="Benutzername"></v-text-field>
                        </v-col>
                        <v-col cols="12" sm="6" md="4">
                          <v-text-field v-model="editedItem.email" label="E-Mail"></v-text-field>
                        </v-col>
                        <v-col cols="12" sm="6" md="4">
                          <v-text-field v-model="editedItem.name" label="Name"></v-text-field>
                        </v-col>
                        <v-col cols="12" sm="6" md="4">
                          <v-text-field v-model="editedItem.password" label="Passwort"></v-text-field>
                        </v-col>
                        <v-col cols="12" sm="6" md="4">
                          <v-text-field
                            v-model="editedItem.repeated_password"
                            label="Passwort wiederholen"
                          ></v-text-field>
                        </v-col>
                      </v-row>
                    </v-card-text>

                    <v-card-actions>
                      <v-spacer></v-spacer>
                      <v-btn color="link" text v-on:click="createUser = false">ABBRECHEN</v-btn>
                      <v-btn color="link" text v-on:click="saveUser">SPEICHERN</v-btn>
                    </v-card-actions>
                  </v-card>
                </v-dialog>
              </v-toolbar>
            </template>
            <template v-slot:actions="{ item }">
              <v-icon small class="mr-2" @click="editItem(item)">mdi-pencil</v-icon>
              <v-icon small @click="deleteItem(item)">mdi-delete</v-icon>
            </template>
            <template v-slot:no-data>
              <v-btn color="link" @click="initialize">ZURÜCKSETZEN</v-btn>
            </template>
          </v-data-table>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="link" class="mr-2" outlined @click.stop="close()" small>CLOSE</v-btn>
        </v-card-actions>
    </v-card>
    </v-dialog>
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex";
export default {
    name: "PlattformUserManagement",
    props: {
      value: Boolean, 
    },
    data: () => ({
        user: "",
        createUser: false,
        formTitle: "Benutzer Form",
        headers: [
        { text: "Benutzername", value: "username" },
        { text: "E-Mail", value: "email" },
        { text: "Name", value: "name" },
        { text: "Gruppe", value: "group" }
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
    methods:{
        ...mapActions("registration", {
            registerUser: "create"
        }),
        ...mapActions("user", {
            fetchUser: "fetchList"
        }),
        ...mapActions("group", {
            fetchGroups: "fetchList"
        }),
        initialize() {
            this.fetchUser();
            console.log("Projekt Benutzer" + this.listPlatformUsers);
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
            });
        },
        close() {
          this.$emit('input', false);
        },
        allUserInfo() {
            var data = [];
            // TODO Bug on fetchGroup Error Handling
            // var groupId;
            // Object.values(this.listPlatformUsers).forEach(
            //   pUser => {
            //     groupId = Object.values(pUser.groups).shift();
            //     data.push({
            //         name: pUser.name,
            //         email: pUser.email,
            //         username: pUser.username,
            //         group: this.groupById(groupId).catch(() => this.fetchGroups()).name
            //     });
            //   });

            // try {
            //     Object.values(this.listPlatformUsers).forEach(pUser => {
            //     groupId = Object.values(pUser.groups).shift();
            //     data.push({
            //         name: pUser.name,
            //         email: pUser.email,
            //         username: pUser.username,
            //         group: this.groupById(groupId).name
            //     });
            //     });
            // } catch (error) {
            //     if (groupId === undefined) {
            //       //this.fetchGroups();
            //     }
            // }
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
        groupById: "byId"
        }),
        ...mapGetters("group", {
        listGroups: "list"
        }),
    }
}
</script>

<style lang="css">
    @import "../main.css";
</style>
    