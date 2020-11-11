import createCrudModule from 'vuex-crud';

export default createCrudModule({
  resource: 'lanes', // The name of your CRUD resource (mandatory)
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

  /** @description Custom function to get lanes
   * @param {number} boardId If set all lanes in that board are returned 
   * @param {number} projectId If set all lanes in that project are returned 
   * @return {string} Url defined by the arguments
   */
  customUrlFn(id, type, { projectId }) {

    // id will only be available when doing request to single resource, otherwise null
    // type is the actions you are dispatching: FETCH_LIST, FETCH_SINGLE, CREATE, UPDATE, REPLACE, DESTROY
    var rootUrl = '/api/lanes';
    if (projectId != undefined) {
      rootUrl = `/api/lanes/?project=${projectId}`
    }
    rootUrl = id ? `${rootUrl}/${id}/` : rootUrl;
    return rootUrl;
  },

  getters: {
    /** @description Get the ID of a lane by it's name 
     * @param {string} laneName Name of the lane 
     * @return {Array} Array of lane with the given name
     */
    byName(state) {
      return laneName => {
        var lanes = null;
        if (state.entities !== undefined) {
          lanes = Object.values(state.entities).filter(lane => lane.name === laneName);
        }
        return lanes;
      }
    },

    /** @description Get all lane object by ID 
     * @param {Array} idArray Array with lane IDs 
     * @return {Array} Array of lanes Objects
     */
    byIdArray(state) {
      return function (idArray) {
        if (idArray === undefined) return undefined
        return idArray.map(id => state.entities[id.toString()])
      }
    },
  }
});