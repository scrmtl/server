<template>
    <v-hover>
      <template v-slot="{ hover }">
        <v-card 
        class="task"
        min-width="350"
        max-width="350"
        :elevation="hover ? 14 : 5"
        @click="showTaskDetail()"
        >
          <v-card-title  >
            <span class="tabbody--text">{{task.name}}</span>
            <v-spacer></v-spacer>
            <div>
              <!-- Card Status: New -->
              <v-tooltip bottom v-if="task.status === 'NW'">
                <template v-slot:activator="{ on, attrs }">
                  <v-icon
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
                    color="tabbody"
                    v-bind="attrs"
                    v-on="on"
                  >mdi-bookmark-check</v-icon>
                </template>
                <span>Status: Accepted</span>
              </v-tooltip>
            </div>
          </v-card-title>
          <v-card-text class="">
            <v-row dense>
              <v-col >
                <v-tooltip bottom>
                  <template v-slot:activator="{ on, attrs }">
                    <v-icon
                      color="tabbody"
                      v-bind="attrs"
                      v-on="on"
                    >mdi-calendar-range</v-icon>
                  </template>
                  <span>Planned implementation</span>
                </v-tooltip>
                <span>DD/MM/JJJJ</span>
              </v-col>
              <v-col cols="auto"></v-col>
              <v-col cols="2">
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
              </v-col>
              <v-col cols="3">
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
                <span>{{task.number_of_steps-task.number_of_open_steps}} / {{task.number_of_steps}}</span>
              </v-col>
            </v-row>
            <v-row dense >
              <div v-for="avatar in avatarsStackedLimited" :key="`avatar-id-${avatar.id}`" class="pa-1">
                <v-menu
                    open-delay="1500"
                    open-on-hover
                    :nudge-width="200"
                    offset-y
                  >
                  <template v-slot:activator="{ on, attrs }">
                    <div v-bind="attrs" v-on="on">
                    <ProfileAvatar :avatar="avatar"/>
                    </div>
                  </template>
                  <ProfileTooltip :avatar="avatar" />
                </v-menu>
              </div>
              <v-col align-self="center">
                <v-avatar   color="primary" size="32px">
                  <v-menu
                    v-model="stackedMenu"
                    
                    open-delay="1000"
                    open-on-hover
                    offset-y
                    :max-height="menuMaxHeight"
                    nudge-bottom="8"
                  >
                    <template v-slot:activator="{ on }">
                      <v-btn icon v-on="on" size="32px">
                        <v-icon color="link" >mdi-dots-horizontal</v-icon>
                      </v-btn>
                    </template>
                    <v-list dense two-line color="accent">
                      <v-list-item
                      v-for="avatar in avatarsSorted"
                        :key="`avatar-menu-id-${avatar.id}`"
                      >
                        <v-list-item-avatar>
                          <ProfileAvatar :avatar="avatar"  size="32px"/>
                        </v-list-item-avatar>
                        <v-list-item-content>
                          <v-list-item-title>{{ avatar.name }}</v-list-item-title>
                          <v-list-item-subtitle>{{ avatar.username }}</v-list-item-subtitle>
                        </v-list-item-content>
                      </v-list-item>
                    </v-list>
                  </v-menu>
                </v-avatar>
              </v-col>              
            </v-row>
            <v-row dense>
              <v-col>
                <v-chip-group column>
                  <v-chip
                    v-for="label in task.labels"
                    :key="label.id"
                    :color="label.color"
                    v-text="label.title"
                    text-color="white--text"
                    small
                  ></v-chip>
                </v-chip-group>
              </v-col>
            </v-row>
          </v-card-text>

        </v-card>
      </template>
    </v-hover>
    
</template>

<script>
import {mapGetters} from "vuex";
import ProfileAvatar from "@/components/Profile/ProfileAvatar.vue";
import ProfileTooltip from "@/components/Profile/ProfileTooltip.vue";

export default {
  data: () => ({
    dialog: null,
    menuMaxHeight: `${(60 * 5) + 4}px`,
    stackedLimit: 6,
    stackedMenu: false
  }),
  props: ["task"],
  components: {
    ProfileAvatar,
    ProfileTooltip,
    
  },

  methods: {
    
    showTaskDetail() {
      this.$store.commit("showTaskDetail", false);
      this.$store.commit("setSelectedTaskDetail", this.task);
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