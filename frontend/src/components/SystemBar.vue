<template>
    <v-system-bar color="appbar" dark absolute class="systemBar">
        <v-icon>mdi-filter-variant</v-icon>
        <span>ScrumTool</span>
        <v-spacer></v-spacer>
        <span class="systemBarUser">{{username}}</span>
        <v-icon class="systemBarIcon">mdi-account</v-icon>   
    </v-system-bar>
</template>

<script>
import { mapState } from 'vuex';

    export default {
        data() {
            return {
                user: ''
            };
        },
        computed: mapState({
            username: state => state.Userinfo.username,
        })
    }
</script>

<style lang="css" scoped>
@import "../main.css";

</style>