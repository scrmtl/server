import createCrudModule from "vuex-crud";

export default createCrudModule({
  resource: "epics", // The name of your CRUD resource (mandatory)
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

  /** @description Custom function to get an array of epics
   * @param {number} laneId If set all epics in that lane are returned (exampleUrl: /api/lanes/1/epics`)
   * @param {number} byUser Gets array of currently assigned epics of the authenticated user (example Url /api/epics/?byUser=1)
   * @return {number} Url defined by the arguments
   */
  customUrlFn(id, type, { laneId = null, byUser = null }) {
    // id will only be available when doing request to single resource, otherwise null
    // type is the actions you are dispatching: FETCH_LIST, FETCH_SINGLE, CREATE, UPDATE, REPLACE, DESTROY
    var rootUrl = id ? `/api/epics/${id}` : "/api/epics/";
    if (laneId) {
      rootUrl = `/api/epics/?lane=${laneId}`;
    } else if (byUser) {
      rootUrl = `/api/epics/?byUser=${byUser}`;
      //rootUrl = `/api/epics/?lane=${laneId}`
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
