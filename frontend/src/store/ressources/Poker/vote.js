import createCrudModule from "vuex-crud";

export default createCrudModule({
  resource: "votes", // The name of your CRUD resource (mandatory)
  // Follow actions are generated:
  // fetchList
  // fetchSingle
  // create
  // update
  // replace
  // destroy

  // Follow getters are generated:
  // list
  // byId(id)
  getters: {
    byPokerVoteIdAndUserId: (state) => {
      return function ({ pokerVoteId, userId }) {
        var votes = null;
        if (state.entities !== undefined) {
          votes = state.list
            .map((id) => state.entities[id.toString()])
            .filter(
              (vote) => vote.poker_vote === pokerVoteId && vote.user === userId
            );
        }
        return votes;
      };
    },
    byPokerVoteId: (state) => {
      return function (pokerVoteId) {
        var votes = null;
        if (state.entities !== undefined) {
          votes = state.list
            .map((id) => state.entities[id.toString()])
            .filter((vote) => vote.poker_vote === pokerVoteId);
        }
        return votes;
      };
    },
  },
});
