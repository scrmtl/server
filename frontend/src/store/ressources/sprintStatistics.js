import createCrudModule from 'vuex-crud';

export default createCrudModule({
    resource: "sprint_statistics", // The name of your CRUD resource (mandatory)
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
      bySprintId(state) {
        return function(sprintId){
            var statistic = null;
            if(state.entities !== undefined && sprintId !== undefined){
                statistic = state.list.map(id => state.entities[id.toString()]).find(statistic => statistic.id == sprintId);
            }
            return statistic;
        }
    }
    }

});