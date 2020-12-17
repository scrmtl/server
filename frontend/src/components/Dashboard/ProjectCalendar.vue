<template>
  <v-card>
  <v-card-title class="navbar white--text">Project Calendar</v-card-title>
  <v-card-text class="navbar white--text">
    <v-sheet
      tile
      height="64"
    >
      <v-toolbar flat>
        <v-btn
          outlined
          class="mr-4"
          color="grey darken-2"
          @click="setToday"
        >
          Today
        </v-btn>
        <v-btn
          fab
          text
          small
          color="grey darken-2"
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
          color="grey darken-2"
          @click="next"
        >
          <v-icon small>
            mdi-chevron-right
          </v-icon>
        </v-btn>
        <v-toolbar-title v-if="$refs.calendar">
          {{ $refs.calendar.title }}
        </v-toolbar-title>
        <v-spacer></v-spacer>
      </v-toolbar>
    </v-sheet>
    <v-sheet height="600">
    <v-calendar
      ref="calendar"
      v-model="focus"
      weekdays="[1, 2, 3, 4, 5, 6, 0]"
      type="month"
      :events="projectEvents"
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
    events: [],
    // Test
    colors: ['blue', 'indigo', 'deep-purple', 'cyan', 'green', 'orange', 'grey darken-1'],
    names: ['Meeting', 'Holiday', 'PTO', 'Travel', 'Event', 'Birthday', 'Conference', 'Party'],
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
          color: "green",
          duration: 1
      });
      events.push({
          name: "Project end",
          start: project.end,
          color: "green",
          duration: 1
      });
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

    getProjectEvents(){
      const events = [];
      var project = this.projectById(this.$route.params.id);

      events.push({
          name: "Project start",
          start: project.start,
          color: "blue",
      });
      this.events = events;
      console.log(events);
    },
    
    getEvents ({ start, end }) {
      const events = [];

      const min = new Date(`${start.date}T00:00:00`);
      const max = new Date(`${end.date}T23:59:59`);
      const days = (max.getTime() - min.getTime()) / 86400000;
      const eventCount = this.rnd(days, days + 20);

      for (let i = 0; i < eventCount; i++) {
        const allDay = this.rnd(0, 3) === 0;
        const firstTimestamp = this.rnd(min.getTime(), max.getTime());
        const first = new Date(firstTimestamp - (firstTimestamp % 900000));
        const secondTimestamp = this.rnd(2, allDay ? 288 : 8) * 900000;
        const second = new Date(first.getTime() + secondTimestamp);

        events.push({
          name: this.names[this.rnd(0, this.names.length - 1)],
          start: first,
          end: second,
          color: this.colors[this.rnd(0, this.colors.length - 1)],
          timed: !allDay,
        });
      }

      this.events = events;
      console.log(events)
    },
    //Test
    rnd (a, b) {
        return Math.floor((b - a + 1) * Math.random()) + a
      },
  }
}
</script>

<style>

</style>