import createCrudModule from "vuex-crud";

export default createCrudModule({
  resource: "poker_votes", // The name of your CRUD resource (mandatory)
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
    byPokerVotingId: (state) => {
      return function (pokerVotingId) {
        var pokerVotes = null;
        if (state.entities !== undefined) {
          pokerVotes = state.list
            .map((id) => state.entities[id.toString()])
            .filter((pokerVote) => pokerVote.poker_voting === pokerVotingId);
        }
        return pokerVotes;
      };
    },
  },
});
