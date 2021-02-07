import Vue from "vue";
import Vuex from "vuex";
import Axios from "axios";
import createPersistedState from "vuex-persistedstate";
// mutation function from the `vuex-map-fields` module.
import { getField, updateField } from "vuex-map-fields";
// import * as Cookies from "js-cookie";
import board from "@/store/ressources/board";
import epic from "@/store/ressources/epic";
import feature from "@/store/ressources/feature";
import label from "@/store/ressources/label";
import lane from "@/store/ressources/lane";
import projectUser from "@/store/ressources/projectUser";
import sprint from "@/store/ressources/sprint";
import steplist from "@/store/ressources/steplist";
import step from "@/store/ressources/step";
import task from "@/store/ressources/task";
import user from "@/store/ressources/user";
import project from "@/store/ressources/project";
import session from "@/store/ressources/session";
import projectRole from "@/store/ressources/projectRole";
import registration from "@/store/ressources/registration";
import group from "@/store/ressources/group";
import selected from "@/store/ressources/selected";
import pokerVote from "@/store/ressources/Poker/pokerVote";
import pokerVoting from "@/store/ressources/Poker/pokerVoting";
import vote from "@/store/ressources/Poker/vote";
import poker from "@/store/ressources/poker"; // Legacy
import sprintStatistics from "@/store/ressources/sprintStatistics";
import projectStatistics from "@/store/ressources/projectStatistics";

Vue.use(Vuex, Axios);

const baseUrlDefault = "https://scrmtl.ddns.net";
//const baseUrlDefault = "http://192.168.178.48:14444";
Axios.defaults.baseURL = process.env.VUE_APP_BASE_URL || baseUrlDefault;

export default new Vuex.Store({
  // for debugging
  // later something like this even better
  // strict: eprocess.env.NODE_ENV !== "production"
  strict: true,
  // save vuex store in LocalStorage of browser
  plugins: [createPersistedState()],
  // save vuex store as cookie, but cookie is too big
  // plugins: [
  //   createPersistedState({
  //     storage: {
  //       getItem: (key) => Cookies.get(key),
  //       // Please see https://github.com/js-cookie/js-cookie#json, on how to handle JSON.
  //       setItem: (key, value) =>
  //         Cookies.set(key, value, { expires: 3, secure: false }),
  //       removeItem: (key) => Cookies.remove(key),
  //     },
  //   }),
  // ],
  // States
  state: {
    Userinfo: {
      status: "",
      username: "",
      userId: "",
      name: "",
      email: "",
      groups: [],
      token: "",
      refreshToken: "",
    },

    systemAlert: {
      visible: false,
      linkVisible: false,
      linkName: "Home",
      linkDestination: "Home",
      message: "",
      category: "info",
    },

    navigation: {
      visable: false,
    },
  },
  // call REST API (async)
  // Use from the components
  actions: {
    login({ commit, dispatch }, credentials) {
      return new Promise((resolve, reject) => {
        commit("AUTH_REQUEST");
        Axios({
          method: "post",
          url: "o/token/",
          auth: {
            username: "ttLwLjOKoJWtm5NDRRfGbgfioDhS7hwGZ0iaAzzD",
            password:
              "SPWysYuxLcr4ju0ITzqKASIQObiWaaUQbKb4ofYgJTv2QmkFSqfgroR3GIOg1QH41okgg0UHPh3gbTUiXuKKuj85Qy241hyBrn851v6eTVOpRujVWzZZP3npTki1Znnc",
          },
          data:
            "grant_type=password&username=" +
            credentials.username +
            "&password=" +
            credentials.password +
            "&scope=write",
        })
          .then(async (resp) => {
            const token = resp.data.access_token;
            const refreshToken = resp.data.refresh_token;
            // const user = credentials.username;
            // localStorage.setItem("token", token);
            // localStorage.setItem("refreshToken", refreshToken);
            Axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
            await dispatch("session/fetchList", {
              id: null,
              customUrlFnArgs: { all: false },
            }).then((res) => {
              var session = Object.values(res.data)[0];
              commit("AUTH_SUCCESS", {
                token: token,
                refreshToken: refreshToken,
                user: session.username,
                id: session.id,
                name: session.name,
                email: session.email,
                groups: session.groups,
              });
              resolve();
            });
            resolve();
          })
          .catch((err) => {
            commit("AUTH_ERROR");
            // localStorage.removeItem("token");
            // localStorage.removeItem("refreshToken");
            reject(err);
          });
      });
    },
    logout({ commit }) {
      return new Promise((resolve) => {
        commit("LOGOUT");
        // localStorage.removeItem("token");
        // localStorage.removeItem("refreshToken");
        delete Axios.defaults.headers.common["Authorization"];
        resolve();
      });
    },
  },
  //Update States (sync)
  mutations: {
    updateField,

    showNavigation(state) {
      state.navigation.visable = true;
    },

    hideNavigation(state) {
      state.navigation.visable = false;
    },

    showSystemAlert(
      state,
      {
        message,
        category = "info",
        link = false,
        linkName = "Poker",
        linkDestination = "PlanningPoker",
      }
    ) {
      state.systemAlert.visible = true;
      if (message.length > 100) {
        state.systemAlert.message = message;
      } else {
        state.systemAlert.message = message;
      }
      if (link) {
        state.systemAlert.linkName = linkName;
        state.systemAlert.linkDestination = linkDestination;
        state.systemAlert.linkVisible = true;
      }
      state.systemAlert.category = category;
    },
    hideSystemAlert(state) {
      state.systemAlert.visible = false;
      state.systemAlert.message = "";
      state.systemAlert.category = "info";
      state.systemAlert.linkName = "Home";
      state.systemAlert.linkDestination = "Home";
      state.systemAlert.linkVisible = false;
    },

    // User login and logout
    AUTH_REQUEST(state) {
      state.Userinfo.status = "loading";
    },
    AUTH_SUCCESS(
      state,
      { token, refreshToken, user, id, email, name, groups }
    ) {
      state.Userinfo.status = "success";
      state.Userinfo.token = token;
      state.Userinfo.refreshToken = refreshToken;
      state.Userinfo.username = user;
      state.Userinfo.userId = id;
      state.Userinfo.name = name;
      state.Userinfo.email = email;
      state.Userinfo.groups = groups;
    },
    AUTH_ERROR(state) {
      state.Userinfo.status = "error";
      state.Userinfo.token = "";
      state.Userinfo.refreshToken = "";
    },
    LOGOUT(state) {
      state.Userinfo.status = "";
      state.Userinfo.token = "";
      state.Userinfo.refreshToken = "";
      state.Userinfo.username = "";
      state.Userinfo.userId = "";
      state.Userinfo.name = "";
      state.Userinfo.email = "";
      state.Userinfo.groups = [];
    },
  },
  getters: {
    getField,

    getToken: (state) => {
      return state.Userinfo.token;
    },

    getUserinfo: (state) => {
      return state.Userinfo;
    },

    isLoggedIn: (state) => {
      return !!state.Userinfo.token;
    },
    authStatus: (state) => {
      return state.Userinfo.status;
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
    selected,
    sprintStatistics,
    projectStatistics,
    poker,
    vote,
    pokerVote,
    pokerVoting,
  },
});
