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
});