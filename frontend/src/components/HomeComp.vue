<template>
  <div class="tabbody tab-content">
    <v-card
        class="mx-auto lane mr-10"
        max-width="320"
        elevation="5"
      >
      <div class="lane-header">
      <p dark>Example Lane
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
          <v-card
              class="mx-auto mt-2 task"
              max-width="260"
              elevation="5"
            >
              <div class="task-header">
              <span class="task-name">Task Name</span>
              <span>
                <v-icon class="task-worker-icon" dark>mdi-account-circle</v-icon>
                <v-icon class="task-worker-icon" dark>mdi-account-circle</v-icon>
                <v-icon class="task-worker-icon" dark>mdi-account-circle</v-icon>
              </span>
              </div>
              <v-card-text class="pa-0">
              <div class="task-labels">
                  <div class="label-backend"><span>Backend</span></div>
                  <div class="label-frontend"><span>Frontend</span></div>
                  <div class="label-ux"><span>UX/UI</span></div>
                  <div class="label-bug"><span>BUG</span></div>
              </div>
              <div class="task-body">
                <div class="task-parent-name">
                <v-icon dark>mdi-cards-variant</v-icon>
                <span>parent-name</span>
                <span class="task-story-points">
                <v-icon dark>mdi-chart-bubble</v-icon>
                <span>13</span>
                </span>
                <span class="task-checklist-icon">
                  <v-icon dark>mdi-file-image-outline</v-icon>
                </span>
                <span class="task-story-points">
                  <v-icon dark>mdi-check-box-multiple-outline</v-icon>
                </span>
                </div>
              </div>
              </v-card-text>
          </v-card>
          <v-card
              class="mx-auto mt-2 task"
              max-width="260"
              elevation="5"
              disabled="true"
            >
              <div class="task-header">
              <span class="task-name">Task Name</span>
              <span>
                <v-icon class="task-worker-icon" dark>mdi-account-circle</v-icon>
                <v-icon class="task-worker-icon" dark>mdi-account-circle</v-icon>
                <v-icon class="task-worker-icon" dark>mdi-account-circle</v-icon>
              </span>
              </div>
              <v-card-text class="pa-0">
              <div class="task-labels">
                  <div class="label-backend"><span>Backend</span></div>
                  <div class="label-frontend"><span>Frontend</span></div>
                  <div class="label-ux"><span>UX/UI</span></div>
                  <div class="label-bug"><span>BUG</span></div>
              </div>
              <div class="task-body">
                <div class="task-parent-name">
                <v-icon dark>mdi-cards-variant</v-icon>
                <span>parent-name</span>
                <span class="task-story-points">
                <v-icon dark>mdi-chart-bubble</v-icon>
                <span>13</span>
                </span>
                <span class="task-checklist-icon">
                  <v-icon dark>mdi-file-image-outline</v-icon>
                </span>
                <span class="task-story-points">
                  <v-icon dark>mdi-check-box-multiple-outline</v-icon>
                </span>
                </div>
              </div>
              </v-card-text>
          </v-card>

          <v-card
              class="mx-auto mt-2 task"
              max-width="260"
              elevation="5"
            >
              <div class="task-header2">
              <span class="task-name">Task Name</span>
              <span>
                <v-icon class="task-worker-icon" dark>mdi-account-circle</v-icon>
                <v-icon class="task-worker-icon" dark>mdi-account-circle</v-icon>
                <v-icon class="task-worker-icon" dark>mdi-account-circle</v-icon>
              </span>
              </div>
              <v-card-text class="pa-0">
              <div class="task-labels2">
                  <div class="label-backend"><span>Backend</span></div>
                  <div class="label-frontend"><span>Frontend</span></div>
                  <div class="label-ux"><span>UX/UI</span></div>
                  <div class="label-bug"><span>BUG</span></div>
              </div>
              <div class="task-body2">
                <div class="task-parent-name">
                <v-icon dark>mdi-cards-variant</v-icon>
                <span>parent-name</span>
                <span class="task-story-points">
                <v-icon dark>mdi-chart-bubble</v-icon>
                <span>13</span>
                </span>
                <span class="task-checklist-icon">
                  <v-icon dark>mdi-file-image-outline</v-icon>
                </span>
                <span class="task-story-points">
                  <v-icon dark>mdi-check-box-multiple-outline</v-icon>
                </span>
                </div>
              </div>
              </v-card-text>
          </v-card>

          <v-card
              class="mx-auto mt-2 task"
              max-width="260"
              elevation="5"
              disabled="true"
            >
              <div class="task-header2">
              <span class="task-name">Task Name</span>
              <span>
                <v-icon class="task-worker-icon" dark>mdi-account-circle</v-icon>
                <v-icon class="task-worker-icon" dark>mdi-account-circle</v-icon>
                <v-icon class="task-worker-icon" dark>mdi-account-circle</v-icon>
              </span>
              </div>
              <v-card-text class="pa-0">
              <div class="task-labels2">
                  <div class="label-backend"><span>Backend</span></div>
                  <div class="label-frontend"><span>Frontend</span></div>
                  <div class="label-ux"><span>UX/UI</span></div>
                  <div class="label-bug"><span>BUG</span></div>
              </div>
              <div class="task-body2">
                <div class="task-parent-name">
                <v-icon dark>mdi-cards-variant</v-icon>
                <span>parent-name</span>
                <span class="task-story-points">
                <v-icon dark>mdi-chart-bubble</v-icon>
                <span>13</span>
                </span>
                <span class="task-checklist-icon">
                  <v-icon dark>mdi-file-image-outline</v-icon>
                </span>
                <span class="task-story-points">
                  <v-icon dark>mdi-check-box-multiple-outline</v-icon>
                </span>
                </div>
              </div>
              </v-card-text>
          </v-card>


        </v-card-text>
        <v-card-actions class="lane-extended">

        </v-card-actions>
    </v-card>
    <v-card
      class="mx-auto epic"
      max-width="300"
      elevation="5"
    >
      <div class="epic-header">
      <p dark>Example Epic
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
                v-for="(epicItem, i) in epicItem"
                :key="i"
              >
                <v-list-item-title>{{ epicItem.title }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu></p> 
      </div>
      <v-card-text class="epic-body pa-0">
          <div>
            <v-icon class="worker-icon">mdi-account-circle</v-icon>
            <v-icon class="worker-icon">mdi-account-circle</v-icon>
            <v-icon class="worker-icon">mdi-account-circle</v-icon>
          </div>
          <div class="label">
            <div class="label-backend"><span>Backend</span></div>
            <div class="label-frontend"><span>Frontend</span></div>
            <div class="label-ux"><span>UX/UI</span></div>
            <div class="label-bug"><span>BUG</span></div>
          </div>
          <div class="points">
            <div >
              <div class="parent-name">
                <v-icon>mdi-cards-variant</v-icon>
                <span>name</span>
              </div>
              <div class="story-points">
                <v-icon>mdi-chart-bubble</v-icon>
                <span>13</span>
              </div>
            </div>
          </div>
          <div class="epic-content">
            <v-card
              class="mx-auto"
              max-width="280"
              elevation="5"
            >
              <div class="feature-header">
              <p dark>Example Feature
                <v-menu>
                  <template v-slot:activator="{ on }">
                    <v-btn
                    dark
                    icon
                    v-on="on"
                    class="icon"
                    height="20"
                    >
                      <v-icon>mdi-dots-vertical</v-icon>
                    </v-btn>
                  </template>
                  <v-list>
                    <v-list-item
                      v-for="(featureItem, i) in featureItem"
                      :key="i"
                    >
                      <v-list-item-title>{{ featureItem.title }}</v-list-item-title>
                    </v-list-item>
                  </v-list>
                </v-menu></p> 
              </div>
              <v-card-text class="feature-body pa-0">
                  <div>
                    <v-icon class="worker-icon">mdi-account-circle</v-icon>
                    <v-icon class="worker-icon">mdi-account-circle</v-icon>
                    <v-icon class="worker-icon">mdi-account-circle</v-icon>
                  </div>
                  <div class="label">
                    <div class="label-backend"><span>Backend</span></div>
                    <div class="label-frontend"><span>Frontend</span></div>
                    <div class="label-ux"><span>UX/UI</span></div>
                    <div class="label-bug"><span>BUG</span></div>
                  </div>
                  <div class="feature-points">
                    <div >
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
                <v-btn
                text
                color="link"
                >
                <v-icon>mdi-chevron-right</v-icon> Show Tasks
                </v-btn>
              </v-card-actions>
            </v-card>
            <v-card
              class="mx-auto mt-2"
              max-width="280"
              elevation="5"
            >
              <div class="feature-header">
              <p dark>Example Feature
                <v-menu>
                  <template v-slot:activator="{ on }">
                    <v-btn
                    dark
                    icon
                    v-on="on"
                    class="icon"
                    height="20"
                    >
                      <v-icon>mdi-dots-vertical</v-icon>
                    </v-btn>
                  </template>
                  <v-list>
                    <v-list-item
                      v-for="(featureItem, i) in featureItem"
                      :key="i"
                    >
                      <v-list-item-title>{{ featureItem.title }}</v-list-item-title>
                    </v-list-item>
                  </v-list>
                </v-menu></p> 
              </div>
              <v-card-text class="feature-body pa-0">
                  <div>
                    <v-icon class="worker-icon">mdi-account-circle</v-icon>
                    <v-icon class="worker-icon">mdi-account-circle</v-icon>
                    <v-icon class="worker-icon">mdi-account-circle</v-icon>
                  </div>
                  <div class="label">
                    <div class="label-backend"><span>Backend</span></div>
                    <div class="label-frontend"><span>Frontend</span></div>
                    <div class="label-ux"><span>UX/UI</span></div>
                    <div class="label-bug"><span>BUG</span></div>
                  </div>
                  <div class="feature-points">
                    <div >
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
                <v-btn
                text
                color="link"
                >
                <v-icon>mdi-chevron-right</v-icon> Show Tasks
                </v-btn>
              </v-card-actions>
            </v-card>
        </div>  
      </v-card-text>
    </v-card>
    
  </div>
</template>

<script>
export default {
  data: () => ({
    items: [
      { title: "+ New Lane"},
      { title: "+ New Epic"},
      { title: "+ New Feature"},
      { title: "+ New Task"},
    ],
    epicItem: [
      { title: "+ New Feature"},
      { title: "+ New Task"},
    ],
    featureItem: [
      { title: "+ New Task"},
    ],

  })


};
</script>

<style lang="css" scoped>
@import "../main.css";

</style>





