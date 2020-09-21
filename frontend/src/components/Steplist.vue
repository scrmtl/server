<template>
  <div>
    <v-list>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title>
            <v-text-field
              v-model="newStep"
              id="newStep"
              name="newStep"
              label="Type your task"
              @keyup.enter="addStep"
            />
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
    <v-list-item-group>
      <v-list-item v-for="(step) in getStepArray()" :key="step.numbering">
        <template #default="{ active }">
          <v-list-item-action>
            <v-checkbox v-model="step.checked" @change="updateStepEvent(step.id)"></v-checkbox>
          </v-list-item-action>

          <v-list-item-content>
            <v-list-item-title :class="{done: step.checked}">{{ step.text}}</v-list-item-title>
            <v-list-item-subtitle></v-list-item-subtitle>
          </v-list-item-content>
          <v-btn fab ripple small color="red" v-if="active" @click="removeStep(step.id)">
            <v-icon class="white--text">mdi-close</v-icon>
          </v-btn>
        </template>
      </v-list-item>
    </v-list-item-group>
  </div>
</template>
<script>
import { mapActions, mapGetters, mapMutations } from "vuex";
export default {
  data() {
    return {
      newStep: ""
    };
  },
  props: ["steplistId"],
  methods: {
    ...mapActions("steplist", {
      fetchSteplistList: "fetchList",
      fetchSteplist: "fetchSingle",
      createSteplist: "create",
      updateSteplist: "update",
      deleteSteplist: "destroy"
    }),
    ...mapActions("step", {
      fetchSteps: "fetchList",
      createStep: "create",
      updateStep: "update",
      deleteStep: "destroy"
    }),
    getStepArray() {
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
    removeStep(id) {
      this.deleteStep({
        id: id,
        customUrlFnArgs: { steplistId: null }
      }).then(() => this.fetchMyData());
    },
    addStep() {
      var value = this.newStep && this.newStep.trim();
      if (!value) {
        return;
      }
      this.createStep({
        data: {
          text: value,
          checked: false,
          steplist: this.steplistId,
          numbering: this.getStepArray().length
        },
        customUrlFnArgs: { steplistId: null }
      }).then(() => this.fetchMyData());

      //prepare for new step
      this.newStep = "";
    },
    fetchMyData() {
      this.fetchSteplist({ id: this.steplistId });
      this.fetchSteps({ customUrlFnArgs: { steplistId: this.steplistId } });
    },
    ...mapMutations({
      mutateUpdateStep: "updateStep"
    })
  },
  computed: {
    ...mapGetters("steplist", {
      steplistById: "byId"
    }),
    ...mapGetters("step", {
      stepById: "byId",
      stepByIdArray: "byIdArray"
    })
  },
  created() {
    this.fetchMyData();
  },
  updated() {}
};
</script>