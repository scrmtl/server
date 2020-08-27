/* eslint-disable */
<template>
  <v-content class="tabbody tab-content">
    <v-card width="400" class="mx-auto mt-10" @submit.prevent="register">
      <v-card-title>
        <h1 class="display-1">Registrieren</h1>
      </v-card-title>
      <v-card-text>
        <v-form>
          <v-text-field
            label="Username"
            v-model="Userinfo.username"
            prepend-icon="mdi-account-circle"
          />
          <v-text-field
            label="Password"
            v-model="Userinfo.password"
            :type="showPassword ? 'text' : 'password'"
            prepend-icon="mdi-lock"
            :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
            @click:append="showPassword = !showPassword"
            value
            name="password"
            v-mo#del="passoword"
          />
        </v-form>
      </v-card-text>
      <v-divider></v-divider>
      <v-card-actions>
        <v-btn color="success">Register</v-btn>
        <v-spacer></v-spacer>
        <!--<router-link :to="{name:'home'}">-->
        <v-btn color="info" @click="login()">Login</v-btn>
        <!--</router-link>-->
      </v-card-actions>
    </v-card>

    <v-snackbar v-model="loginFalse">{{ FailText }}</v-snackbar>
  </v-content>
</template>

<script>
import { mapState } from "vuex";
import { mapMutations } from "vuex";

export default {
  data: () => ({
    showPassword: false,

    Userinfo: {
      username: "",
      password: "",
    },

    loginFalse: false,
    FailText: "Nutzername oder Passwort falsch...\n"
  }),

  computed: {
    ...mapState({})
  },

  methods: {
    ...mapMutations(["setToken", "setUsername"]),

    login() {
      var axios = require("axios");
      axios
        .request({
          url: "https://scrmtl.ddns.net/o/token/",
          method: "post",
          auth: {
            username: "ttLwLjOKoJWtm5NDRRfGbgfioDhS7hwGZ0iaAzzD",
            password:
              "SPWysYuxLcr4ju0ITzqKASIQObiWaaUQbKb4ofYgJTv2QmkFSqfgroR3GIOg1QH41okgg0UHPh3gbTUiXuKKuj85Qy241hyBrn851v6eTVOpRujVWzZZP3npTki1Znnc"
          },
          data:
            "grant_type=password&username=" +
            this.Userinfo.username +
            "&password=" +
            this.Userinfo.password +
            "&scope=write"
        })
        .then(response => {
          console.log(response);
          this.token = response.data.access_token;
          //console.log(this.token);
          this.setToken(this.token);
          this.setUsername(this.Userinfo.username)
          console.log(this.$store.getters.getToken);
          if (response.status == 200) {
            this.$router.push("home");
          } else {
            this.loginFalse = true;
          }
        })
        .catch(error => {
          //Hier der Fehlerfall...
          if (error.response) {
            this.loginFalse = true;
          }
        });
    }
  }
};


</script>

<style lang="css" scoped>
@import "../main.css";
</style>