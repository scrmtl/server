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

  /** @description Custom function to get an array of lanes
   * @param {number} boardId If set all lanes in that board are returned (exampleUrl: /api/board/1/lanes`)
   * @return {string} Url defined by the arguments
   */
  customUrlFn(id, type, boardId) {
    // id will only be available when doing request to single resource, otherwise null
    // type is the actions you are dispatching: FETCH_LIST, FETCH_SINGLE, CREATE, UPDATE, REPLACE, DESTROY
    const rootUrl = `/api/boards/${boardId}/lanes`;
    return id ? `${rootUrl}/${id}/` : rootUrl;
    //const rootURL = `/api/lanes/?boards=${boardId}`
    //return rootUrl;
  }
});