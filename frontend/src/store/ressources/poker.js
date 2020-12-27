import { getField, updateField } from 'vuex-map-fields';

const state = () => ({
  toVote: [
    {name: "Redesgin App Baar", id: "10", storypoints: "0"},
    {name: "Upload Filter", id: "12", storypoints: "0"},
    {name: "Animation Snake", id: "14", storypoints: "0"}
  ],
  voted: [
    {name: "New Logo", id: "15", storypoints: "0"},
    {name: "Websocket", id: "16", storypoints: "0"}
  ],
  players: [
    {name: "Peter", storypoints: "3", color: "white"},
    {name: "Hans", storypoints: "3", color: "white"},
    {name: "Jonas", storypoints: "32", color: "warning"},
    {name: "König Ludwig", storypoints: "8", color: "white"},
    {name: "Dittrich", storypoints: "8", color: "white"},
  ]
});

const mutations = {
  updateField
};

const getters = {
  getField
};


export default {
  // We're using namespacing
  // in all of our modules.
  namespaced: true,
  name: "poker",
  state,
  getters,
  mutations
};