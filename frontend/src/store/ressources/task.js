import createCrudModule from 'vuex-crud';

export default createCrudModule({
    resource: 'tasks', // The name of your CRUD resource (mandatory)
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

    /** @description Custom function to get an array of tasks
     * @param {number} laneId If set all tasks in that lane are returned (exampleUrl: /api/lanes/1/tasks`)
     * @param {number} byUser Gets array of currently assigned tasks of the authenticated user (example Url /api/tasks/?byUser=1)
     * @return {string} Url defined by the arguments
     */
    customUrlFn(id, type, { laneId = null, projectId = null, byUser = null }) {

        // id will only be available when doing request to single resource, otherwise null
        // type is the actions you are dispatching: FETCH_LIST, FETCH_SINGLE, CREATE, UPDATE, REPLACE, DESTROY
        var rootUrl = '/api/tasks';
        if (laneId) {
            rootUrl = `/api/tasks/?lane=${laneId}`;
        } else if (projectId) {
            rootUrl = `/api/tasks/?projects=${projectId}`;
        } else if (byUser) {
            rootUrl = `/api/tasks/?byUser=${byUser}`;
        }
        rootUrl = id ? `${rootUrl}/${id}/` : rootUrl;
        return rootUrl;
    },

    getters: {
        /** @description Add Custom getter 
         * @param {Array} idArray Array with Task IDs 
         * @return {Array} Array of Task Objects
         */
        byIdArray(state) {
            return idArray =>
                idArray.map(id => state.entities[id.toString()])
        },

    }
});