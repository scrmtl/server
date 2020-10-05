<template>
  <div>
    <v-navigation-drawer
      v-model="visible"
      left
      fixed
      width="800"
      color="tabbody"
      :retain-focus="Boolean(false)"
      scrollable
    >
      <v-container>
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
              <v-list subheader flat>
                <v-subheader>Stepliste</v-subheader>
                <v-list-item-group>
                  <v-list-item v-for="step in steplist" :key="step.id">
                    <v-list-item-action>
                      <v-checkbox color="primary" v-model="step.checked"></v-checkbox>
                    </v-list-item-action>
                    <v-list-item-content class="mt-2">
                      <v-list-item-title v-text="step.title"></v-list-item-title>
                    </v-list-item-content>
                    <v-list-item-action>
                      <v-icon color="error" @click.stop="deleteStep(step.id)">mdi-delete</v-icon>
                    </v-list-item-action>
                  </v-list-item>
                </v-list-item-group>
              </v-list>
              <v-text-field
                label="Step hinzufügen"
                :append-outer-icon="'mdi-plus'"
                v-model="newStep"
                @click:append-outer="addStep()"
              ></v-text-field>
              <small>*müssen ausgefüllt sein</small>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-btn color="error" absolute left outlined @click="deleteDialog = true">
              <v-icon left>mdi-delete</v-icon>
              <span class="pa-0">Löschen</span>
            </v-btn>
            <v-spacer></v-spacer>
            <v-btn class color="tabbody" outlined @click="close()">ABBRECHEN</v-btn>
            <v-btn class="status" color="tabbody" outlined @click="confirm()">SPEICHERN</v-btn>
          </v-card-actions>
        </v-card>
      </v-container>
    </v-navigation-drawer>
    <v-dialog v-model="deleteDialog" persistent class="mx-auto" width="600" dark>
      <v-card color="tabbody" shaped>
        <v-card-text class="headline pt-10">
          <span class="ml-12">Möchten Sie den Task wirklich löschen?</span>
        </v-card-text>
        <v-card-actions class="ml-10 pb-10 pt-10">
          <v-btn width="250" outlined color="error" @click="deleteTask()">Ja</v-btn>
          <v-btn width="250" outlined color="primary" @click="deleteDialog = false">Nein</v-btn>
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
    detaildrawer: null,
    tab: null,
    selectedLabel: "",
    deleteDialog: false,
    settings: [],
    newStep: "",

    steplist: [
      {
        id: 1,
        title: "test 123",
        checked: false
      },
      {
        id: 2,
        title: "test kjdfkl",
        checked: true
      }
    ],

    //Dropdown der Step-Actions
    step_actions: [{ title: "Edit" }, { title: "Delete" }]
  }),

  created: function() {
    this.$store.commit("hideDetailView");
    this.fetchData();
    this.TaskData = this.task;
  },

  updated: function() {
    this.TaskData = this.task;
    //   this.fetchData();
    //   setInterval(
    //     function() {
    //       this.fetchData();
    //     }.bind(this),
    //     10000
    //   );
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
      updateTask: "update",
      deleteTa: "destroy"
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

    saveTask() {
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
          labels: this.TaskData.labels
          // steplists: this.TaskData.steplists
        }
      });
    },

    deleteTask() {
      this.deleteDialog = false;
      this.deleteTa({
        id: this.TaskData.id + "/"
      });
      this.close();
    },

    deleteStep(id) {
      this.steplist.splice(id-1, 1);
    },

    addStep() {
      this.steplist.push({
        id: this.steplist.length+1,
        title: this.newStep,
        checked: false
      });
    }
  },

  watch: {
    $route: "fetchData"
  }
};
</script>