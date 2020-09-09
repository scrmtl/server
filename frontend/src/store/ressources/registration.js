import createCrudModule from 'vuex-crud';

export default createCrudModule({
    resource: 'registration', // The name of your CRUD resource (mandatory)
    urlRoot: '/rest-auth/registration/', // The url to fetch the resource
    only: [
        'CREATE',
    ], // What CRUD actions should be available

    // Follow getters are generated:
    // list 
    // byId(id)

});