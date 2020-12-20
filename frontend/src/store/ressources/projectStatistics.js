import createCrudModule from 'vuex-crud';

export default createCrudModule({
    resource: "project_statistics", // The name of your CRUD resource (mandatory)
    // Follow actions are generated:
    // fetchList
    // fetchSingle

    // Follow getters are generated:
    // list 
    // byId(id)
    /** @description Custom function to get an array of tasks
     * @param {number} laneId If set all tasks in that lane are returned (exampleUrl: /api/lanes/1/tasks`)
     * @param {number} byUser Gets array of currently assigned tasks of the authenticated user (example Url /api/tasks/?byUser=1)
     * @return {string} Url defined by the arguments
     */
    /*customUrlFn(id, type, { templateId = undefined }) {

        // id will only be available when doing request to single resource, otherwise null
        // type is the actions you are dispatching: FETCH_LIST, FETCH_SINGLE, CREATE, UPDATE, REPLACE, DESTROY
        var rootUrl = `/api/project_statistics`;
        if (!(templateId === undefined)) {
            rootUrl = `/api/project_statistics/?template=${templateId}`;
        }
        rootUrl = id ? `${rootUrl}/${id}/` : rootUrl;
        return rootUrl;
    },*/
    /*only: [
      "FETCH_LIST",
      "FETCH_SINGLE",
    ],*/
    getters: {
      byProjectId(state) {
        return function (projectID) {
            let result = undefined;
            let projectList = this.$store.getters["projectStatistics/list"];
            if (projectList!== undefined && state.entities !== undefined) {
                projectList.forEach(element => {
                    if (element.id === projectID) {
                        result = element;
                    }
                })
            }
            return result;
        }
    }
    }

});