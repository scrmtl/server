<template>
  <div>
    <v-card class="mx-auto lane mr-10" max-width="320" elevation="5">
      <div class="lane-header">
        <p dark>
          {{ lane.name }}
          <v-menu>
            <template v-slot:activator="{ on }">
              <v-btn dark icon v-on="on" class="icon" height="32">
                <v-icon>mdi-dots-vertical</v-icon>
              </v-btn>
            </template>
            <v-list>
              <v-list-item v-for="(item, i) in items" :key="i">
                <v-list-item-title>{{ item.title }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </p>
      </div>
      
      <v-card-text class="lane-body pa-2">
        <div v-for="task in getLaneTasks()" :key="task.id">
          <Task v-bind:task="task" />
        </div>
      </v-card-text>
      <v-card-actions class="lane-extended"></v-card-actions>
    </v-card>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';
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
  methods:{
    ...mapActions("task", {
      fetchTask: "fetchList"
    }),

    fetchData() {
        this.fetchTask({ customUrlFnArgs: {laneId: this.lane.id}});
    },

    getLaneTasks(){
      var LaneTasks = [];
      this.lane.task_cards.forEach(taskId => {
        LaneTasks.push(this.tasksById(taskId));
        console.log(taskId);
        console.log(this.tasksById(taskId));
      });
      console.log(LaneTasks);
      return LaneTasks;
    }
  },
  computed:{
    ...mapGetters("task",{
      tasksById: "byId"
    })

  },
  updated(){
    
  },
  created(){
    this.fetchData();
  }
};
</script>

<style lang="scss" scoped>
</style>