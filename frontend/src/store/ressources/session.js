import createCrudModule from 'vuex-crud';

export default createCrudModule({
    resource: 'users', // The name of your CRUD resource (mandatory)
    // Follow actions are generated:
    // fetchList
    // fetchSingle
    // create
    // update
    // replace
    // destroy

    // Follow getters are generated:
    // list 
    // byid(id)

    /** @description Custom function to get an array of tasks
     * @param {boolean} all If set all tasks in that lane are returned (exampleUrl: /api/lanes/1/tasks`)
     * @return {string} Url defined by the arguments
     */
    customUrlFn(id, type, { all = false }) {

        // type is the actions you are dispatching: FETCH_LIST, FETCH_SINGLE, CREATE, UPDATE, REPLACE, DESTROY
        var rootUrl = '';
        if (all) {
            rootUrl = `/api/users/?session=all`;
        } else {
            rootUrl = `/api/users/?session=self`;
        }
        
        return rootUrl;  
    }
});