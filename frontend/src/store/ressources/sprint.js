import createCrudModule from 'vuex-crud';

export default createCrudModule({
    resource: 'sprints', // The name of your CRUD resource (mandatory)
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
    customUrlFn(id, type, projectId) {
        // id will only be available when doing request to single resource, otherwise null
        // type is the actions you are dispatching: FETCH_LIST, FETCH_SINGLE, CREATE, UPDATE, REPLACE, DESTROY
        const rootUrl = `/api/projects/${projectId}/sprints`;
        return id ? `${rootUrl}/${id}/` : rootUrl;
    }
});