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
export default {
  props: {
    task: Object
  },
  data: () => ({
    activator: null,
    attach: null,
    colors: ["#EF9A9A", "#9fa8da", "#90CAF9", "##81d4fa", "#80deea", "#A5D6A7"],
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

  watch: {
    model(val, prev) {
      if (val.length === prev.length) return;
      this.model = val
        //skip adding label if it is newly created
        //-> Promise is going to add it after with response of backend
        .filter(v => {
          if (typeof v === "string") {
            v = {
              text: v,
              color: this.colors[this.nonce - 1]
            };
            this.createLabel({ data: { title: v.text, color: v.color } }).then(
              function(value) {
                //add label to local label stack
                var label = value.data;
                label["text"] = label.title;
                this.items.push(label);
                this.model.push(label);
                //add label to task in backend
                var labelIds = this.task.labels;
                labelIds.push(label.id);
                this.updateTask({
                  id: this.task.id,
                  data: { labels: labelIds }
                }).then(
                  function(value) {
                    var task = value.data;
                    this.fetchTask({ id: task.id });
                  }.bind(this)
                );
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
    }
  },

  methods: {
    ...mapActions("label", {
      fetchLabels: "fetchList",
      updateLabel: "update",
      createLabel: "create"
    }),
    ...mapActions("task", {
      fetchTask: "fetch",
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
      console.log("filter called; item: " + item + queryText + itemText);
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
    fetchAll() {
      this.fetchLabels()
        .catch(error => {
          this.fetchErrors.push(error);
        })
        .then(() => {
          this.listLabels.forEach(label => {
            //do not use title instead of text. v-combobox needs a text property
            label["text"] = label.title;
            this.items.push(label);
          });
          this.fillTaskLabels(this.task);
        });
      this.fetchTask({ id: this.task.id });
    },
    fillTaskLabels(task) {
      task.labels.forEach(labelId => {
        this.model.push(this.labelById(labelId));
      });
      var labelIds = [];
      task.labels.forEach(label => {
        labelIds.push(label.id);
      });
    }
  },
  computed: {
    ...mapGetters("label", {
      listLabels: "list",
      labelById: "byId"
    })
  },
  created() {
    this.fetchAll();
  }
};
</script>