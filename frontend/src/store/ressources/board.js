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
    // byid(id))
    customUrlFn(id, type, projectId) {
        // id will only be available when doing request to single resource, otherwise null
        // type is the actions you are dispatching: FETCH_LIST, FETCH_SINGLE, CREATE, UPDATE, REPLACE, DESTROY
        const rootUrl = `/api/projects/${projectId}/boards`;
        return id ? `${rootUrl}/${id}/` : rootUrl;
      }
});

