<template>
  <div>
    <v-dialog
      v-model="visible"
      persistent
      max-width="400px"
      content-class="TaskDialog"
      hide-overlay
      scrollable
    >
      <v-card class="task mt-4">
        <v-card-title>
          <span class="headline ma-0 pa-1">Task</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-text-field
              label="Taskname*"
              class="ma-1"
              required
              prepend-icon="mdi-information-outline"
              v-model="TaskData.name"
            ></v-text-field>
            <v-textarea
              label="Taskbeschreibung"
              prepend-icon="mdi-information-outline"
              outlined
              height="70"
              class="ma-1"
              v-model="TaskData.description"
            ></v-textarea>
            <v-select :items="Storypoints" label="Storypoints" v-model="TaskData.storypoints"></v-select>
            <v-select
              :items="['NW', 'PL', 'NS', 'DO', 'IP', 'AC']"
              label="Status*"
              required
              prepend-icon="mdi-circle-edit-outline"
              v-model="TaskData.status"
            ></v-select>
            <v-text-field label="Feature" v-model="TaskData.feature"></v-text-field>
            <v-chip-group column>
              <v-chip
                v-for="(label_item, i) in TaskData.labels"
                :key="i"
                :color="label_item.color"
                v-text="label_item.title"
              ></v-chip>
            </v-chip-group>
            <v-select
              :items="labelList"
              item-text="title"
              label="Label hinzufügen"
              :append-outer-icon="'mdi-plus'"
              v-model="selectedLabel"
              @click:append-outer="addLabel()"
            ></v-select>
            <!--<v-textarea label="Steplist"></v-textarea>-->
            <v-list multiple>
              <v-list-item-group v-for="step in TaskData.steps" :key="step.id">
                <v-row align="center">
                  <v-list-item-action>
                    <v-checkbox v-model="step['checked']"></v-checkbox>
                  </v-list-item-action>

                  <v-list-item-content>
                    <v-list-item-title v-text="step['text']"></v-list-item-title>
                  </v-list-item-content>
                  <!--<v-menu>
                      <template v-slot:activator="{ on }">
                        <v-btn dark icon v-on="on" class="icon" height="32">
                          <v-icon>mdi-dots-vertical</v-icon>
                        </v-btn>
                      </template>
                      <v-list>
                        <v-list-item v-for="(item, i) in step_actions" :key="i">
                          <v-list-item-title
                            @click.stop="openStepDialog(item.title, step.id)"
                          >{{ item.title }}</v-list-item-title>
                        </v-list-item>
                      </v-list>
                  </v-menu>-->
                </v-row>
              </v-list-item-group>
            </v-list>
            <v-text-field label="Step hinzufügen" :append-outer-icon="'mdi-plus'"></v-text-field>
            <small>*müssen ausgefüllt sein</small>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text class color="error" outlined @click="close()">Close</v-btn>
          <v-btn class="status" color="link" outlined text @click="confirm()">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>


<script>
import { mapState, mapGetters, mapActions } from "vuex";

export default {
  name: "DetailView",
  data: () => ({
    Storypoints: [0, 1, 2, 3, 5, 8, 13, 21, 34, 55],
    TaskData: {},

    selectedLabel: "", 

    //Dropdown der Step-Actions
    step_actions: [{ title: "Edit" }, { title: "Delete" }],

  }),

  created: function() {
    this.$store.commit("hideDetailView");
    this.fetchData();
    this.TaskData = this.task;
  },

  mounted: function() {
    this.TaskData = this.task;
    this.fetchData();
    setInterval(
      function() {
        this.fetchData();
      }.bind(this),
      10000
    );
  },

  computed: {
    ...mapState({
      visible: "detailViewVisable",
      task: "detailTask"
    }),
    ...mapGetters("label", {
      labelList: "list"
    })
  },

  methods: {
    ...mapActions("label", {
      fetchLabel: "fetchList"
    }),
    ...mapActions("task", {
      updateTask: "update"
    }),

    fetchData() {
      return this.fetchLabel();
    },

    confirm() {
      this.saveTask();
      this.$store.commit("hideDetailView");
    },

    close() {
      this.$store.commit("hideDetailView");
    },

    addLabel() {
      this.TaskData.labels.push(
        this.labelList.find(item => item.title == this.selectedLabel)
      );
      console.log(this.TaskData.labels);
      this.updateTask({
        id: this.TaskData.id + "/",
        data: {
          labels: this.TaskData.labels
          /*id: this.TaskData.id,
          name: this.TaskData.name,
          description: this.TaskData.description,
          storypoints: this.TaskData.storypoints,

          status: this.TaskData.status,
          lane: this.TaskData.lane,
          sprint: this.TaskData.sprint,
          feature: this.TaskData.feature,
          labels: this.TaskData.labels,
          steplists: this.TaskData.steplists*/
        }
      });
    },

    saveTask(){
      this.updateTask({
        id: this.TaskData.id + "/",
        data: {
          id: this.TaskData.id,
          name: this.TaskData.name,
          description: this.TaskData.description,
          storypoints: this.TaskData.storypoints,
          status: this.TaskData.status,
          lane: this.TaskData.lane,
          sprint: this.TaskData.sprint,
          feature: this.TaskData.feature,
          labels: this.TaskData.labels,
          //steplists: this.TaskData.steplists
        }

      });
    }
  },

  watch: {
    $route: "fetchData"
  }
};
</script>