<template>
    <div>
        <v-navigation-drawer
      v-model="detail"
      absolute
      temporary
      right
      width="800"
      color="navbar"
      dark
    >
      <v-container>
        <v-card>
          <v-tabs
            v-model="tab"
            dark
            background-color="navbar"
            slider-color="link"
            centered
            grow
            tile
          >
            <v-tab
            >
              Details
            </v-tab>
            <v-tab
            >
              Info
            </v-tab>
          </v-tabs>

          <v-tabs-items
          v-model="tab" 
          background-color="navbar"
          color="navbar"
          >
            <v-tab-item
            >
              <v-card flat dark color="navbar" tile>
                <v-card-text>
                    <v-text-field
                    label="Projektname*"
                    required
                    prepend-icon="mdi-information-outline"
                    class="ma-1"
                  ></v-text-field>
                  <v-text-field
                    label="Projekt Start*"
                    hint="DD/MM/JJJJ"
                    required
                    persistent-hint
                    prepend-icon="mdi-calendar-range"
                    class="ma-1"
                  ></v-text-field>
                  <v-text-field
                    label="Projekt Ende*"
                    hint="DD/MM/JJJJ"
                    persistent-hint
                    required
                    prepend-icon="mdi-calendar-range"
                    class="mb-6 mt-1 ml-1 mr-1"
                  ></v-text-field>
                  <v-textarea
                    label="Projektbeschreibung"
                    prepend-icon="mdi-information-outline"
                    outlined
                    height="70"
                    class="ma-1"
                  ></v-textarea>
                  <v-textarea
                    label="Definition of Ready"
                    prepend-icon="mdi-information-outline"
                    outlined
                    height="70"
                    class="ma-1"
                  ></v-textarea>
                  <v-textarea
                    label="Definition of Done"
                    prepend-icon="mdi-information-outline"
                    outlined
                    height="70"
                    class="ma-0"
                  ></v-textarea>
                  <v-select
                    :items="['User1', 'User2', 'User3', 'User4']"
                    label="Projekt Mitglieder*"
                    multiple
                    required
                    prepend-icon="mdi-account-multiple-plus"
                  ></v-select>
                  <v-btn color="link" text @click="drawer = false">Close</v-btn>
                  <v-btn color="link" text @click="drawer = false">Save</v-btn>
                </v-card-text>
              </v-card>
            </v-tab-item>
            <v-tab-item
            >
              <v-card flat dark color="navbar" tile>
                <v-card-text>
                  <v-select
                    :items="['Nicht gestartet', 'Läuft', 'Überzogen', 'Beendet']"
                    label="Status*"
                    required
                    prepend-icon="mdi-circle-edit-outline"
                  ></v-select>
                  <span class="headline ma-4">Sprintinformationen</span>
                  <v-row>
                    <div class="ma-4">
                      <v-progress-circular
                        :rotate="-90"
                        :size="100"
                        :width="15"
                        :value="valueDetail"
                        color="link"
                      >{{ valueDetail }}</v-progress-circular>
                    </div>
                    <div class="ma-4">
                      <p>Sprints absolviert: 75</p>
                      <p>Sprints geplant: 100</p>
                      <p>Sprintlänge in Wochentagen: 20</p>
                      <p>nächster Sprintende: 13.07.20</p>
                      <p>nächster Sprintstart: 14.07.20</p>
                    </div>
                  </v-row>
                    <v-btn color="link" text @click="drawer = false">Close</v-btn>
                    <v-btn color="link" text @click="drawer = false">Save</v-btn>
                </v-card-text>
              </v-card>
            </v-tab-item>
          </v-tabs-items>
        </v-card>
      </v-container>
    </v-navigation-drawer>

    </div>
</template>

<script>
import { mapState } from "vuex"
    export default {
        name:"DetailProject",
        data() {
            return {
                detail: null,
                tab: null,
            }
        },
        computed: {
          ...mapState({
            visible: "detailProjectVisable",
            task: "detailProject"
          }),
        }
        
    }
</script>

<style lang="css" scoped>
@import "../main.css";

</style>