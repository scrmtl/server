<template>
  <v-container fluid>
    <v-row justify="center">
      <v-col cols="1">
      </v-col>
      <v-col cols="6">
        <v-row justify="center">
        <span class="text-h5 white--text">Project x</span>
        </v-row>
        <v-row justify="center">
          <v-col>
            <v-expansion-panels dark accordion>
            <v-expansion-panel
              v-for="(item,i) in 5"
              :key="i"
              class="primary"
            >
              <v-expansion-panel-header>Task</v-expansion-panel-header>
              <v-expansion-panel-content>
                <v-row no-gutters justify="start">
                    <v-col>
                      Beschreibung vom Task.
                      Task werden nacheinander freigeschaltet, alle anderen sind derweil disabled
                      <v-btn
                        text
                        color="white"
                      >
                        Details
                      </v-btn>
                      
                    </v-col>
                    <v-divider
                      vertical
                      class="mx-4"
                    ></v-divider>
                    <v-col>
                      <v-row >
                        <v-col>
                          <v-autocomplete
                            v-model="storypoints"
                            :items="availableStorypoints"
                            outlined
                            dense
                            label="Story points"
                          ></v-autocomplete>
                        </v-col>
                      </v-row>
                      <v-spacer></v-spacer>
                      <v-row >
                        <v-col>
                          <v-btn
                            text
                            outlined
                            color="white"
                          >
                            Enthalten
                          </v-btn>
                        </v-col>
                      </v-row>
                      <v-row >
                        <v-col >
                          <v-btn
                            text
                            outlined
                            color="link"
                          >
                            Abgeben
                          </v-btn>
                        </v-col>
                      </v-row>
                    </v-col>
                  </v-row>
              </v-expansion-panel-content>
            </v-expansion-panel>
            </v-expansion-panels>
          </v-col>
        </v-row>
      </v-col>
      <v-col cols="4">
        <PokerSummary/>
      </v-col>
      <v-col cols="1">
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import PokerSummary from "@/components/Poker/PokerSummary.vue"
export default {
  components: { PokerSummary },
  name: "PlanningPoker",
  data: () => ({
    storypoints: 0,
    availableStorypoints: [0, 1, 2, 3, 5, 8, 13, 21, 34, 55],
  }),
}
</script>

<style>

</style>