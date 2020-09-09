<template>
  <div>
    <v-hover>
      <template v-slot="{ hover }">
        <v-card 
        class="task mt-4" 
        min-width="300" 
        max-height="260" 
        :elevation="hover ? 14 : 5"
        @click="showDialog()"
        >
          <div class="task-header2 task">
            <span class="task-name">{{task.name}}</span>
            <v-spacer></v-spacer>
            <span class="task-status">
              <!-- Card Status: New -->
              <v-tooltip bottom v-if="task.status === 'NW'">
                <template v-slot:activator="{ on, attrs }">
                  <v-icon
                    class="task-status-icons"
                    color="tabbody"
                    v-bind="attrs"
                    v-on="on"
                  >mdi-new-box</v-icon>
                </template>
                <span>Status: new</span>
              </v-tooltip>
              <!-- Card Status: Not Started -->
              <v-tooltip bottom v-else-if="task.status === 'NS'">
                <template v-slot:activator="{ on, attrs }">
                  <v-icon
                    class="task-status-icons"
                    color="tabbody"
                    v-bind="attrs"
                    v-on="on"
                  >mdi-coffee</v-icon>
                </template>
                <span>Status: not started</span>
              </v-tooltip>
              <!-- Card Status: Planned -->
              <v-tooltip bottom v-else-if="task.status === 'PL'">
                <template v-slot:activator="{ on, attrs }">
                  <v-icon
                    class="task-status-icons"
                    color="tabbody"
                    v-bind="attrs"
                    v-on="on"
                  >mdi-notebook</v-icon>
                </template>
                <span>Status: not started</span>
              </v-tooltip>
              <!-- Card Status: In Pogress -->
              <v-tooltip bottom v-else-if="task.status === 'IP'">
                <template v-slot:activator="{ on, attrs }">
                  <v-icon
                    class="task-status-icons"
                    color="tabbody"
                    v-bind="attrs"
                    v-on="on"
                  >mdi-circle-slice-4</v-icon>
                </template>
                <span>Status: In Progress</span>
              </v-tooltip>
              <!-- Card Status: Done -->
              <v-tooltip bottom v-else-if="task.status === 'DO'">
                <template v-slot:activator="{ on, attrs }">
                  <v-icon
                    class="task-status-icons"
                    color="tabbody"
                    v-bind="attrs"
                    v-on="on"
                  >mdi-beaker-check</v-icon>
                </template>
                <span>Status: Done</span>
              </v-tooltip>
              <!-- Card Status: Accepted-->
              <v-tooltip bottom v-else-if="task.status ==='AC'">
                <template v-slot:activator="{ on, attrs }">
                  <v-icon
                    class="task-status-icons"
                    color="tabbody"
                    v-bind="attrs"
                    v-on="on"
                  >mdi-bookmark-check</v-icon>
                </template>
                <span>Status: Accepted</span>
              </v-tooltip>
            </span>
          </div>
          <v-card-text class="pa-0 task">
            <div class="task-body2 task">
              <div class="task-icons">
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-icon
                      class="task-status-icons ml-1"
                      color="tabbody"
                      v-bind="attrs"
                      v-on="on"
                    >mdi-calendar-range</v-icon>
                  </template>
                  <span>Planned implementation</span>
                </v-tooltip>
                <span>DD/MM/JJJJ</span>
                <div class="task-icons2">
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-icon
                        class="task-status-icons ml-1"
                        color="tabbody"
                        v-bind="attrs"
                        v-on="on"
                      >mdi-chart-bubble</v-icon>
                    </template>
                    <span>Story Points</span>
                  </v-tooltip>
                  <span>{{task.storypoints}}</span>
                  <!-- Use Images -->
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-icon
                        class="task-status-icons ml-1"
                        color="tabbody"
                        v-bind="attrs"
                        v-on="on"
                      >mdi-file-image-outline</v-icon>
                    </template>
                    <span>Task: used images</span>
                  </v-tooltip>
                  <span>1</span>
                  <!-- Steps -->
                  <v-tooltip bottom>
                    <template v-slot:activator="{ on, attrs }">
                      <v-icon
                        class="task-status-icons ml-1"
                        color="tabbody"
                        v-bind="attrs"
                        v-on="on"
                      >mdi-check-box-multiple-outline</v-icon>
                    </template>
                    <span>open steps</span>
                  </v-tooltip>
                  <span>{{task.number_of_open_steps}} / {{task.number_of_steps}}</span>
                </div>
              </div>


            </div>
            <v-container >
            <!-- assigned Users -->
            <v-row>
              <v-col>
                <section class="avatars-group pa-3 stacked">
                  <div v-for="avatar in avatarsStackedLimited" 
                    :key="`avatar-id-${avatar.id}`" 
                    class="avatars-group__item">
                      <v-tooltip bottom>
                        <template v-slot:activator="{ on, attrs }">
                          <div v-bind="attrs" v-on="on">
                          <ProfileAvatar :avatar="avatar"/>
                          </div>
                        </template>
                      <ProfileTooltip :avatar="avatar" />
                    </v-tooltip>
                  </div>
                  <div class="avatars-group__item more">
                <v-avatar color="primary" size="40px">
                  <v-menu
                    v-model="stackedMenu"
                    lazy
                    open-delay="1000"
                    open-on-hover
                    offset-y
                    :max-height="menuMaxHeight"
                    nudge-bottom="8"
                  >
                    <template v-slot:activator="{ on }">
                      <v-btn icon v-on="on">
                        <v-icon :color="tabbody" >mdi-dots-horizontal</v-icon>
                      </v-btn>
                    </template>
                    <v-list dense two-line>
                      <v-list-item
                      v-for="avatar in avatarsSorted"
                        :key="`avatar-menu-id-${avatar.id}`"
                        avatar
                      >
                        <v-list-item-avatar>
                          <ProfileAvatar :avatar="avatar" custom-class="bordered small" size="32px"/>
                        </v-list-item-avatar>
                        <v-list-item-content>
                          <v-list-item-title>{{ avatar.username }}</v-list-item-title>
                          <v-list-item-subtitle>{{ avatar.email }}</v-list-item-subtitle>
                        </v-list-item-content>
                      </v-list-item>
                    </v-list>
                  </v-menu>
                </v-avatar>
              </div>
                </section>
                
              </v-col>
            </v-row>
            <v-row>
              <v-col>
                <v-chip-group class="ml-2">
                  <v-chip
                    v-for="label in task.labels"
                    :key="label.id"
                    :color="label.color"
                    v-text="label.title"
                  ></v-chip>
                </v-chip-group>
              </v-col>
            </v-row>
            </v-container>


              
            
            
          </v-card-text>
        </v-card>
      </template>
    </v-hover>
  </div>
</template>

<script>
import {mapGetters} from "vuex";
import ProfileAvatar from "@/components/Profile/ProfileAvatar.vue";
import ProfileTooltip from "@/components/Profile/ProfileTooltip.vue";
export default {
  data: () => ({
    dialog: null,
  }),
  props: ["task"],
  components: {
    ProfileAvatar,
    ProfileTooltip
  },

  methods: {
    
    showDialog() {
      this.$store.commit("hideDetailView");
      this.$store.commit("showDetailView");
      this.$store.commit("setDetailTask", this.task);
    },
    GetUserInitial(id){
      var inital = "AA";
      var user = this.UsersById(id)
      inital = user.username.substring(0,2);
      return inital;
    },
  },
  computed:{
    ...mapGetters("user", {
      UsersById: "byId",
      usersByIdArray: "byIdArray"
    }),
    avatarsSorted () {
      return (this.usersByIdArray(this.task.assigned_users) && this.usersByIdArray(this.task.assigned_users).length > 0)
        ? this.usersByIdArray(this.task.assigned_users).sort((a, b) => a.username.localeCompare(b.alt))
        : null
    },
    avatarsStackedLimited () {
      return (this.avatarsSorted && this.avatarsSorted.length > 0)
        ? this.avatarsSorted.slice(0, 5)
        : null
    }
  },
  

};
</script>

<style lang="css" scoped>
@import "../main.css";
@import './Profile/profile.css';
</style>