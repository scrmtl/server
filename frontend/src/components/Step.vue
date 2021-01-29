<template>
  <v-list-item class="step-item" :class="{ editing: editing }">
    <v-list-item-action>
      <v-checkbox
        :input-value="step.checked"
        @change="toggleTodo(step)"
        color="primary"
        v-if="!editing"
      ></v-checkbox>
      <v-icon color="primary" v-else>mdi-pencil</v-icon>
    </v-list-item-action>
    <template v-if="!editing">
      <v-list-item-content
        :class="{ 'primary--text': step.checked }"
        @dblclick="editing = true"
      >
        {{ step.text }}
      </v-list-item-content>
      <v-list-item-action>
        <v-btn @click="removeTodo(step)" color="red lighten-3" text icon>
          <v-icon>mdi-close-circle</v-icon>
        </v-btn>
      </v-list-item-action>
    </template>
    <v-text-field
      :value="step.text"
      @blur="doneEdit"
      @keyup.enter="doneEdit"
      @keyup.esc="cancelEdit"
      clearable
      color="primary"
      flat
      hide-details
      maxlength="1023"
      ref="input"
      solo
      v-else
      v-focus="editing"
    ></v-text-field>
  </v-list-item>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
export default {
  props: ["step"],
  data() {
    return {
      editing: false,
    };
  },
  directives: {
    focus(el, { value }, { context }) {
      if (value) {
        context.$nextTick(() => {
          context.$refs.input.focus();
        });
      }
    },
  },
  methods: {
    editTodo({ step, value }) {
      this.updateStep({
        id: step.id,
        data: {
          checked: step.checked,
          text: value,
        },
        customUrlFnArgs: { steplistId: null },
      }).then(() => this.$emit("fetch-steplist"));
    },
    removeTodo(step) {
      this.deleteStep({
        id: step.id,
        customUrlFnArgs: { steplistId: null },
      }).then(() => this.$emit("fetch-steplist"));
    },
    toggleTodo(step) {
      this.updateStep({
        id: step.id,
        data: {
          checked: !step.checked,
        },
        customUrlFnArgs: {},
      }).then((response) => {
        this.$emit("fetch-steplist");
        return response;
      });
    },
    doneEdit(e) {
      const value = e.target.value.trim();
      const { step } = this;
      if (!value) {
        this.removeTodo(step);
      } else if (this.editing) {
        this.editTodo({
          step,
          value,
        });
        this.editing = false;
      }
    },
    cancelEdit() {
      this.editing = false;
    },
    ...mapActions("step", {
      fetchStep: "fetchSingle",
      fetchSteps: "fetchList",
      createStep: "create",
      updateStep: "update",
      deleteStep: "destroy",
    }),
  },
  computed: {
    ...mapGetters("step", {
      stepById: "byId",
      stepByIdArray: "byIdArray",
    }),
  },
};
</script>
