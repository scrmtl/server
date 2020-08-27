<template>
    <v-system-bar color="appbar" dark absolute class="systemBar">
        <v-icon>mdi-filter-variant</v-icon>
        <span>ScrumTool</span>
        <v-spacer></v-spacer>
        <span class="systemBarUser">{{Username}}</span>
        <v-icon class="systemBarIcon">mdi-account</v-icon>   
    </v-system-bar>
</template>

<script>
    import { mapState } from "vuex";
    export default {
        computed: {
        ...mapState({
            Username: "username"
        })
    },
    }
</script>

<style lang="css" scoped>
@import "../main.css";

</style>