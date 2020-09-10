import createCrudModule from 'vuex-crud';

export default createCrudModule({
    resource: 'groups', // The name of your CRUD resource (mandatory)
    only: [
        'FETCH_LIST',
        'FETCH_SINGLE'
    ], // What CRUD actions should be available
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

});