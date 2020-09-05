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
                    <template>
                        <v-data-table
                            :headers="headers"
                            :items="desserts"
                            sort-by="calories"
                            class="elevation-1"
                        >
                            <template v-slot:top>
                            <v-toolbar flat color="white">
                                <v-toolbar-title>My CRUD</v-toolbar-title>
                                <v-divider
                                class="mx-4"
                                inset
                                vertical
                                ></v-divider>
                                <v-spacer></v-spacer>
                                <v-dialog v-model="dialog" max-width="500px">
                                <template v-slot:activator="{ on, attrs }">
                                    <v-btn
                                    color="primary"
                                    dark
                                    class="mb-2"
                                    v-bind="attrs"
                                    v-on="on"
                                    >New Item</v-btn>
                                </template>
                                <v-card>
                                    <v-card-title>
                                    <span class="headline">{{ formTitle }}</span>
                                    </v-card-title>

                                    <v-card-text>
                                    <v-container>
                                        <v-row>
                                        <v-col cols="12" sm="6" md="4">
                                            <v-text-field v-model="editedItem.name" label="Dessert name"></v-text-field>
                                        </v-col>
                                        <v-col cols="12" sm="6" md="4">
                                            <v-text-field v-model="editedItem.calories" label="Calories"></v-text-field>
                                        </v-col>
                                        <v-col cols="12" sm="6" md="4">
                                            <v-text-field v-model="editedItem.fat" label="Fat (g)"></v-text-field>
                                        </v-col>
                                        <v-col cols="12" sm="6" md="4">
                                            <v-text-field v-model="editedItem.carbs" label="Carbs (g)"></v-text-field>
                                        </v-col>
                                        <v-col cols="12" sm="6" md="4">
                                            <v-text-field v-model="editedItem.protein" label="Protein (g)"></v-text-field>
                                        </v-col>
                                        </v-row>
                                    </v-container>
                                    </v-card-text>

                                    <v-card-actions>
                                    <v-spacer></v-spacer>
                                    <v-btn color="blue darken-1" text @click="close">Cancel</v-btn>
                                    <v-btn color="blue darken-1" text @click="save">Save</v-btn>
                                    </v-card-actions>
                                </v-card>
                                </v-dialog>
                            </v-toolbar>
                            </template>
                            <!-- eslint-disable-next-line vue/no-v-html -->
                             <template v-slot:item.actions="{ item }">
                            <v-icon
                                small
                                class="mr-2"
                                @click="editItem(item)"
                            >
                                mdi-pencil
                            </v-icon>
                            <v-icon
                                small
                                @click="deleteItem(item)"
                            >
                                mdi-delete
                            </v-icon>
                            </template>
                            <template v-slot:no-data>
                            <v-btn color="primary" @click="initialize">Reset</v-btn>
                            </template>
                        </v-data-table>
                        </template>
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
                headers: [
                    {
                    text: 'Dessert (100g serving)',
                    align: 'start',
                    sortable: false,
                    value: 'name',
                    },
                    { text: 'Calories', value: 'calories' },
                    { text: 'Fat (g)', value: 'fat' },
                    { text: 'Carbs (g)', value: 'carbs' },
                    { text: 'Protein (g)', value: 'protein' },
                    { text: 'Actions', value: 'actions', sortable: false },
                ],
                desserts: [],
                editedIndex: -1,
                editedItem: {
                    name: '',
                    calories: 0,
                    fat: 0,
                    carbs: 0,
                    protein: 0,
                },
                defaultItem: {
                    name: '',
                    calories: 0,
                    fat: 0,
                    carbs: 0,
                    protein: 0,
                },
            };
        },
        computed: mapState({
            username: state => state.Userinfo.username,
            formTitle () {
        return this.editedIndex === -1 ? 'New Item' : 'Edit Item'
            }
      }),
      watch: {
      dialog (val) {
        val || this.close()
      },
      created () {
      this.initialize()
    },

    methods: {
      initialize () {
        this.desserts = [
          {
            name: 'Frozen Yogurt',
            calories: 159,
            fat: 6.0,
            carbs: 24,
            protein: 4.0,
          },
          {
            name: 'Ice cream sandwich',
            calories: 237,
            fat: 9.0,
            carbs: 37,
            protein: 4.3,
          },
          {
            name: 'Eclair',
            calories: 262,
            fat: 16.0,
            carbs: 23,
            protein: 6.0,
          },
          {
            name: 'Cupcake',
            calories: 305,
            fat: 3.7,
            carbs: 67,
            protein: 4.3,
          },
          {
            name: 'Gingerbread',
            calories: 356,
            fat: 16.0,
            carbs: 49,
            protein: 3.9,
          },
          {
            name: 'Jelly bean',
            calories: 375,
            fat: 0.0,
            carbs: 94,
            protein: 0.0,
          },
          {
            name: 'Lollipop',
            calories: 392,
            fat: 0.2,
            carbs: 98,
            protein: 0,
          },
          {
            name: 'Honeycomb',
            calories: 408,
            fat: 3.2,
            carbs: 87,
            protein: 6.5,
          },
          {
            name: 'Donut',
            calories: 452,
            fat: 25.0,
            carbs: 51,
            protein: 4.9,
          },
          {
            name: 'KitKat',
            calories: 518,
            fat: 26.0,
            carbs: 65,
            protein: 7,
          },
        ]
      },

      editItem (item) {
        this.editedIndex = this.desserts.indexOf(item)
        this.editedItem = Object.assign({}, item)
        this.dialog = true
      },

      deleteItem (item) {
        const index = this.desserts.indexOf(item)
        confirm('Are you sure you want to delete this item?') && this.desserts.splice(index, 1)
      },

      close () {
        this.dialog = false
        this.$nextTick(() => {
          this.editedItem = Object.assign({}, this.defaultItem)
          this.editedIndex = -1
        })
      },

      save () {
        if (this.editedIndex > -1) {
          Object.assign(this.desserts[this.editedIndex], this.editedItem)
        } else {
          this.desserts.push(this.editedItem)
        }
        this.close()
   },
    },
  }}
</script>

<style lang="css" scoped>
@import "../main.css";

</style>