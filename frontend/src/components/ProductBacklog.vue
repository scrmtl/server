<template>
  <body>
  <div class="tab-content tabbody">
    <v-card
        class="mx-auto lane mr-10"
        max-width="320"
        elevation="5"
      >
      <div class="lane-header">
      <p dark>Bugs
        <v-menu>
            <template v-slot:activator="{ on }">
              <v-btn
              dark
              icon
              v-on="on"
              class="icon"
              height="32"
              >
                <v-icon>mdi-dots-vertical</v-icon>
              </v-btn>
            </template>
            <v-list>
              <v-list-item
                v-for="(item, i) in items"
                :key="i"
              >
                <v-list-item-title>{{ item.title }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu></p> 
      </div>
        <v-card-text class="lane-body">

        </v-card-text>
        <v-card-actions class="lane-extended">

        </v-card-actions>
    </v-card>
    <v-card
        class="mx-auto lane mr-10"
        max-width="320"
        elevation="5"
      >
      <div class="lane-header">
      <p dark>Ideas
        <v-menu>
            <template v-slot:activator="{ on }">
              <v-btn
              dark
              icon
              v-on="on"
              class="icon"
              height="32"
              >
                <v-icon>mdi-dots-vertical</v-icon>
              </v-btn>
            </template>
            <v-list>
              <v-list-item
                v-for="(item, i) in items"
                :key="i"
              >
                <v-list-item-title>{{ item.title }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu></p> 
      </div>
        <v-card-text class="lane-body">
          
        </v-card-text>
        <v-card-actions class="lane-extended">

        </v-card-actions>
    </v-card>
    <v-card
        class="mx-auto lane mr-10"
        max-width="320"
        elevation="5"
      >
      <div class="lane-header">
      <p dark>Product Backlog
        <v-menu>
            <template v-slot:activator="{ on }">
              <v-btn
              dark
              icon
              v-on="on"
              class="icon"
              height="32"
              >
                <v-icon>mdi-dots-vertical</v-icon>
              </v-btn>
            </template>
            <v-list>
              <v-list-item
                v-for="(item, i) in items"
                :key="i"
              >
                <v-list-item-title>{{ item.title }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu></p> 
      </div>
        <v-card-text class="lane-body">
          
        </v-card-text>
        <v-card-actions class="lane-extended">

        </v-card-actions>
    </v-card>
    <v-card
        class="mx-auto lane mr-10 mb-10"
        max-width="320"
        elevation="5"
      >
      <div class="lane-header">
      <p dark>Growning (for Refinement)
        <v-menu>
            <template v-slot:activator="{ on }">
              <v-btn
              dark
              icon
              v-on="on"
              class="icon"
              height="32"
              >
                <v-icon>mdi-dots-vertical</v-icon>
              </v-btn>
            </template>
            <v-list>
              <v-list-item
                v-for="(item, i) in items"
                :key="i"
              >
                <v-list-item-title>{{ item.title }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu></p> 
      </div>
        <v-card-text class="lane-body">
          
        </v-card-text>
        <v-card-actions class="lane-extended">

        </v-card-actions>
    </v-card>
    <v-card
        class="mx-auto lane mr-10"
        max-width="320"
        elevation="5"
      >
      <div class="lane-header">
      <p dark>Ready (for next Sprints)
        <v-menu>
            <template v-slot:activator="{ on }">
              <v-btn
              dark
              icon
              v-on="on"
              class="icon"
              height="32"
              >
                <v-icon>mdi-dots-vertical</v-icon>
              </v-btn>
            </template>
            <v-list>
              <v-list-item
                v-for="(item, i) in items"
                :key="i"
              >
                <v-list-item-title>{{ item.title }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu></p> 
      </div>
        <v-card-text class="lane-body">
          
        </v-card-text>
        <v-card-actions class="lane-extended">

        </v-card-actions>
    </v-card>
  </div>
  </body>
</template>

<script>
export default {
  data: () => ({
    items: [
      { title: "+ New Lane"},
      { title: "+ New Epic"},
      { title: "+ New Feature"},
      { title: "+ New Task"},
    ]
  })

};
</script>

<style lang="css" scoped>
@import "../main.css";

.tab-content {
  height: 1500px;
  padding: 20px;
}
</style>
