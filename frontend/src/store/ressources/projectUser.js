import createCrudModule from 'vuex-crud';

export default createCrudModule({
    resource: 'project_users', // The name of your CRUD resource (mandatory)
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

    /** @description Custom function to get an array of project_users
     * @param {number} projectId If set all tasks in that lane are returned (exampleUrl: /api/projects/1/project_users`)
     * @return {string} Url defined by the arguments
     */
    customUrlFn(id, type, projectId) {
        // id will only be available when doing request to single resource, otherwise null
        // type is the actions you are dispatching: FETCH_LIST, FETCH_SINGLE, CREATE, UPDATE, REPLACE, DESTROY
        var rootUrl = '/api/project_users';
        if (projectId != null) {
            rootUrl = `/api/project_users/?project=${projectId}`
        }
        rootUrl = id ? `${rootUrl}/${id}/` : rootUrl;
        return rootUrl;

    },

    getters: {
        /** @description Add Custom getter 
         * @param {Array} idArray Array with project User IDs 
         * @return {Array} Array of User Objects
         */
        byIdArray(state) {
            return function (idArray) {
                if (idArray === undefined) return undefined
                return idArray.map(id => state.entities[id.toString()])
            }
        },

        /** @description Add Custom getter 
         * @param {Array} idArray Array with project User IDs
         * @return {Array} Array of User Objects with Details to project context {id: <project user id>, role: <role object> , plattform_user: <plattform user object>, project: <id>}
         */
        byIdArrayWithDetails: (state) => {
            return function(idArray){
              let resultArray = [];
              let projectRoles = this.$store.getters["projectRole/list"];
              let users = this.$store.getters["user/list"];
              if(idArray !== undefined && projectRoles !== undefined && state.entities !== undefined){
                idArray.filter(x => Object.keys(state.entities).includes(x.toString())).map(id => state.entities[id.toString()]).forEach(projectUser => {
                    resultArray.push({
                    id: projectUser.id,
                    role: projectRoles.find(role => role.id === projectUser.role),
                    plattform_user: users.find(user => user.id === projectUser.plattform_user),
                    project: projectUser.project,
                  })
                });
              }
              return resultArray.sort((a, b) =>
                a.plattform_user.username.localeCompare(b.plattform_user.alt)
              );
      
            }
        },

        /** @description Add Custom getter 
         * @param {string} roleName searching role by name
         * @return {Array} Array of project User Objects with the searching role 
         */
        byRole: (state) => {
          return function(roleName){
            let userByRole = null;
            let projectRoles = this.$store.getters["projectRole/list"];
            if(roleName !== undefined && state.entities !== undefined){
              let roleId = projectRoles[roleName.toString()].id;
              userByRole = state.list.map(id => state.entities[id.toString()]).filter(puser => puser.role === roleId);
            }
            return userByRole;
          }
        }
    }

});