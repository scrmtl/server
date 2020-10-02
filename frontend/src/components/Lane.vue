<template>
  <v-card class="lane" min-width="370" max-width="420">
    <v-card-title class="navbar white--text">
      <div>
        {{ lane.name }}
      </div>
      <v-spacer></v-spacer>
      <v-menu>
        <template v-slot:activator="{ on }">
          <v-btn dark icon v-on="on" class="icon" height="32">
            <v-icon>mdi-dots-vertical</v-icon>
          </v-btn>
        </template>
        <v-list>
          <v-list-item v-for="(item, i) in items" :key="i">
            <v-list-item-title>
              {{ item.title }}
            </v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-card-title>

    <v-card-text class="lane-body">
      <v-row
        v-for="task in this.tasksByIdArray(this.lane.task_cards)"
        :key="task.id"
      >
        <v-col>
          <Task v-bind:task="task" />
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import Task from "@/components/Task.vue";
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
  components: {
    Task
  },
  props: ["lane"],
  methods: {
    ...mapActions("task", {
      fetchTask: "fetchList"
    }),

    fetchData() {
      this.fetchTask({ customUrlFnArgs: { laneId: this.lane.id } });
    }
  },
  computed: {
    ...mapGetters("task", {
      tasksById: "byId",
      tasksByIdArray: "byIdArray"
    })
  },
  updated() {},
  created() {
    this.fetchData();
  }
};
</script>

<style lang="scss" scoped>
</style>