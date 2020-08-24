import Vue from "vue";
import Vuex from "vuex";
//import Axios from "axios";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    detailViewVisable: false,

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

