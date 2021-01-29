<template>
  <v-list color="accent">
    <v-list-item>
      <v-list-item-avatar>
        <ProfileAvatar :avatar="avatar" size="32px" />
      </v-list-item-avatar>
      <v-list-item-content>
        <v-list-item-title>{{
          avatar.plattform_user.username
        }}</v-list-item-title>
        <v-list-item-subtitle v-if="avatar.role.role_name">{{
          avatar.role.role_name
        }}</v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>
    <v-divider></v-divider>
    <v-list-item>
      <v-list-item-content>
        <v-list-item-subtitle>{{
          avatar.plattform_user.name
        }}</v-list-item-subtitle>
        <v-list-item-subtitle>{{
          avatar.plattform_user.email
        }}</v-list-item-subtitle>
      </v-list-item-content>
    </v-list-item>
  </v-list>
</template>
<script>
import ProfileAvatar from "@/components/Profile/ProfileAvatar.vue";
export default {
  props: {
    avatar: {
      default: () => {},
      type: Object,
    },
  },
  components: {
    ProfileAvatar,
  },
};
</script>
<style lang="css" scoped>
@import "./profile.css";
</style>
