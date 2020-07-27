import Vue from "vue";
import Vuex from "vuex";
//import Axios from "axios";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    detailViewVisable: false,
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
    }
    
  },
  actions: {
  
  },
  modules: {

  },
  getters: {
    getDetailStatus: state => state.detailViewVisable

  }
});

