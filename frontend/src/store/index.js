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
import task from '@/store/ressources/task';
import user from '@/store/ressources/user';
import project from '@/store/ressources/project';

Vue.use(Vuex, Axios);

const baseUrlDefault = "https://scrmtl.ddns.net";
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
    detailProjectVisable: false,
    detailTask: {},
    detailProject: {},
    Userinfo: {
      username: "",
      token: ""
    },

    projects: [],
    selectedProject: {}
  },
  // call REST API
  // Use from the components
  actions: {
    login({ commit }, { token, user }) {
      commit("SET_TOKEN", token);
      commit("SET_USERNAME", user);
      // set auth header
      Axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;

    },

    logout({ commit }) {
      commit("RESET", '');
    },
  },
  //Update States
  mutations: {
    showDetailView(state) {
      state.detailViewVisable = true;
    },

    hideDetailView(state) {
      state.detailViewVisable = false;
    },

    showProjectDetail(state) {
      state.detailProjectVisable = true;
    },
    
    hideProjectDetail(state) {
      state.detailProjectVisable = false;
    },
    setDetailTask(state, Task){
      state.detailTask = Task;
    },
    setProjectDetail(state, ProjectDetail){
      state.detailProject = ProjectDetail;
    },

    increment(state) {
      state.count++;
    },

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
      return state.detailProjectVisable;
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
  }
});

