<template>
  <div class="tabbody tab-content">
    Statistic Vue-Comp
  </div>
</template>

<script>
import axios from "axios";

export default {
  created() {
    axios
      .get(
        //"https://elherminius.ddns.net:14444/api/board",
        "http://scrmtl.ddns.net:14444/api/board/",
        //{},
        {
          auth: {
            username: "stephan",
            password: "scrmtl14444"
          }
        }
      )
      .then(response => {
        console.log(response.data);
      })
      .catch(error => {
        console.log("There was an error:" + error.response);
      });
  }
};
</script>

<style lang="css" scoped>
.tab-content {
  height: 1000px;
}
</style>
