import createCrudModule from "vuex-crud";

export default createCrudModule({
  resource: "poker_votings", // The name of your CRUD resource (mandatory)
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
    byVoterId: (state) => {
      return function (voterId) {
        var pokerVotings = null;
        if (state.entities !== undefined) {
          pokerVotings = state.list
            .map((id) => state.entities[id.toString()])
            .filter((pokerVoting) => pokerVoting.voters.includes(voterId));
        }
        return pokerVotings;
      };
    },
  },
});
