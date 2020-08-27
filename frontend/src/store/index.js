import Vue from "vue";
import Vuex from "vuex";
//import axios from "axios";

Vue.use(Vuex);


export default new Vuex.Store({
  state: {
    detailViewVisable: false,

    username: "",


    Userinfo: {
      
      token: ""
    },
  },
  mutations: {
    showDetailView(state){
      state.detailViewVisable = true;
    },

    hideDetailView(state) {
      state.detailViewVisable = false;
    },

    increment(state) {
      state.count++;
    },

    setToken(state, token){
      state.Userinfo.token = token;
    },
    setUsername(state, username){
      state.username = username;
    }
    
  },
  actions: {

  },
  modules: {

  },
  getters: {
    getDetailStatus: state => state.detailViewVisable, 

    getToken: state => state.Userinfo.token,

    getUsername: state => state.username

  }
});

