import createCrudModule from 'vuex-crud';

export default createCrudModule({
    resource: 'steps', // The name of your CRUD resource (mandatory)
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

    /**@description Custom function to get an array of features
     * @param {number} taskId If set all steplists in that task are returned (exampleUrl: /api/tasks/1/steplists`)
     * @return {string} Url defined by the arguments
     */
    customUrlFn(id, type, { steplistId = null }) {

        // id will only be available when doing request to single resource, otherwise null
        // type is the actions you are dispatching: FETCH_LIST, FETCH_SINGLE, CREATE, UPDATE, REPLACE, DESTROY
        var rootUrl = '/api/steplists';
        //rootUrl = `/api/steplists/${taskId}/step`;
        //rootUrl = id ? `${rootUrl}/${id}/` : rootUrl;

        if (steplistId != null) {
            rootUrl = `/api/steps/?steplist=${steplistId}`
        }
        rootUrl = id ? `${rootUrl}/${id}/` : rootUrl;
        return rootUrl;
    },
    getters: {
        /** @description Add Custom getter 
         * @param {Array} idArray Array with step IDs 
         * @return {Array} Array of Step Objects
         */
        byIdArray(state) {
            return idArray =>
                idArray.map(id => state.entities[id.toString()])
        },

    }
});