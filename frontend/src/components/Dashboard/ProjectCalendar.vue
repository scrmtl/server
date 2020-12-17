<template>
  <v-card tile flat>
  <v-card-title class="navbar white--text">Project Calendar</v-card-title>
  <v-card-text class="navbar white--text">
    <v-sheet
      tile
      height="64"
      class="navbar"
    >
      <v-toolbar class="navbar" flat>
        <v-btn
          outlined
          class="mr-4"
          color="link"
          @click="setToday"
        >
          Today
        </v-btn>
        <v-btn
          fab
          text
          small
          color="link"
          @click="prev"
        >
          <v-icon small>
            mdi-chevron-left
          </v-icon>
        </v-btn>
        <v-btn
          fab
          text
          small
          color="link"
          @click="next"
        >
          <v-icon small>
            mdi-chevron-right
          </v-icon>
        </v-btn>
        <v-toolbar-title class="white--text" v-if="$refs.calendar">
          {{ $refs.calendar.title }}
        </v-toolbar-title>
        <v-spacer></v-spacer>
      </v-toolbar>
    </v-sheet>
    <v-sheet class="navbar" height="875">
    <v-calendar
      ref="calendar"
      v-model="focus"
      type="month"
      color="link"
      dark
      :events="projectEvents"
      :event-color="getEventColor"
    ></v-calendar>
    </v-sheet>
  </v-card-text>
</v-card>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  name: "ProjectCalendar",
  data: () =>({
    focus: '',
  }),
  computed:{
    ...mapGetters("project", {
      projectById: "byId"
    }),
    ...mapGetters("sprint", {
      listSprints: "list"
    }),

    projectEvents(){
      const events = [];
      var project = this.projectById(this.$route.params.id);
      console.log(project)
      events.push({
          name: "Project start",
          start: project.start,
          color: "grey",
          category: "project",
          timed: false,
      });
      events.push({
          name: "Project end",
          start: project.end,
          color: "grey",
          category: "project",
          timed: false,
      });
      this.listSprints.forEach(sprint => {
        // Sprint Duration
        events.push({
          name: `Sprint ${sprint.number} (${sprint.version})`,
          start: sprint.start,
          end: sprint.end,
          color: "blue",
          category: "sprint",
          timed: false,
        });
        // Release Date
        events.push({
          name: `Release ${sprint.version}`,
          start: sprint.end,
          color: "orange",
          category: "Release",
          timed: false,
        });
        // Sprint planning date
        events.push({
          name: `Sprint planning for Sprint ${sprint.number}`,
          start: sprint.start,
          color: "green",
          category: "sprint",
          timed: false,
        });
        // Sprint planning date
        events.push({
          name: `Sprint review for Sprint ${sprint.number}`,
          start: sprint.end,
          color: "green",
          category: "sprint",
          timed: false,
        });
      })

      console.log(events)
      return events;
    }
  }, 
  methods: {
    setToday () {
      this.focus = ''
    },
    prev () {
      this.$refs.calendar.prev()
    },
    next () {
      this.$refs.calendar.next()
    },
    getEventColor (event) {
      return event.color
    },
  },
  mounted() {

  },
}
</script>

<style>

</style>