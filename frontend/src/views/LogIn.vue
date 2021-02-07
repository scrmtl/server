<template>
  <v-container fluid>
    <v-row no-gutters align="center" justify="center">
      <v-img
        max-height="150"
        max-width="150"
        src="@/assets/logo_transparent.png"
      ></v-img>
      <span class="text-lg-h1 text-sm-h2 white--text">Welcome</span>
    </v-row>
    <v-row no-gutters align="center" justify="center">
      <span class="text-lg-subtitle-1 text-sm-subtitle-2 white--text"
        >dark, cool and easy</span
      >
    </v-row>
    <v-row no-gutters align="center" justify="center">
      <v-col sm="12" lg="5">
        <v-card class="ma-4">
          <v-card-title>
            <span class="text-lg-h4 text-sm-h3">Sign in</span>
          </v-card-title>
          <v-card-text>
            <v-form ref="form" v-model="isFormVaild">
              <v-text-field
                label="Username"
                :counter="150"
                v-model="username"
                :rules="usernameRules"
                prepend-icon="mdi-account-circle"
                @keydown.enter="login()"
                required
              />
              <v-text-field
                label="Password"
                v-model="password"
                :rules="passwordRules"
                :type="showPassword ? 'text' : 'password'"
                prepend-icon="mdi-lock"
                :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append="showPassword = !showPassword"
                @keydown.enter="login()"
                required
              />
            </v-form>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
            <v-btn color="success" @click="register()">Register</v-btn>
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
      username: "",
      password: "",
      errorMessage: "Username or password is invalid",
      usernameRules: [
        (v) => !!v || "Name is required",
        (v) =>
          (v && v.length <= 150) || "Name must be less than 150 characters",
        (v) => (v || "").indexOf(" ") < 0 || "No spaces are allowed",
      ],
      passwordRules: [(v) => !!v || "password is required"],
    };
  },
  methods: {
    login() {
      this.isLoginError = false;
      const credentials = {
        username: this.username,
        password: this.password,
      };
      this.$store
        .dispatch("login", credentials)
        .then(() => {
          this.goToHome();
        })
        .catch((err) => {
          console.log(err);
          this.isLoginError = true;
        });
    },
    goToHome() {
      this.$router.push({ name: "Home" });
    },

    register() {
      this.$router.push({ name: "Register" });
    },
  },
  computed: {
    ...mapGetters(["authStatus", "isLoggedIn"]),
  },
};
</script>

<style lang="css" scoped>
@import "../main.css";
</style>
