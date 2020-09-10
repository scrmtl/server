<template>
  
    <v-list dark>
      <v-list-item>
        <v-list-item-avatar>
          <ProfileAvatar :avatar="avatar" custom-class="bordered small" size="32px"/>
        </v-list-item-avatar>
        <v-list-item-content>
          <v-list-item-title>{{ avatar.name }}</v-list-item-title>
          <v-list-item-subtitle>Rolle</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-divider></v-divider>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-subtitle>{{ avatar.username }}</v-list-item-subtitle>
          <v-list-item-subtitle>{{ avatar.email }}</v-list-item-subtitle>

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
      type: Object
    }
  },
  components: {
    ProfileAvatar,
  },
  
}
</script>
<style lang="css" scoped>
@import './profile.css';
</style>