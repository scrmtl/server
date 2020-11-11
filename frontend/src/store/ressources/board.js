import createCrudModule from 'vuex-crud';

export default createCrudModule({
    resource: 'boards', // The name of your CRUD resource (mandatory)
    // Follow actions are generated:
    // fetchList
    // fetchSingle
    // create
    // update
    // replace
    // destroy

    // Follow getters are generated:
    // list 
    // byId(id))

    /** @description Custom function to get an array of boards
     * @param {number} projectId If set all boards in that project are returned 
     * @return {string} Url defined by the arguments
     */
    customUrlFn(id, type, projectId) {
        // id will only be available when doing request to single resource, otherwise null
        // type is the actions you are dispatching: FETCH_LIST, FETCH_SINGLE, CREATE, UPDATE, REPLACE, DESTROY
        var rootUrl = '/api/boards';
        if (projectId != null) {
            rootUrl = `/api/boards/?project=${projectId}`
        }
        rootUrl = id ? `${rootUrl}/${id}/` : rootUrl;
        return rootUrl;

    },


    getters: {
        /** @description Add Custom getter 
         * @param {string} type Board Type (PB, SP, AB) 
         * @return {Object} selected Board
         */
        byType(state) {
            return (type, projectId) => {
                return Object.values(state.entities).find(x => (
                    x.board_type === type &&
                    x.project === projectId));
            }
        },

    }
});

