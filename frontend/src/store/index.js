import Vue from "vue";
import Vuex from "vuex";
import Axios from "axios";
import createPersistedState from "vuex-persistedstate";

import board from '@/store/ressources/board';
import epic from '@/store/ressources/epic';
import feature from '@/store/ressources/feature';
import label from '@/store/ressources/label';
import lane from '@/store/ressources/lane';
import projectUser from '@/store/ressources/projectUser';
import sprint from '@/store/ressources/sprint';
import steplist from '@/store/ressources/steplist';
import step from '@/store/ressources/step';
import task from '@/store/ressources/task';
import user from '@/store/ressources/user';
import project from '@/store/ressources/project';
import session from '@/store/ressources/session';
import projectRole from '@/store/ressources/projectRole';
import registration from '@/store/ressources/registration';
import group from '@/store/ressources/group';

Vue.use(Vuex, Axios);

const baseUrlDefault = "https://scrmtl.ddns.net";
//const baseUrlDefault = "http://192.168.178.48:14444";
Axios.defaults.baseURL = process.env.VUE_APP_BASE_URL || baseUrlDefault

export default new Vuex.Store({
  // for debugging 
  // later something like this even better 
  // strict: eprocess.env.NODE_ENV !== 'production'
  strict: true,
  plugins: [createPersistedState()],
  // States
  state: {
    detailViewVisable: false,
    detailTask: {},
    Userinfo: {
      username: "",
      token: ""
    },

    selectedProject: {
      visableDetail: false,
      visableCreate: false,
      details: {},
    },
    selectedTask: {
      visableDetail: false,
      visableCreate: false,
      details: {},
    },
    selectedBoard: {}
  },
  // call REST API (async)
  // Use from the components
  actions: {
    login({ commit }, { token, user }) {
      commit("SET_TOKEN", token);
      commit("SET_USERNAME", user);
      // set auth header
      Axios.defaults.headers.common["Authorization"] = `Bearer ${this.$state.Userinfo.token}`;

    },

    logout({ commit }) {
      commit("RESET", '');
    },
  },
  //Update States (sync)
  mutations: {
    showDetailView(state) {
      state.detailViewVisable = true;
    },

    hideDetailView(state) {
      state.detailViewVisable = false;
    },

    showTaskDetail(state, withCreate = false) {
      state.selectedTask.visableDetail = true;
      if (withCreate) {
        state.selectedTask.visableCreate = true;
      }
    },
    hideTaskDetail(state) {
      state.selectedTask.visableDetail = false;
      state.selectedTask.visableCreate = false;
      state.selectedTask.details = {};
    },
    setSelectedTaskDetail(state, task) {
      state.selectedTask.details = task;
    },

    showProjectDetail(state, withCreate = false) {
      state.selectedProject.visableDetail = true;
      if (withCreate) {
        state.selectedProject.visableCreate = true;
      }
    },

    hideProjectDetail(state) {
      state.selectedProject.visableDetail = false;
      state.selectedProject.visableCreate = false;
      state.selectedProject.details = {};
    },

    setSelectedProjectDetail(state, project) {
      state.selectedProject.details = project;
    },

    //Legacy
    setDetailTask(state, Task) {
      state.detailTask = Task;
    },


    increment(state) {
      state.count++;
    },
    // User login and logout
    SET_TOKEN(state, token) {
      state.Userinfo.token = token;
    },
    SET_USERNAME(state, username) {
      state.Userinfo.username = username;
    },
    RESET(state) {
      state.Userinfo.username = "";
      state.Userinfo.token = "";
    },
    // SET_PROJECTS(state, projects) {
    //   state.projects = projects;
    // },
    // NEW_PROJECT(state, project) {
    //   state.projects.unshift(project);
    // },
    // UPDATE_PROJECT(state, updatedProject) {
    //   const index = state.projects.findIndex(t => t.id === updatedProject.id);
    //   if (index !== -1) {
    //     state.tasks.splice(index, 1, updatedProject);
    //   }
    // },
    // DELETE_PROJECT(state, project) {
    //   state.projects = state.projects.filter(prj => project.id !== prj.id);
    // }

  },
  getters: {
    getDetailStatus: state => {
      return state.detailViewVisable;
    },
    getProjectDetailStatus: state => {
      return state.selectedProject.visableDetail;
    },
    getTaskDetailStatus: state => {
      return state.selectedTask.visableDetail;
    },

    getToken: state => {
      return state.Userinfo.token;
    },

    getUsername: state => {
      return state.Userinfo.username;
    },
  },
  modules: {
    task,
    board,
    epic,
    feature,
    label,
    lane,
    projectUser,
    sprint,
    steplist,
    user,
    project,
    session,
    projectRole,
    registration,
    group,
    step,
  }
});

