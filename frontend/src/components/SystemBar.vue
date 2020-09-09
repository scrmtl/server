<template>
  <v-system-bar color="appbar" dark absolute class="systemBar">
    <router-link :to="{name: 'Home'}" style="text-decoration: none; color: inherit;">
      <span class="link--text">
        <v-icon size="25" color="link">mdi-home</v-icon>ScrumTool
      </span>
    </router-link>
    <v-dialog v-model="dialog" width="1200">
      <template v-slot:activator="{ on, attrs }">
        <v-btn
          color="link"
          text
          x-small
          dark
          v-bind="attrs"
          v-on="on"
          class="ml-4"
        >Benutzerverwaltung</v-btn>
      </template>

      <v-card color="navbar" dark flat>
        <v-card-title class="headline">Benutzerverwaltung</v-card-title>
        <v-divider></v-divider>
        <v-card-text>
          <v-data-table
            :headers="headers"
            :items="projectUsers"
            sort-by="calories"
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
          <v-btn color="link" class="mr-2" outlined @click="createUser = false" small>SPEICHERN</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-spacer></v-spacer>
    <v-icon class="systemBarIcon">mdi-account</v-icon>
    <span class="systemBarUser">{{userinfos.username}}</span>
    <v-btn icon text @click="logout()">
      <v-tooltip bottom color="link">
        <template v-slot:activator="{ on, attrs }">
          <v-icon class="task-status-icons" color="link" v-bind="attrs" v-on="on">mdi-logout</v-icon>
        </template>
        <span>Logout</span>
      </v-tooltip>
    </v-btn>
  </v-system-bar>
</template>

<script>
import { mapState, mapActions, mapGetters } from "vuex";

export default {
  data() {
    return {
      user: "",
      dialog: false,
      createUser: false,
      formTitle: "Benutzer Form",
      headers: [
        { text: "Benutzername", value: "username" },
        { text: "E-Mail", value: "email" },
        { text: "Name", value: "name" }
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
    };
  },
  methods: {
    logout() {
      this.$store.dispatch("logout");
      this.$router.push("/login");
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
    initialize() {
      this.fetchUser();
      console.log("Projekt Benutzer" + this.projectUsers);
    },
    ...mapActions("registration", {
      registerUser: "create"
    }),
    ...mapActions("users", {
      fetchUser: "fetchList"
    })
  },

  computed: {
    ...mapState({
      userinfos: "Userinfo"
    }),
    ...mapGetters("user", {
      projectUsers: "list"
    })
  }
};
</script>

<style lang="css" scoped>
@import "../main.css";
</style>