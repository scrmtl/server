import createCrudModule from "vuex-crud";

export default createCrudModule({
  resource: "groups", // The name of your CRUD resource (mandatory)
  only: ["FETCH_LIST", "FETCH_SINGLE"], // What CRUD actions should be available
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
    /** @description Get the ID of a group by it's name
     * @param {string} groupName Name of the group
     * @return {object} group with the given name
     */
    byName(state) {
      return (groupName) => {
        for (const [key, value] of Object.entries(state.entities)) {
          if (value.name === groupName) {
            return parseInt(key);
          }
        }
      };
    },
  },
});
