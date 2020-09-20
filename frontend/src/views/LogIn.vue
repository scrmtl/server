<template>
  <div class="tabbody tab-content" >
    <v-row>
      <v-card width="400" class="mx-auto mt-10" @submit.prevent="register">
        <v-card-title>
          <h1 class="display-1">Sign In</h1>
        </v-card-title>
        <v-card-text>
          <v-form>
            <v-text-field
              label="Username"
              v-model="username"
              prepend-icon="mdi-account-circle"
              @keydown.enter="login()"
            />
            <v-text-field
              label="Password"
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              prepend-icon="mdi-lock"
              :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
              @click:append="showPassword = !showPassword"
              @keydown.enter="login()"
              value
              name="password"
            />
          </v-form>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-btn color="success">Register</v-btn>
          <v-spacer></v-spacer>
          <v-btn color="info" @click.native="login()">Login</v-btn>
        </v-card-actions>
      </v-card>
    </v-row>
    <v-row>
      <v-snackbar v-model="loginFalse">{{ bentuzerausgabe }}</v-snackbar>
    </v-row>
  </div>
</template>

<script>
import AuthService from "@/services/AuthService.js";

export default {
  data() {
    return {
      showPassword: false,
      loginFalse: false,
      username: "",
      password: "",
      errorMessage: "", 
      bentuzerausgabe: "Benutzername oder Passwort ist falsch...", 
    };
  },
  methods:{
    async login() {
      try {
        const credentials = {
          username: this.username,
          password: this.password
        };
        const response = await AuthService.login(credentials);
        this.errorMessage = response.errorMessage;        
        const token = response.access_token;
        const user = this.username;
        this.$store.dispatch("login", { token, user });
        console.log(response);
        if (response.access_token !== "") {
          this.$router.push("/")
        } else {
          this.loginFalse = true;
        }
      } catch (error) {
        this.errorMessage = error.response.data.msg;
        this.loginFalse = true;
      }
    }
  }
};

</script>

<style lang="css" scoped>
@import "../main.css";
</style>