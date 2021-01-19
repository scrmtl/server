import { mapGetters } from "vuex";
import { mapFields } from "vuex-map-fields";
export default {
  computed:{
    ...mapGetters("vote", {
      voteByIds: "byPokerVoteIdAndUserId"
    }),
    ...mapFields([
      "Userinfo.userId"
    ]),
  },
  
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
    },
    GetVoteStatus(pokerVoteStatus, pokerVoteId){
      var voteStatus = "VOTED"
      var votes = this.voteByIds({pokerVoteId: pokerVoteId, userId: this.userId})
      if(votes.length > 0 && pokerVoteStatus === "WAIT"){
        // check vote abstention 
        if(votes.some(vote => vote.storypoints === 0)){
          voteStatus="ABSTENTION"
        }
        else{
          voteStatus = "VOTED";
        }
      }
      // Voting is closed
      else if(votes.length > 0 && pokerVoteStatus === "FIN"){
        // check vote abstention 
        if(votes.some(vote => vote.storypoints === 0)){
          voteStatus="ABSTENTION"
        }
        else{
          voteStatus = "VOTED";
        }
      }
      // Not voted, still waiting for voting
      else if(votes.length == 0 && pokerVoteStatus === "WAIT"){
        voteStatus = "WAIT";
      }
      // Voting is closed
      else if(votes.length == 0 && pokerVoteStatus === "FIN"){
        voteStatus = "NOTVOTED";
      }
      else{
        voteStatus = "SKIPPED";
      }
      // WAIT, SKIPPED, VOTED, ABSTENTION, NOTVOTED
      return voteStatus;
    },
  }
}