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
    // byId(id)
    getters: {
        /** @description Add Custom getter 
         * @param {Array} idArray Array with User IDs 
         * @return {Array} Array of User Objects
         */
        byIdArray(state) {
            return function (idArray) {
                if (idArray === undefined) return undefined
                return idArray.map(id => state.entities[id.toString()])
            }
        },

    }
});