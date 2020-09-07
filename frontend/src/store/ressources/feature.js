import createCrudModule from 'vuex-crud';

export default createCrudModule({
    resource: 'features', // The name of your CRUD resource (mandatory)
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
     * @param {number} laneId If set all epics in that lane are returned (exampleUrl: /api/lanes/1/features`)
     * @return {string} Url defined by the arguments
     */
    customUrlFn(id, type, laneId = null) {

        // id will only be available when doing request to single resource, otherwise null
        // type is the actions you are dispatching: FETCH_LIST, FETCH_SINGLE, CREATE, UPDATE, REPLACE, DESTROY
        var rootUrl = '';
        rootUrl = `/api/lanes/${laneId}/features`;
        rootUrl = id ? `${rootUrl}/${id}/` : rootUrl;

        return rootUrl;
    }
});