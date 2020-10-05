import createCrudModule from 'vuex-crud';

export default createCrudModule({
    resource: 'project_users', // The name of your CRUD resource (mandatory)
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

    /** @description Custom function to get an array of project_users
     * @param {number} projectId If set all tasks in that lane are returned (exampleUrl: /api/projects/1/project_users`)
     * @return {string} Url defined by the arguments
     */
    customUrlFn(id, type, projectId) {
        // id will only be available when doing request to single resource, otherwise null
        // type is the actions you are dispatching: FETCH_LIST, FETCH_SINGLE, CREATE, UPDATE, REPLACE, DESTROY
        var rootUrl = '/api/project_users';
        if (projectId != null) {
            rootUrl = `/api/project_users/?project=${projectId}`
        }
        rootUrl = id ? `${rootUrl}/${id}/` : rootUrl;
        return rootUrl;

    },

    getters: {
        /** @description Add Custom getter 
         * @param {Array} idArray Array with project User IDs 
         * @return {Array} Array of User Objects
         */
        byIdArray(state) {
            return function (idArray) {
                if (idArray === undefined) return undefined
                return idArray.map(id => state.entities[id.toString()])
            }
        },

    }

});