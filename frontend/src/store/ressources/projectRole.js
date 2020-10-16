import createCrudModule from 'vuex-crud';

export default createCrudModule({
    resource: 'project_roles', // The name of your CRUD resource (mandatory)
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
    getters: {
        /** @description Get the ID of a role by it's name 
         * @param {string} roleName Name of the role 
         * @return {object} role with the given name
         */
        byName(state) {
            return roleName => {
                for (const [key, value] of Object.entries(state.entities)) {
                    if (value.role_name === roleName) {
                        return parseInt(key)
                    }
                }
            }
        }
    }

});