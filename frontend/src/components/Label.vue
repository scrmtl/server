<template>
  <v-container fluid>
    <v-combobox
      v-model="model"
      :filter="filter"
      :hide-no-data="!search"
      :items="items"
      :search-input.sync="search"
      hide-selected
      label="Labels"
      multiple
      chips
      outlined
      :disabled="status === 'DO' || status === 'AC'"
    >
      <template v-slot:no-data>
        <v-list-item>
          <span class="subheading">Create</span>
          <v-chip :color="`${colors[nonce - 1]} `" label small>
            {{ search }}
          </v-chip>
        </v-list-item>
      </template>
      <template v-slot:selection="{ attrs, item, parent, selected }">
        <v-chip
          v-if="item === Object(item)"
          v-bind="attrs"
          :color="`${item.color} `"
          :input-value="selected"
          label
        >
          <span class="pr-2"> {{ item.text }} id: {{ item.id }} </span>
          <v-icon small @click="parent.selectItem(item)"
            >mdi-close-circle</v-icon
          >
        </v-chip>
      </template>
      <template v-slot:item="{ index, item }">
        <v-text-field
          v-if="editing === item"
          v-model="editing.text"
          autofocus
          flat
          background-color="transparent"
          hide-details
          outlined
          @keyup.enter="edit(index, item)"
        ></v-text-field>
        <v-chip v-else :color="`${item.color}`" label small>
          {{ item.text }}
        </v-chip>
        <v-spacer></v-spacer>
        <v-list-item-action @click.stop.prevent="edit(index, item)">
          <v-btn icon>
            <v-icon>{{ editing !== item ? "mdi-pencil" : "mdi-check" }}</v-icon>
          </v-btn>
        </v-list-item-action>
      </template>
    </v-combobox>
  </v-container>
</template>


<script>
import { mapActions, mapGetters } from "vuex";
import { mapFields } from "vuex-map-fields";
export default {
  props: {

  },
  data: () => ({
    activator: null,
    attach: null,
    colors: ["#EF9A9A", "#9fa8da", "#90CAF9", "#81d4fa", "#80deea", "#A5D6A7"],
    editing: null,
    fetchErrors: [],
    index: -1,
    items: [{ header: "Select an label or create one" }],
    nonce: 1,
    menu: false,
    model: [],
    x: 0,
    search: null,
    y: 0
  }),

  computed:{
    ...mapFields("selected", [
      "task.details.id",
      "task.details.labels",
      "task.details.status",
    ]),
    ...mapGetters("label", {
      listLabels: "list",
      labelById: "byId"
    })
  },

  watch: {
    model(val, prev) {
      if (val.length === prev.length) return;
      //If new Label is created
      var updateLabel = true;
      this.model = val
        //skip adding label if it is newly created
        //-> Promise is going to add it after with response of backend
        .filter(v => {
          if (typeof v === "string") {
            updateLabel = false;
            v = {
              text: v,
              color: this.colors[this.nonce - 1]
            };
            this.createLabel({ data: { title: v.text, color: v.color } }).then(
              function(value) {
                //add label to local label stack
                if (value.data.id === undefined) return value;
                var label = value.data;
                label["text"] = label.title;
                this.items.push(label);
                this.model.push(label);
                //add label ID to task labels
                this.labels.push(value.data.id);
                return value;
              }.bind(this)
            );
            this.nonce++;
            return false;
          }
          return true;
        })
        .map(v => {
          return v;
        });
      //if no new label is created override labels in task with updated list
      if (updateLabel) {
        this.labels = val.map(label => label.id);
      }
    },
    id(val, prev) {
      if (val === prev) return;
      this.items = [{ header: "Select an label or create one" }];
      this.model = [];
      this.fetchAll(val, this.labels);
    }
  },

  methods: {
    ...mapActions("label", {
      fetchLabels: "fetchList",
      updateLabel: "update",
      createLabel: "create"
    }),
    ...mapActions("task", {
      fetchTask: "fetchSingle",
      updateTask: "update"
    }),
    edit(index, item) {
      if (!this.editing) {
        this.editing = item;
        this.index = index;
      } else {
        this.updateLabel({
          id: item.id,
          data: { title: item.text, color: item.color }
        });
        this.editing = null;
        this.index = -1;
      }
    },
    filter(item, queryText, itemText) {
      if (item.header) return false;

      const hasValue = val => (val != null ? val : "");

      const text = hasValue(itemText);
      const query = hasValue(queryText);

      return (
        text
          .toString()
          .toLowerCase()
          .indexOf(query.toString().toLowerCase()) > -1
      );
    },
    fetchAll(taskId, labels) {
      if (labels === undefined) return;
      this.fetchLabels({ customUrlFnArgs: {} })
        .catch(error => {
          this.fetchErrors.push(error);
          console.log("error");
          return error;
        })
        .then(value => {
          this.listLabels.forEach(label => {
            //do not use title instead of text. v-combobox needs a text property
            label["text"] = label.title;
            this.items.push(label);
          });
          this.fillTaskLabels(labels);
          return value;
        });
      this.fetchTask({ id: taskId, customUrlFnArgs: {} });
    },
    fillTaskLabels(labels) {
      labels.forEach(labelId => {
        this.model.push(this.labelById(labelId));
      });
      var labelIds = [];
      labels.forEach(label => {
        labelIds.push(label.id);
      });
    }
  }
};
</script>