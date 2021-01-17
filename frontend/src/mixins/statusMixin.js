export default {
  methods:{
    GetPokerNamedStatus(status){
      var namedStatus = "Not started";
      switch(status){
        case "NS":
          namedStatus = "Not started"
          break;
        case "WAIT":
          namedStatus = "Waiting for vote"
          break;
        case "SKIP":
          namedStatus = "Skipped"
          break;
        case "FIN":
          namedStatus = "Voted"
          break;
      };
      return namedStatus;
    }
  }
}