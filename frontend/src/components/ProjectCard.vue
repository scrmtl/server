<template>
  <div>
    <v-hover>
      <template v-slot="{ hover }">
        <v-card class="navbar projectCard" max-width="344" dark shaped :elevation="hover ? 24 : 1">
          <v-list-item three-line>
            <v-list-item-content>
              <v-list-item-title class="headline mb-1">Projektname</v-list-item-title>
              <v-list-item-subtitle>
                <span>
                  Lorem ipsum dolor sit amet, consetetur sadipscing elitr,
                  sed diam nonumy eirmod tempor invidunt ut labore et dolore
                  magna aliquyam erat, sed diam voluptua. At vero eos et
                  accusam et
                </span>
              </v-list-item-subtitle>
            </v-list-item-content>

            <v-list-item-avatar tile size="100" color="transparent">
              <v-progress-circular
                :rotate="-90"
                :size="100"
                :width="15"
                :value="value"
                color="link"
              >{{ value }}</v-progress-circular>
            </v-list-item-avatar>
          </v-list-item>

          <v-card-actions>
            <v-btn text class="status" outlined color="link">Details</v-btn>
            <v-spacer></v-spacer>
            <v-switch
              v-model="ex11"
              label
              color="link"
              value="select"
              hide-details
              class="projectCardSelect"
            ></v-switch>
            <v-spacer></v-spacer>
            <v-btn text class color="error" outlined>...Status</v-btn>
          </v-card-actions>
        </v-card>
      </template>
    </v-hover>
  </div>
</template>

<script>
export default {
  data() {
    return {
      value: "75/100",
      ex11: true
    };
  },
};
</script>

<style lang="css" scoped>
@import "../main.css";
</style>