import createCrudModule from 'vuex-crud';

export default createCrudModule({
    resource: "project_statistics", // The name of your CRUD resource (mandatory)
    // Follow actions are generated:
    // fetchList
    // fetchSingle

    // Follow getters are generated:
    // list 
    // byId(id)
    /*only: [
      "FETCH_LIST",
      "FETCH_SINGLE",
    ],*/
    getters: {
      byProjectId(state) {
        return function(projectId){
            var statistic = null;
            if(state.entities !== undefined && projectId !== undefined){
                statistic = state.list.map(id => state.entities[id.toString()]).find(statistic => statistic.id == projectId);
            }
            return statistic;
        }
      }
    }

});