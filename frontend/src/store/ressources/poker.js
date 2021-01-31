import { getField, updateField } from "vuex-map-fields";

const state = () => ({
  voteCards: [
    { name: "Jingle schreiben", id: "110", storypoints: "0" },
    { name: "Neue Leute kennenlernen", id: "106", storypoints: "0" },
    {
      name: "Schafkopf lernen, wie ein Meisterschüler",
      id: "161",
      storypoints: "0",
    },
  ],
  votedCards: [
    { name: "New Logo", id: "15", storypoints: "0" },
    { name: "Websocket", id: "16", storypoints: "0" },
  ],
  players: [
    { name: "Peter", storypoints: "3", color: "white" },
    { name: "Hans", storypoints: "3", color: "white" },
    { name: "Jonas", storypoints: "32", color: "warning" },
    { name: "König Ludwig", storypoints: "8", color: "white" },
    { name: "Dittrich", storypoints: "8", color: "white" },
  ],
});

const mutations = {
  updateField,

  addCardToVote(state, { cardName, cardId, cardStorypoints }) {
    state.voteCards.push({
      name: cardName,
      id: cardId,
      storypoints: cardStorypoints,
    });
  },

  removeCardToVote(state, cardId) {
    state.voteCards = state.voteCards.filter((item) => item.id !== cardId);
  },
};

const getters = {
  getField,
};

export default {
  // We're using namespacing
  // in all of our modules.
  namespaced: true,
  name: "poker",
  state,
  getters,
  mutations,
};
