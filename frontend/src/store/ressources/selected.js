import { getField, updateField } from 'vuex-map-fields';

const state = () => ({
  project: {
    visableDetail: false,
    visableCreate: false,
    details: {},
  },
  sprint: {
    visableDetail: false,
    visableCreate: false,
    readOnly: false,
    details: {},
  },
  task: {
    visableDetail: false,
    visableCreate: false,
    readOnly: false,
    details: {},
  }
});

const mutations = {
  updateField,

  showProjectDetail(state, withCreate = false) {
    state.project.visableDetail = true;
    if (withCreate) {
      state.project.visableCreate = true;
      // Set Default values of nessessary data
      state.project.details = {
        name: "",
        start:"",
        end: "",
        sprint_duration: 0
      }
    }
  },
  hideProjectDetail(state) {
    state.project.visableDetail = false;
    state.project.visableCreate = false;
    state.project.details = {};
  },
  
  setProjectDetail(state, project) {
    state.project.details = project;
  },

  showSprintDetail(state, withCreate = false) {
    state.sprint.visableDetail = true;
    if (withCreate) {
      state.sprint.visableCreate = true;
      // Set Default values of nessessary data
      state.sprint.details = {
        version: "",
        project: 0,
        story: ""
      };
    }
  },

  showSprintDetailWithReadOnly(state){
    state.sprint.visableDetail = true;
    state.sprint.readOnly = true;
  },

  hideSprintDetail(state) {
    state.sprint.visableDetail = false;
    state.sprint.visableCreate = false;
    state.sprint.readOnly = false;
    // state.sprint.details = {};
  },

  setSprintDetail(state, sprint) {
    state.sprint.details = sprint;
  },

  showTaskDetail(state, withCreate = false) {
    state.task.visableDetail = true;
    if (withCreate) {
      state.task.visableCreate = true;
      // Default values are set in lane (createTaskHelper)
    }
  },

  showTaskDetailWithReadOnly(state){
    state.task.visableDetail = true;
    state.task.readOnly = true;
  },

  hideTaskDetail(state) {
    state.task.visableDetail = false;
    state.task.visableCreate = false;
    state.task.readOnly = false;
    state.task.details = {};
  },

  setTaskDetail(state, task) {
    state.task.details = task;
  },
};

const getters = {
  getField
};


export default {
  // We're using namespacing
  // in all of our modules.
  namespaced: true,
  name: "selected",
  state,
  getters,
  mutations
};