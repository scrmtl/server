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
     * @param {number} projectId If set all tasks in that lane are returned (exampleUrl: /api/projects/1/boards`)
     * @return {string} Url defined by the arguments
     */
    customUrlFn(id, type, projectId) {
        // id will only be available when doing request to single resource, otherwise null
        // type is the actions you are dispatching: FETCH_LIST, FETCH_SINGLE, CREATE, UPDATE, REPLACE, DESTROY
        const rootUrl = `/api/projects/${projectId}/boards`;
        return id ? `${rootUrl}/${id}/` : rootUrl;
    },
    getters: {
        /** @description Add Custom getter 
         * @param {string} type Board Type (PB, SP, AB) 
         * @return {Object} selected Board
         */
        byType(state) {
            return  type => 
                Object.values(state.entities).filter(x => x.board_type === type).shift()},
        
    }
});

