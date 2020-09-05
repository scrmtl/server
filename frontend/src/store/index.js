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

// const baseUrl = "https://scrmtl.ddns.net/api";
const baseUrlDefault = "https://scrmtl.ddns.net";
// const projectPath = "/project/";

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

    projects: []
  },
  // call REST API
  // Use from the components
  actions: {
    login({ commit }, { token, user }) {
      commit("SET_TOKEN", token);
      commit("SET_USERNAME", user);
      // set auth header
      Axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
      Axios.defaults.baseURL = process.env.VUE_APP_BASE_URL || baseUrlDefault
    },

    logout({ commit }) {
      commit("RESET", '');
    },

    //Project
    // async fetchProjects({ commit }) {
    //   const response = await Axios.get(`${baseUrl}${projectPath}`);
    //   commit("SET_PROJECTS", response.data);
    // },
    // async addProject({ commit }, project) {
    //   const response = await Axios.post(`${baseUrl}${projectPath}`, project);
    //   commit("NEW_PROJECT", response.data);
    // },
    // async updateProject({ commit }, project) {
    //   const response = await Axios.put(`${baseUrl}${projectPath}${project.id}`, project);
    //   commit("UPDATE_PROJECT", response.data);
    // },
    // async removeProject({ commit }, project) {
    //   await Axios.delete(`${baseUrl}${projectPath}${project.id}`);
    //   commit("DELETE_PROJECT", project);
    // }
  },
  //Update States
  mutations: {
    showDetailView(state) {
      state.detailViewVisable = true;
    },

    hideDetailView(state) {
      state.detailViewVisable = false;
    },

    setDetailTask(state, Task){
      state.detailTask = Task;
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

    getToken: state => {
      return state.Userinfo.token;
    },

    getUsername: state => {
      return state.Userinfo.username;
    },

    // getProjects: state => {
    //   return state.projects;
    // }
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

