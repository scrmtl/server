import createCrudModule from "vuex-crud";

export default createCrudModule({
  resource: "sprints", // The name of your CRUD resource (mandatory)
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

  /** @description Custom function to get an array of sprints
   * @param {number} projectId If set all tasks in that lane are returned (exampleUrl: /api/projects/1/sprints`)
   * @return {string} Url defined by the arguments
   */
  customUrlFn(id, type, { projectId = null }) {
    // id will only be available when doing request to single resource, otherwise null
    // type is the actions you are dispatching: FETCH_LIST, FETCH_SINGLE, CREATE, UPDATE, REPLACE, DESTROY
    var rootUrl = "/api/sprints/";
    if (projectId != null) {
      rootUrl = `/api/sprints/?project=${projectId}`;
    }
    rootUrl = id ? `${rootUrl}${id}/` : `${rootUrl}`;
    return rootUrl;
  },

  getters: {
    byProjectId: (state) => {
      return function (projectId) {
        var sprints = null;
        if (state.entities !== undefined) {
          sprints = state.list
            .map((id) => state.entities[id.toString()])
            .filter((sprint) => sprint.project == projectId);
        }
        return sprints;
      };
    },
  },
});
