import createCrudModule from "vuex-crud";

export default createCrudModule({
  resource: "labels", // The name of your CRUD resource (mandatory)
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
    /** @description Add Custom getter
     * @param {Array} idArray Array with label IDs
     * @return {Array} Array of Label Objects
     */
    byIdArray(state) {
      return (idArray) => idArray.map((id) => state.entities[id.toString()]);
    },
  },
});
