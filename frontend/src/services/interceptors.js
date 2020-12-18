import Axios from "axios";
import store from "../store";

export default function setup() {
  const token = localStorage.getItem('token');
  if (token) {
    Axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  }

  Axios.interceptors.response.use(
    function (response){
      return response;
    },
    function (error) {
      if (error.response.status) {
        switch (error.response.status) {
          case 400:
            //do something
            break;
          case 401:
            store.commit("showSystemAlert", {
              message: "seesion expired",
              category: "error"
              });
            store.dispatch("logout").then(() => {
              this.$router.push("/login");
            });
            break;        
          case 403:
            store.commit("showSystemAlert", {
            message: "Permission denied: "+ error.response.data.detail,
            category: "error"
            });          
            break;        
          case 404:
            store.commit("showSystemAlert", {
            message: "page not found",
            category: "error"
            });
            break;        
          case 502:
            //do something
            break;
        }
      }
      return Promise.reject(error.response);
    }
  );
  
  Axios.interceptors.request.use(config => {
    if (
      (config.method === "post" || config.method === "patch") &&
      config.url[config.url.length - 1] !== "/" &&
      !config.url.includes("/?")
    ) {
      config.url += "/";
    }
    return config;
  });
}