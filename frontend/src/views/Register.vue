<template>
  <v-container fluid>
    <v-row no-gutters align="center" justify="center">
      <span class="text-lg-h1 text-sm-h2 white--text">Welcome to scrmtl</span>
    </v-row>
    <v-row no-gutters align="center" justify="center">
      <span class="text-lg-subtitle-1 text-sm-subtitle-2 white--text">dark, cool and easy</span>
    </v-row>
    <v-row ro no-gutters align="center" justify="center">
      <v-col sm="12" lg="5">
        <v-card class="ma-4">
          <v-card-title>
            <h1>Register</h1>
          </v-card-title>
          <v-card-text>
            <v-form ref="form" v-model="isFormVaild">
              <v-text-field label="Your name" v-model="name"> </v-text-field>
              <v-text-field
                label="E-Mail Adress *"
                v-model="eMail"
              ></v-text-field>
              <v-text-field
                label="Repeat E-Mail Adress *"
                v-model="eMail_repeat"
              ></v-text-field>
              <v-text-field label="Username" v-model="username"></v-text-field>
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
            <v-btn @click="back()">BACK</v-btn>
            <v-spacer></v-spacer>
            <v-btn :disabled="!isFormVaild" color="info" @click="register()"
              >register</v-btn
            >
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-snackbar v-model="isRegisterError">{{ errorMessage }}</v-snackbar>
    </v-row>
  </v-container>
</template>
<script>
import { mapGetters, mapActions } from "vuex";
import Axios from "axios";

export default {
  data() {
    return {
      isFormVaild: null,
      isRegisterError: false,
      showPassword: false,
      showPassword_repeat: false,
      name: "",
      username: "",
      password: "",
      eMail: "",
      eMail_repeat: "",
      password_repeat: "",
      errorHappend: false,
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
    ...mapActions("registration", {
      registerUser: "create"
    }),

    register() {
        this.errorHappend = false;
      if (this.eMail == this.eMail_repeat) {
        if (this.password == this.password_repeat) {
          this.registerUser({
            data: {
              name: this.name,
              email: this.eMail,
              username: this.username,
              password1: this.password,
              password2: this.password_repeat
            }
          }).catch(err => {
            if (err.response === undefined) {
              this.errorHappend = false;
            } else {
              console.log(err.response.status);
              console.log(err.response.data);
              this.errorHappend = true;
              if (err.response.data.email === undefined) {
                if (err.response.data.password1 === undefined) {
                  if (err.response.data.username === undefined) {
                    this.errorHappend = false;
                  } else {
                    this.errorMessage = err.response.data.username[0];
                    this.isRegisterError = true;
                  }
                } else {
                  this.errorMessage = err.response.data.password1[0];
                  this.isRegisterError = true;
                }
              } else {
                this.errorMessage = err.response.data.email[0];
                this.isRegisterError = true;
              }
            }
            if (this.errorHappend == false) {
              this.$router.push("/login");
            }
          });
        } else {
          this.errorMessage = "Password does not macht";
          this.isRegisterError = true;
        }
      } else {
        this.errorMessage = "E-Mail Adress does not match";
        this.isRegisterError = true;
      }
    },

    back() {
      this.$router.push("/login");
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
    Axios.interceptors.request.use(config => {
      if (
        (config.method === "post") | (config.method === "patch") &&
        config.url[config.url.length - 1] !== "/"
      ) {
        config.url += "/";
      }
      return config;
    });
  }
};
</script>

<style lang="css" scoped>
@import "../main.css";
</style>