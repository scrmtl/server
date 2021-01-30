<template>
  <v-list three-line subheader dark color="tabbody">
    <v-subheader class="subtitle-1">Label Management</v-subheader>
    <v-list-item>
      <v-list-item-content>
        <v-data-table
          :headers="headers"
          :items="listLabels"
          sort-by="title"
          class="tabbody"
        >
          <template v-slot:top>
            <v-toolbar flat class="tabbody">
              <v-dialog v-model="editedDialog" persistent max-width="500">
                <template v-slot:activator="{ on, attrs }">
                  <v-spacer></v-spacer>
                  <v-btn
                    color="link"
                    class="mb-2"
                    v-bind="attrs"
                    v-on="on"
                    small
                    outlined
                    >add label
                  </v-btn>
                </template>
                <!-- Add or edit Dialog -->
                <v-card class="tabbody" dark>
                  <v-card-title>
                    <span class="headline">{{ formTitle }}</span>
                  </v-card-title>
                  <v-card-text
                    class="overflow-y-auto"
                    style="height: calc(95vh - 250px)"
                  >
                    <v-row>
                      <v-text-field
                        label="Text"
                        v-model="editedLabel.title"
                      ></v-text-field>
                    </v-row>
                    <v-row>
                      <span style="font-size: 12px">Color</span>
                    </v-row>
                    <v-row justify="space-around">
                      <v-color-picker
                        class="ma-2"
                        show-swatches
                        v-model="editedLabel.color"
                        swatches-max-height="150"
                        :swatches="swatches"
                      ></v-color-picker>
                    </v-row>
                  </v-card-text>
                  <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="white" text @click="close()"> Cancel </v-btn>
                    <v-btn color="link" text @click="save()"> Save </v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
              <v-dialog
                v-model="deleteDialog"
                persistent
                class="mx-auto"
                width="600"
                dark
              >
                <v-card color="tabbody" shaped>
                  <v-card-text class="headline pt-10">
                    <span class="ml-12"
                      >Do you want to remove the selected label?</span
                    >
                  </v-card-text>
                  <v-card-actions class="ml-10 pb-10 pt-10">
                    <v-btn
                      width="250"
                      outlined
                      color="error"
                      @click="confirmDeleteLabel()"
                      >Yes</v-btn
                    >
                    <v-btn width="250" outlined @click="closeDeleteDialog()"
                      >No</v-btn
                    >
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </v-toolbar>
          </template>
          <template v-slot:[`item.color`]="{ item }">
            <v-btn rounded plain :color="item.color"></v-btn>
          </template>
          <template v-slot:[`item.actions`]="{ item }">
            <v-icon small class="mr-2" @click="editLabel(item)">
              mdi-pencil
            </v-icon>
            <v-icon small @click="deleteLabel(item)"> mdi-delete </v-icon>
          </template>
        </v-data-table>
      </v-list-item-content>
    </v-list-item>
  </v-list>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import { mapFields } from "vuex-map-fields";
export default {
  name: "LabelManagement",
  data: () => ({
    colorPicker: false,
    editedDialog: false,
    deleteDialog: false,
    editedIndex: -1,
    editedLabel: {
      id: 0,
      title: "",
      color: "#A5D6A7",
    },
    defaultLabel: {
      id: 0,
      title: "",
      color: "#A5D6A7",
    },
    headers: [
      {
        text: "ID",
        align: "start",
        value: "id",
      },
      {
        text: "Text",
        value: "title",
      },
      {
        text: "Color",
        value: "color",
      },
      {
        text: "Actions",
        value: "actions",
        sortable: false,
      },
    ],
    swatches: [
      ["#EF9A9A", "#F48FB1", "#CE93D8"],
      ["#B39DDB", "#9FA8DA", "#90CAF9"],
      ["#81D4FA", "#80DEEA", "#80CBC4"],
      ["#A5D6A7", "#C5E1A5", "#E6EE9C"],
      ["#FFF59D", "#FFE082", "#FFCC80"],
      ["#FFAB91", "#BCAAA4", "#B0BEC5"],
    ],
  }),
  computed: {
    ...mapGetters("label", {
      listLabels: "list",
    }),
    // See more under Two-way Computed Property https://vuex.vuejs.org/guide/forms.html
    // Implementation with https://github.com/maoberlehner/vuex-map-fields
    // the string after the last dot (e.g. `id`) is used
    // for defining the name of the computed property.
    ...mapFields(["Userinfo.userId"]),
    formTitle() {
      return this.editedIndex === -1 ? "New label" : "Edit label";
    },
  },
  methods: {
    ...mapActions("label", {
      fetchLabels: "fetchList",
      fetchSingleLabel: "fetchSingle",
      updateLabel: "update",
      destroyLabel: "destroy",
      createLabel: "create",
    }),
    ...mapActions("task", {
      fetchTasks: "fetchList",
    }),
    editLabel(item) {
      this.editedIndex = this.listLabels.indexOf(item);
      this.editedLabel = Object.assign({}, item);
      this.editedDialog = true;
    },

    deleteLabel(item) {
      this.editedIndex = this.listLabels.indexOf(item);
      this.editedLabel = Object.assign({}, item);
      this.deleteDialog = true;
    },
    confirmDeleteLabel() {
      this.destroyLabel({
        id: this.editedLabel.id,
      }).then(() => {
        this.fetchTasks({
          customUrlFnArgs: { byUser: this.userId },
        });
        this.fetchLabels();
      });
      this.closeDeleteDialog();
    },

    save() {
      if (this.editedIndex > -1) {
        this.updateLabel({
          id: this.editedLabel.id,
          data: {
            title: this.editedLabel.title,
            color: this.editedLabel.color,
          },
        }).then(() => {
          this.fetchLabels();
        });
      } else {
        this.createLabel({
          data: {
            title: this.editedLabel.title,
            color: this.editedLabel.color,
          },
        }).then(() => {
          this.fetchLabels();
        });
      }
      this.close();
    },

    close() {
      this.editedDialog = false;
      this.$nextTick(() => {
        this.editedLabel = Object.assign({}, this.defaultLabel);
        this.editedIndex = -1;
      });
    },
    closeDeleteDialog() {
      this.deleteDialog = false;
      this.$nextTick(() => {
        this.editedIeditedLabeltem = Object.assign({}, this.defaultLabel);
        this.editedIndex = -1;
      });
    },
  },
};
</script>

<style></style>
