import createCrudModule from "vuex-crud";

export default createCrudModule({
  resource: "users", // The name of your CRUD resource (mandatory)
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
     * @param {Array} idArray Array with plattform user IDs
     * @return {Array} Array of User Objects
     */
    byIdArray(state) {
      return function (idArray) {
        if (idArray === undefined) return undefined;
        return idArray.map((id) => state.entities[id.toString()]);
      };
    },
    /** @description Add Custom getter
     * @param {Array} idArray Array with User IDs
     * @param {Number} projectId project ID
     * @return {Array} Array of User Objects with Details to project context {id: <plattform user id>, role: <role object> , plattform_user: <plattform user object>, project: <id>}
     */
    byIdArrayWithDetails(state) {
      return function (idArray, projectId) {
        let resultArray = [];
        let projectUsers = this.$store.getters["projectUser/list"];
        let projectRoles = this.$store.getters["projectRole/list"];
        if (
          idArray !== undefined &&
          projectRoles !== undefined &&
          projectUsers !== undefined &&
          state.entities !== undefined
        ) {
          idArray
            .filter((x) => Object.keys(state.entities).includes(x.toString()))
            .map((id) => state.entities[id.toString()])
            .forEach((user) => {
              let projectUser = projectUsers.find(
                (projectUser) =>
                  projectUser.plattform_user == user.id &&
                  projectUser.project == projectId
              );
              resultArray.push({
                id: user.id,
                role: projectUser
                  ? projectRoles.find((role) => role.id === projectUser.role)
                  : "",
                plattform_user: user,
                project: projectId,
              });
            });
        }
        return resultArray.sort((a, b) =>
          a.plattform_user.username.localeCompare(b.plattform_user.alt)
        );
      };
    },

    byProjectIdWithDetails(state) {
      return function (projectId) {
        let resultArray = [];
        let projectUsers = this.$store.getters["projectUser/list"];
        let projectRoles = this.$store.getters["projectRole/list"];
        if (
          projectRoles !== undefined &&
          projectUsers !== undefined &&
          state.entities !== undefined
        ) {
          projectUsers
            .filter((projectUser) => projectUser.project === projectId)
            .forEach((projectUser) => {
              let user = state.entities[projectUser.plattform_user.toString()];
              resultArray.push({
                id: user.id,
                role: projectRoles.find((role) => role.id === projectUser.role),
                plattform_user: user,
                project: projectId,
              });
            });
        }
        return resultArray;
      };
    },
    byProjectId(state) {
      return function (projectId) {
        let resultArray = [];
        let projectUsers = this.$store.getters["projectUser/list"];
        if (projectUsers !== undefined && state.entities !== undefined) {
          projectUsers
            .filter((projectUser) => projectUser.project === projectId)
            .forEach((projectUser) => {
              let user = state.entities[projectUser.plattform_user.toString()];
              resultArray.push(user);
            });
        }
        return resultArray;
      };
    },
    byUserId(state) {
      return function (userId) {
        let resultArray = [];
        let projectUsers = this.$store.getters["projectUser/list"];
        if (projectUsers !== undefined && state.entities !== undefined) {
          projectUsers.forEach((element) => {
            if (element.plattform_user === userId) {
              resultArray.push(element);
            }
          });
        }
        return resultArray;
      };
    },
  },
});
