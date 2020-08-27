<template>
  <div>
    <v-card class="mx-auto" max-width="280" elevation="5">
      <div class="feature-header">
        <p dark>
          Example Feature
          <v-menu>
            <template v-slot:activator="{ on }">
              <v-btn dark icon v-on="on" class="icon" height="20">
                <v-icon>mdi-dots-vertical</v-icon>
              </v-btn>
            </template>
            <v-list>
              <v-list-item v-for="(featureItem, i) in featureItem" :key="i">
                <v-list-item-title>{{ featureItem.title }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </p>
      </div>
      <v-card-text class="feature-body pa-0">
        <div>
          <v-icon class="worker-icon">mdi-account-circle</v-icon>
          <v-icon class="worker-icon">mdi-account-circle</v-icon>
          <v-icon class="worker-icon">mdi-account-circle</v-icon>
        </div>
        <div class="label">
          <div class="label-backend">
            <span>Backend</span>
          </div>
          <div class="label-frontend">
            <span>Frontend</span>
          </div>
          <div class="label-ux">
            <span>UX/UI</span>
          </div>
          <div class="label-bug">
            <span>BUG</span>
          </div>
        </div>
        <div class="feature-points">
          <div>
            <div class="parent-name">
              <v-icon>mdi-cards-variant</v-icon>
              <span>epic-name</span>
            </div>
            <div class="story-points">
              <v-icon>mdi-chart-bubble</v-icon>
              <span>13</span>
            </div>
          </div>
        </div>
      </v-card-text>
      <v-card-actions class="feature-extended">
        <v-btn text color="link">
          <v-icon>mdi-chevron-right</v-icon>Show Tasks
        </v-btn>
      </v-card-actions>
    </v-card>
  </div>
</template>

<script>


export default {
  data: () => ({
    items: [
      { title: "+ New Lane" },
      { title: "+ New Epic" },
      { title: "+ New Feature" },
      { title: "+ New Task" }
    ],
    epicItem: [{ title: "+ New Feature" }, { title: "+ New Task" }],
    featureItem: [{ title: "+ New Task" }]
  }),


};
</script>

<style lang="scss" scoped>
</style>