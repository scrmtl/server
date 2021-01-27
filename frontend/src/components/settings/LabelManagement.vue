<template>
  <v-list
    three-line
    subheader
    dark
    color="tabbody"
  >
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
              <v-dialog
                v-model="editedDialog"
                persistent
                max-width="500"
              >
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
                  <v-card-text>
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
                    <v-btn
                      color="white"
                      text
                      @click="close"
                    >
                      Cancel
                    </v-btn>
                    <v-btn
                      color="link"
                      text
                      @click="save"
                    >
                      Save
                    </v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </v-toolbar>
          </template>
          <template v-slot:[`item.color`]="{ item }">
            <v-btn
              rounded
              plain
              :color="item.color"
            ></v-btn>
          </template>
          <template v-slot:[`item.actions`]="{ item }">
            <v-icon
              small
              class="mr-2"
              @click="editLabel(item)"
            >
              mdi-pencil
            </v-icon>
            <v-icon
              small
              @click="deleteLabel(item)"
            >
              mdi-delete
            </v-icon>
            </template>
        </v-data-table>
      </v-list-item-content>
    </v-list-item>
  </v-list> 
</template>

<script>
import { mapActions, mapGetters } from "vuex";
export default {
  name: "LabelManagement",
  data: () =>({
    colorPicker: false,
    editedDialog: false,
    editedIndex: -1,
    editedLabel: {
        id: 0,
        title: "",
        color: "#A5D6A7"
    },
    defaultLabel: {
        id: 0,
        title: "",
        color: "#A5D6A7"
    },
    headers: [
      {
        text: 'ID',
        align: 'start',
        value: 'id',
      },
      { 
        text: 'Text',
        value: 'title' 
      },
      { 
        text: 'Color',
        value: 'color' 
      },
      { 
        text: 'Actions',
        value: 'actions',
        sortable: false 
      },
    ],
    swatches: [
      ["#EF9A9A", "#9fa8da", "#90CAF9"],
      ["#81d4fa", "#80deea", "#A5D6A7"]
    ],
  }),
  computed:{
    ...mapGetters("label", {
      listLabels: "list"
    }),
    formTitle() {
      return this.editedIndex === -1 ? 'New label' : 'Edit label'
    },

  },
  methods:{
    ...mapActions("label", {
      fetchLabel: "fetchList",
      fetchSingleLabel: "fetchSingle",
      updateLabel: "update",
      deleteLabel: "destroy",
      createLabel: "create"
    }),
    editLabel(item) {
        this.editedIndex = this.listLabels.indexOf(item)
        this.editedLabel = Object.assign({}, item)
        this.editedDialog = true
    },

    deleteLabel(item) {
      this.editedIndex = this.listLabels.indexOf(item)
      this.editedLabel = Object.assign({}, item)
      this.editedDialog = true
    },

    save () {
      if (this.editedIndex > -1) {
        console.log("edit")
        // Object.assign(this.desserts[this.editedIndex], this.editedItem)
      } else {
        console.log("new")
        // this.desserts.push(this.editedItem)
      }
      this.close();
    },

    close () {
      this.editedDialog = false;
      this.$nextTick(() => {
        this.editedLabel = Object.assign({}, this.defaultLabel)
        this.editedIndex = -1;
      })
    },
  }
}
</script>

<style>

</style>