<template>
    <v-avatar :class="(customClass) ? customClass : ''" :color="(!avatar.img) ? GetColour(avatar.username) : null" :size="size">
      <slot></slot>
      <img
        v-if="avatar.img"
        :src="avatar.img"
        :alt="avatar.username"
      >
      <span
        v-else
        class="white--text"
      >
        {{ GetInitials(avatar.username) }}
      </span>
    </v-avatar>
</template>

<script>
export default {
  props: {
    avatar: {
      default: () => {},
      type: Object
    },
    customClass: {
      default: '',
      type: String
    },
    size: {
      default: '48px',
      type: String
    }
  },
  
  methods: {
    GetColour (name) {
        var hash = 0;
        if (name.length === 0) return hash;
        for (var i = 0; i < name.length; i++) {
            hash = name.charCodeAt(i) + ((hash << 5) - hash);
            hash = hash & hash;
        }
        var color = '#'
        for (var j = 0; j < 3; j++) {
            var value = (hash >> (j * 8)) & 255;
            color += ('00' + value.toString(16)).substr(-2);
        }
        return color;
    },
    GetInitials (name) {
        var initials = "AA";
        initials = name.substring(0,2);
        return initials;
    }
  }
}
</script>
<style lang="css" scoped>
@import './profile.css';
</style>