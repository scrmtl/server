import Vue from "vue";
import VueRouter from "vue-router";
import LogIn from "../views/LogIn.vue";
import Home from "../views/Home.vue";
import ProductBacklog from "../components/ProductBacklog.vue";
import SprintPlaning from "../components/SprintPlaning.vue";
import SprintBacklog from "../components/SprintBacklog.vue";
import Statistic from "../components/Statistic.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "LogIn",
    component: LogIn
  },
  {
    path: "home",
    name: "home",
    component: Home
  },
  {
    path: "pb",
    name: "pb",
    component: ProductBacklog
  },
  {
    path: "sp",
    name: "sp",
    component: SprintPlaning
  },
  {
    path: "sb",
    name: "sb",
    component: SprintBacklog
  },
  {
    path: "st",
    name: "st",
    component: Statistic
  },

];

const router = new VueRouter({
  routes
});

export default router;
