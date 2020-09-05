<template>
  <div>
    <v-hover>
      <template v-slot="{ hover }">
        <v-card
         class="navbar projectCard"
         max-width="344" 
         dark 
         shaped 
         :elevation="hover ? 24 : 1"
         >
          <v-list-item three-line>
            <v-list-item-content>
              <v-list-item-title class="headline mb-1">{{project.name}}</v-list-item-title>
              <v-list-item-subtitle>
                <span>{{project.description}}</span>
              </v-list-item-subtitle>
            </v-list-item-content>

            <v-list-item-avatar tile size="100" color="transparent">
              <v-progress-circular
                :rotate="-90"
                :size="100"
                :width="15"
                :value="valueCard"
                color="link"
              >{{ valueCard }}</v-progress-circular>
            </v-list-item-avatar>
          </v-list-item>

          <v-card-actions>
            <v-btn 
            text
            outlined 
            color="link"
            @click="showProjectDetail()"
            >Details</v-btn>
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
      <div>
    <DetailProject/>
  </div>
  </div>
</template>

<script>
import DetailProject from '@/components/DetailProject.vue';

export default {
  props: ["project"],
  data() {
    return {
      valueCard: "50/100",
      valueDetail: "30/100",
      ex11: true,
      drawer: null,
      tab: null,
    };
  },
  components: {
    DetailProject
  },
  methods:  {
    showProjectDetail() {
      this.$store.commit("showProjectDetail");
      this.$store.commit("setProjectDetail", this.detailproject);
    }
  }
};
</script>

<style lang="css" scoped>
@import "../main.css";
</style>