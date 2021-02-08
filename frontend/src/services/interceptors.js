import Axios from "axios";
// this is not available in axios interceptor, so it have to import directly
import store from "../store";
import router from "../router";

export default function setup() {
  // load token from vuex
  const token = store.getters.getToken;
  if (token) {
    Axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  }

  Axios.interceptors.response.use(
    function (response) {
      return response;
    },
    function (error) {
      console.log(error);
      if (error.response.status) {
        switch (error.response.status) {
          case 400:
            // Bad Request
            break;
          case 401:
            store.commit("showSystemAlert", {
              message: "session expired",
              category: "error",
            });
            store.dispatch("logout").then(() => {
              if (router.history.current.name !== "LogIn") {
                router.push("/login");
              }
            });
            break;
          case 403:
            store.commit("showSystemAlert", {
              message: "Permission denied: " + error.response.data.detail,
              category: "error",
            });
            break;
          case 404:
            store.commit("showSystemAlert", {
              message: "page not found",
              category: "error",
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

  Axios.interceptors.request.use((config) => {
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
