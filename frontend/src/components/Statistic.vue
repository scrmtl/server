<template>
  <div class="tabbody tab-content">
      Statistic Vue-Comp
  </div>
</template>

<script>

import axios from 'axios';

export default {
    created() {
      axios
      .get('http://scrmtl.ddns.net:14444/api/', {}, {
        auth: {
          username: "stephan",
          password: "scrmtl14444"
        }
      })
      .then (response=>{
        console.log(response.data)
      })
      .catch(error => {
        console.log('There was an error:' + error.response)
      })
    }


};
</script>

<style lang="css" scoped>
.tab-content {
  height: 1500px;
}
</style>