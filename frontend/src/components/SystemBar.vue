<template>
    <v-system-bar color="appbar" dark absolute class="systemBar">
        <v-icon>mdi-filter-variant</v-icon>
        <span>ScrumTool</span>
        <v-dialog
            v-model="dialog"
            width="900"
            >
            <template v-slot:activator="{ on, attrs }">
                <v-btn
                color="link"
                outlined
                x-small
                dark
                v-bind="attrs"
                v-on="on"
                class="ml-10"
                >
                Benutzerverwaltung
                </v-btn>
            </template>

            <v-card color="lanbody">
                <v-card-title class="headline">
                Benutzerverwaltung
                </v-card-title>
                <v-divider></v-divider>

                <v-card-text>
                    <v-row>
                        <v-col cols="12" sm="6">
                            <v-text-field
                                label="Vorname"
                                prepend-icon="mdi-account-check"
                                required
                            ></v-text-field>
                            <v-text-field
                                label="Nachname"
                                prepend-icon="mdi-account-check"
                                required
                            ></v-text-field>
                        </v-col>
                        <v-col cols="12" sm="6">
                            <v-text-field
                                label="E-Mail"
                                prepend-icon="mdi-at"
                                required
                            ></v-text-field>
                            <v-text-field
                                label="Projektrolle"
                                prepend-icon="mdi-account-multiple-check"
                                required
                            ></v-text-field>
                        </v-col>
                    </v-row>
                    <v-row>
                        <v-spacer></v-spacer>
                        <v-btn
                            color="info"
                            outlined
                            small
                            class="mb-8 mr-2"
                        >
                            Benutzer anlegen
                        </v-btn>
                    </v-row>
                <v-divider></v-divider>
                table
                </v-card-text>
                <v-divider></v-divider>
                <v-card-actions>
                <v-spacer></v-spacer>
                    <v-btn
                        color="link"
                        class="mr-2"
                        outlined
                        @click="dialog = false"
                        small
                    >
                        Save
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-dialog>
        <v-spacer></v-spacer>
        <v-icon class="systemBarIcon">mdi-account</v-icon>
        <span class="systemBarUser">{{username}}</span>
        <v-btn
        text
        >
            <v-tooltip bottom color="link">
                <template v-slot:activator="{ on, attrs }">
                  <v-icon
                    class="task-status-icons"
                    color="link"
                    v-bind="attrs"
                    v-on="on"
                  >mdi-logout</v-icon>
                </template>
                <span>Logout</span>
            </v-tooltip>
        </v-btn>
    </v-system-bar>
</template>

<script>
import { mapState } from 'vuex';

    export default {
        data() {
            return {
                user: '',
                dialog: false,
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