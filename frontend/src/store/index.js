import Vue from "vue";
import Vuex from "vuex";
import Axios from "axios";
import createPersistedState from "vuex-persistedstate";

Vue.use(Vuex, Axios);

export default new Vuex.Store({
  // for debugging 
  // later something like this even better 
  // strict: eprocess.env.NODE_ENV !== 'production'
  strict: true,
  plugins: [createPersistedState()],
  // States
  state: {   
    detailViewVisable: false,

    

    


    Userinfo: {
      username: "",
      token: ""
    },
  },
  // call REST API
  // Use from the components
  actions: {
    login ({ commit }, { token, username }) {
      commit('SET_TOKEN', token);
      commit('SET_USERNAME', username);
      // set auth header
      Axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    },

    logout ({ commit }) {
      commit('RESET', '');
    }
      
  },
  //Update States
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

    SET_TOKEN(state, token){
      state.Userinfo.token = token;
    },
    SET_USERNAME(state, username){
      state.Userinfousername = username;
    },
    RESET(state){
      state.Userinfo.username = "";
      state.Userinfo.token = "";
    }

    
  },
  getters: {
    getDetailStatus: state => {
      return state.detailViewVisable
    }, 

    getToken: state => {
      return state.Userinfo.token
    },

    getUsername: state => {
      return state.Userinfo.username
    },
  },
  modules: {

  }
});

