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
          <span class="pr-2">
            {{ item.title }}
          </span>
          <v-icon small @click="parent.selectItem(item)"
            >mdi-close-circle</v-icon
          >
        </v-chip>
      </template>
      <template v-slot:item="{ index, item }">
        <v-text-field
          v-if="editing === item"
          v-model="editing.title"
          autofocus
          flat
          background-color="transparent"
          hide-details
          outlined
          @keyup.enter="edit(index, item)"
        ></v-text-field>
        <v-chip v-else :color="`${item.color}`" label small>
          {{ item.title }}
        </v-chip>
        <v-spacer></v-spacer>
        <v-list-item-action @click.stop>
          <v-btn icon @click.stop.prevent="edit(index, item)">
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
    colors: ["green", "purple", "indigo", "cyan", "teal", "orange"],
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

      this.model = val.map(v => {
        if (typeof v === "string") {
          v = {
            title: v,
            color: this.colors[this.nonce - 1]
          };

          this.items.push(v);

          this.nonce++;
        }

        return v;
      });
    }
  },

  methods: {
    ...mapActions("label", {
      fetchLabels: "fetchList"
    }),
    edit(index, item) {
      if (!this.editing) {
        this.editing = item;
        this.index = index;
      } else {
        this.editing = null;
        this.index = -1;
      }
    },
    filter(item, queryText, itemText) {
      console.log("filter called; item: " + item + queryText + itemText);
      if (item.header) return false;

      const hasValue = val => (val != null ? val : "");

      const title = hasValue(itemText);
      const query = hasValue(queryText);

      return (
        title
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
            this.items.push(label);
            this.model.push(label);
          });
        });
      console.log("label IDs: " + this.getLabelIds(this.Task));
    },
    getLabelIds(Task) {
      var labelIds = [];
      Task.labels.forEach(label => {
        labelIds.push(label.id);
      });
    }
  },
  computed: {
    ...mapGetters("label", {
      listLabels: "list"
    })
  },
  created() {
    this.fetchAll();
  }
};
</script>