import createCrudModule from "vuex-crud";

export default createCrudModule({
  resource: "features", // The name of your CRUD resource (mandatory)
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

  /** @description Custom function to get an array of features
   * @param {number} laneId If set all features in that lane are returned (exampleUrl: /api/lanes/1/features`)
   * @param {number} byUser Gets array of currently assigned features of the authenticated user (example Url /api/features/?byUser=1)
   * @return {number} Url defined by the arguments
   */
  customUrlFn(id, type, { laneId = null, byUser = null }) {
    // id will only be available when doing request to single resource, otherwise null
    // type is the actions you are dispatching: FETCH_LIST, FETCH_SINGLE, CREATE, UPDATE, REPLACE, DESTROY
    var rootUrl = id ? `/api/features/${id}` : "/api/features/";
    if (laneId) {
      rootUrl = `/api/features/?lane=${laneId}`;
    } else if (byUser) {
      rootUrl = `/api/features/?byUser=${byUser}`;
      //rootUrl = `/api/features/?lane=${laneId}`
    }
    return rootUrl;
  },
  getters: {
    /** @description Add Custom getter
     * @param {Array} idArray Array with Task IDs
     * @return {Array} Array of Task Objects
     */
    byIdArray(state) {
      return (idArray) => idArray.map((id) => state.entities[id.toString()]);
    },
  },
});
