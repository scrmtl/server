/* eslint-disable prettier/prettier */
<template>
  <v-content class="tabbody tab-content">
    <v-card width="400" class="mx-auto mt-10">
      <v-card-title>
        <h1 class="display-1">Login</h1>
      </v-card-title>
      <v-card-text>
        <v-form>
          <v-text-field label="Username" prepend-icon="mdi-account-circle" />
          <v-text-field
            label="Password"
            :type="showPassword ? 'text' : 'password'"
            prepend-icon="mdi-lock"
            :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
            @click:append="showPassword = !showPassword"
          />
        </v-form>
      </v-card-text>
      <v-divider></v-divider>
      <v-card-actions>
        <v-btn color="success">Register</v-btn>
        <v-spacer></v-spacer>
        <router-link :to="{name:'home'}">
          <v-btn color="info">Login</v-btn>
        </router-link>
      </v-card-actions>
    </v-card>
  </v-content>
</template>

<script>
export default {
  data: () => ({
    showPassword: false
  })
};
</script>

<style lang="css" scoped>
@import "../main.css";

</style>