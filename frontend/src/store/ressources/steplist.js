import createCrudModule from 'vuex-crud';

export default createCrudModule({
    resource: 'steplist', // The name of your CRUD resource (mandatory)
    // Follow actions are generated:
    // FETCH_LIST
    // FETCH_SINGLE
    // CREATE
    // UPDATE
    // REPLACE
    // DESTROY
    
    // Follow getters are generated:
    // list 
    // byid(id)
});