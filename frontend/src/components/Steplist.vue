<template>
  <v-layout row wrap>
    <v-flex text-xs-center>
      <v-card>
        <v-list class="pa-0">
          <v-list-item>
            <v-list-item-action>
              <v-checkbox
                :input-value="allChecked"
                @change="toggleAll(!allChecked)"
                color="primary"
                v-if="steps.length > 0"
              ></v-checkbox>
              <v-icon color="primary" v-else>mdi-playlist-check</v-icon>
            </v-list-item-action>
            <v-text-field
              :label="'New step input'"
              @keydown.enter="addTodo"
              autofocus
              autocomplete="off"
              clearable
              color="primary"
              text
              hide-details
              maxlength="1023"
              placeholder="What needs to be checked?"
              solo
              v-model="newTodo"
            ></v-text-field>
          </v-list-item>
        </v-list>
      </v-card>
      <!-- main -->
      <v-card class="mt-3" v-show="steps.length">
        <v-progress-linear class="my-0" v-model="progressPercentage" />
        <v-card-actions class="px-3" v-show="steps.length">
          <span class="primary--text">
            {{ remaining }} {{ remaining | pluralize("item") }} left
          </span>
          <v-spacer></v-spacer>
        </v-card-actions>
        <v-list class="pa-0">
          <template v-for="step in steps">
            <v-divider :key="`${step.numbering}-divider`"></v-divider>
            <Step
              :key="`${step.numbering}-step`"
              v-bind:step="step"
              @fetch-steplist="fetchMyData()"
              @fetch-step="fetchStep($event)"
            />
          </template>
        </v-list>
      </v-card>
      <v-btn
        @click="clearCompleted"
        block
        class="mt-3"
        color="primary"
        depressed
        rounded
        v-show="steps.length > remaining"
      >
        Clear completed
      </v-btn>
    </v-flex>
  </v-layout>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import Step from "@/components/Step.vue";
export default {
  props: ["steplistId"],
  components: {
    Step,
  },
  data() {
    return {
      newTodo: "",
      steps: [],
    };
  },
  computed: {
    todos() {
      return this.$store.state.todos;
    },
    allChecked() {
      return this.steps.every((step) => step.checked);
    },
    remaining() {
      return this.steps.filter((step) => !step.checked).length;
    },
    progressPercentage() {
      const len = this.steps.length;
      return ((len - this.remaining) * 100) / len;
    },
    ...mapGetters("step", {
      stepById: "byId",
      stepByIdArray: "byIdArray",
    }),
    ...mapGetters("steplist", {
      steplistById: "byId",
    }),
  },
  methods: {
    getSteps() {
      var steplist;
      var steplistitems = [];
      steplist = this.steplistById(this.steplistId);
      if (steplist === undefined) {
        this.fetchMyData();
      } else {
        steplistitems = this.stepByIdArray(steplist.steplistitem_set);
      }
      return steplistitems;
    },
    compare(a, b) {
      // Use toUpperCase() to ignore character casing
      const numA = a.numbering;
      const numB = b.numbering;

      let comparison = 0;
      if (numA > numB) {
        comparison = 1;
      } else if (numA < numB) {
        comparison = -1;
      }
      return comparison;
    },
    toggleAll(value) {
      this.steps.forEach((step) => {
        this.updateStep({
          id: step.id,
          data: {
            checked: value,
          },
          customUrlFnArgs: {},
        }).then(() => this.fetchMyData());
      });
    },
    clearCompleted() {
      this.steps.forEach((step) => {
        if (step.checked) {
          this.deleteStep({
            id: step.id,
            customUrlFnArgs: { steplistId: null },
          }).then(() => this.fetchMyData());
        }
      });
    },
    addTodo() {
      const text = this.newTodo.trim();
      this.createStep({
        data: {
          text: text,
          checked: false,
          steplist: this.steplistId,
          numbering: this.steps.length,
        },
        customUrlFnArgs: {},
      }).then(() => this.fetchMyData());

      //prepare for new step
      this.newTodo = "";
    },
    fetchMyData() {
      this.fetchSteplist({ id: this.steplistId }).then(() => {
        this.steps = this.getSteps().sort(this.compare);
      });
      this.fetchSteps({
        customUrlFnArgs: { steplistId: this.steplistId },
      }).then(() => {
        this.steps = this.getSteps().sort(this.compare);
      });
    },
    fetchStep(stepId) {
      this.fetchStep({
        id: stepId,
        customUrlFnArgs: { steplistId: null },
      }).then(() => {
        this.steps = this.getSteps();
      });
    },
    ...mapActions("steplist", {
      fetchSteplistList: "fetchList",
      fetchSteplist: "fetchSingle",
      createSteplist: "create",
      updateSteplist: "update",
      deleteSteplist: "destroy",
    }),
    ...mapActions("step", {
      fetchStep: "fetchSingle",
      fetchSteps: "fetchList",
      createStep: "create",
      updateStep: "update",
      deleteStep: "destroy",
    }),
  },
  filters: {
    pluralize: (n, w) => (n === 1 ? w : w + "s"),
    capitalize: (s) => s.charAt(0).toUpperCase() + s.slice(1),
  },
  mounted() {
    this.fetchMyData();
  },
};
</script>