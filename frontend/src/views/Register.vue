<template>
  <v-container fluid>
    <v-row ro no-gutters align="center" justify="center">
      <v-col cols="4">
        <v-card class="ma-4">
          <v-card-title>
            <h1>Sign In</h1>
          </v-card-title>
          <v-card-text>
            <v-form ref="form" v-model="isFormVaild">
              <v-text-field
                label="E-Mail Adresse *"
                v-model="eMail"
              ></v-text-field>
              <v-text-field
                label="E-Mail Adresse wiederholen *"
                v-model="eMail_repeat"
              ></v-text-field>
              <v-text-field
                label="Gewünschter Benutzername"
                v-model="username"
              ></v-text-field>
              <v-text-field
                label="Passwort *"
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                prepend-icon="mdi-lock"
                :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append="showPassword = !showPassword"
              ></v-text-field>
              <v-text-field
                label="Passwort wiederholen *"
                v-model="password_repeat"
                :type="showPassword_repeat ? 'text' : 'password'"
                prepend-icon="mdi-lock"
                :append-icon="showPassword_repeat ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append="showPassword_repeat = !showPassword_repeat"
              ></v-text-field>
            </v-form>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
            <v-btn color="success">Register</v-btn>
            <v-spacer></v-spacer>
            <v-btn :disabled="!isFormVaild" color="info" @click="login()"
              >Login</v-btn
            >
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-snackbar v-model="isLoginError">{{ errorMessage }}</v-snackbar>
    </v-row>
  </v-container>
</template>
<script>
import { mapGetters } from "vuex";

export default {
  data() {
    return {
      isFormVaild: null,
      isLoginError: false,
      showPassword: false,
      showPassword_repeat: false,
      username: "",
      password: "",
      eMail: "",
      eMail_repeat: "",
      password_repeat: "",
      errorMessage: "Username or password is invalid",
      usernameRules: [
        v => !!v || "Name is required",
        v => (v && v.length <= 150) || "Name must be less than 150 characters",
        v => (v || "").indexOf(" ") < 0 || "No spaces are allowed"
      ],
      passwordRules: [v => !!v || "password is required"]
    };
  },
  methods: {
    login() {
      this.isLoginError = false;
      const credentials = {
        username: this.username,
        password: this.password
      };
      this.$store
        .dispatch("login", credentials)
        .then(() => this.$router.push("/"))
        .catch(err => {
          console.log(err);
          this.isLoginError = true;
        });
    }
  },
  computed: {
    ...mapGetters(["authStatus", "isLoggedIn"])
  },

  created: function() {
    this.eMail = "";
    this.eMail_repeat = "";
    this.username = "";
    this.password = "";
    this.password_repeat = "";
  }
};
</script>

<style lang="css" scoped>
@import "../main.css";
</style>