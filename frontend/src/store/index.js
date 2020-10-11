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
      status: "",
      username: "",
      token: localStorage.getItem('token') || '',
      refreshToken: localStorage.getItem('refreshToken') || '',
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
    // login({ commit }, { token, user }) {
    //   commit("SET_TOKEN", token);
    //   commit("SET_USERNAME", user);
    //   // set auth header
    //   Axios.defaults.headers.common["Authorization"] = `Bearer ${this.$state.Userinfo.token}`;

    // },

    login({ commit }, credentials) {
      return new Promise((resolve, reject) => {
        commit('AUTH_REQUEST');
        Axios({
          method: "post",
          url: "o/token/",
          auth: {
            username: "ttLwLjOKoJWtm5NDRRfGbgfioDhS7hwGZ0iaAzzD",
            password: "SPWysYuxLcr4ju0ITzqKASIQObiWaaUQbKb4ofYgJTv2QmkFSqfgroR3GIOg1QH41okgg0UHPh3gbTUiXuKKuj85Qy241hyBrn851v6eTVOpRujVWzZZP3npTki1Znnc"
          },
          data:
            "grant_type=password&username=" + credentials.username + "&password=" + credentials.password + "&scope=write"
        })
          .then(resp => {
            const token = resp.data.access_token;
            const refreshToken = resp.data.refresh_token;
            console.log(credentials);
            const user = credentials.username;
            localStorage.setItem('token', token);
            localStorage.setItem('refreshToken', refreshToken);
            Axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
            commit('AUTH_SUCCESS', { token, refreshToken, user });
            resolve(resp);
          })
          .catch(err => {
            commit('AUTH_ERROR');
            localStorage.removeItem('token');
            localStorage.removeItem('refreshToken');
            reject(err);
          })
      })
    },
    logout({ commit }) {
      return new Promise((resolve) => {
        commit('LOGOUT');
        localStorage.removeItem('token');
        localStorage.removeItem('refreshToken');
        delete Axios.defaults.headers.common['Authorization'];
        resolve();
      })
    }
  },
  //Update States (sync)
  mutations: {
    showDetailView(state) {
      state.detailViewVisable = true;
    },

    hideDetailView(state) {
      state.detailViewVisable = false;
    },

    showTaskDetail(state, withCreate) {
      state.selectedTask.visableDetail = true;
      if (!(withCreate === undefined)) {
        state.selectedTask.visableCreate = withCreate;
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

    // User login and logout
    AUTH_REQUEST(state) {
      state.Userinfo.status = "loading";
    },
    AUTH_SUCCESS(state, { token, refreshToken, user }) {
      state.Userinfo.status = "success";
      state.Userinfo.token = token;
      state.Userinfo.refreshToken = refreshToken;
      state.Userinfo.username = user;
    },
    AUTH_ERROR(state) {
      state.Userinfo.status = "error";
    },
    LOGOUT(state) {
      state.Userinfo.status = "";
      state.Userinfo.token = "";
      state.Userinfo.refreshToken = "";
      state.Userinfo.username = "";
    },

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

    getUserinfo: state => {
      return state.Userinfo;
    },

    isLoggedIn: state => {
      return !!state.Userinfo.token;
    },
    authStatus: state => {
      return state.Userinfo.status;
    },

    projectUsersbyIdArrayWithDetails: state => {
      return function(idArray){
        let resultArray = [];
        if(idArray !== undefined && state.projectRole.entities !== undefined && state.projectUser.entities !== undefined){
          idArray.map(id => state.projectUser.entities[id.toString()]).forEach(projectUser => {
            resultArray.push({
              id: projectUser.id,
              role: state.projectRole.entities[projectUser.role],
              plattform_user: state.user.entities[projectUser.plattform_user],
              project: projectUser.project,
            })
          });
        }
        console.log(resultArray);
        return resultArray.sort((a, b) =>
          a.plattform_user.username.localeCompare(b.plattform_user.alt)
        );

      }
    },

    plattformUsersbyIdArrayWithDetails: (state, rootGetters) => {
      return function(idArray, projectId){
        let resultArray = [];
        if(idArray !== undefined && state.projectRole.entities !== undefined && state.projectUser.entities !== undefined && state.user.entities !== undefined){
          idArray.map(id => state.user.entities[id]).forEach( user => {
            var projectUsers = rootGetters["projectUser/list"];
            
            var projectUserArray = projectUsers.filter(projectUser => projectUser.plattform_user == user.id && projectUser.project == projectId);
            var projectUser = null;
            if (projectUserArray.length == 1) {
              projectUser = projectUserArray.shift();
            }
            projectUser ? state.projectRole.entities[projectUser.role]: null;
            resultArray.push({
              id: user.id,
              role: "",
              plattform_user: user,
              project: projectId,
            })
          })
        }
        console.log(resultArray);
        return resultArray.sort((a, b) =>
          a.plattform_user.username.localeCompare(b.plattform_user.alt)
        );
      }
    }


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

