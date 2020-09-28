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
          <v-chip
            :color="`${colors[nonce - 1]} lighten-3`"
            label
            small
          >
            {{ search }}
          </v-chip>
        </v-list-item>
      </template>
      <template v-slot:selection="{ attrs, item, parent, selected }">
        <v-chip
          v-if="item === Object(item)"
          v-bind="attrs"
          :color="`${item.color} lighten-3`"
          :input-value="selected"
          label
          
        >
          <span class="pr-2">
            {{ item.title }}
          </span>
          <v-icon
            small
            @click="parent.selectItem(item)"
          >mdi-close-circle</v-icon>
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
        <v-chip
          v-else
          :color="`${item.color} lighten-3`"
          
          label
          small
        >
          {{ item.title }}
        </v-chip>
        <v-spacer></v-spacer>
        <v-list-item-action @click.stop>
          <v-btn
            icon
            @click.stop.prevent="edit(index, item)"
          >
            <v-icon>{{ editing !== item ? 'mdi-pencil' : 'mdi-check' }}</v-icon>
          </v-btn>
        </v-list-item-action>
      </template>
    </v-combobox>
  </v-container>
</template>


<script>
  export default {
    data: () => ({
      activator: null,
      attach: null,
      colors: ['green', 'purple', 'indigo', 'cyan', 'teal', 'orange'],
      editing: null,
      index: -1,
      items: [
        { header: 'Select an label or create one' },
        {
          title: 'Foo',
          color: 'blue',
        },
        {
          title: 'Bar',
          color: 'red',
        },
      ],
      nonce: 1,
      menu: false,
      model: [
        {
          title: 'Foo',
          color: 'blue',
        },
      ],
      x: 0,
      search: null,
      y: 0,
    }),

    watch: {
      model (val, prev) {
        if (val.length === prev.length) return

        this.model = val.map(v => {
          if (typeof v === 'string') {
            v = {
              title: v,
              color: this.colors[this.nonce - 1],
            }

            this.items.push(v)

            this.nonce++
          }

          return v
        })
      },
    },

    methods: {
      edit (index, item) {
        if (!this.editing) {
          this.editing = item
          this.index = index
        } else {
          this.editing = null
          this.index = -1
        }
      },
      filter (item, queryText, itemText) {
        if (item.header) return false

        const hasValue = val => val != null ? val : ''

        const title = hasValue(itemText)
        const query = hasValue(queryText)

        return title.toString()
          .toLowerCase()
          .indexOf(query.toString().toLowerCase()) > -1
      },
    },

  }
</script>