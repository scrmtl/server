import Vue from "vue";
import Vuex from "vuex";
//import axios from "axios";

Vue.use(Vuex);


export default new Vuex.Store({
  state: {
<<<<<<< HEAD
    Userinfo: {
      username: "stephan",
      password: "scrmtl14444",
      token: ""
    },
    responseData:[],
        
=======
    detailViewVisable: false,

    Userinfo: {
      token: ""
    },
>>>>>>> Login
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
    
  },
  actions: {

  },
  modules: {

  },
  getters: {
    getDetailStatus: state => state.detailViewVisable, 

    getToken: state => state.Userinfo.token

  }
});

