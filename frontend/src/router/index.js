import Vue from "vue";
import VueRouter from "vue-router";

import LogIn from "../views/LogIn.vue";
import Home from "../views/Home.vue";
import ProductBacklog from "../views/ProductBacklog.vue"
import SprintBacklog from "../views/SprintBacklog.vue"
import SprintPlaning from "../views/SprintPlaning.vue"
import Statistic from "../views/Statistic.vue"
import Archive from "../views/Archive.vue"

import Lane from "../components/Lane.vue";
import Epic from "../components/Epic.vue";
import Feature from "../components/Feature.vue";
import Task from "../components/Task.vue";



Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "LogIn",
    component: LogIn
  },
  {
    path: "/home",
    name: "home",
    component: Home,
  },
  {
    path: "/ProductBacklog",
    name: "ProductBacklog",
    component: ProductBacklog
  },{
    path: "/SprintBacklog",
    name: "SprintBacklog",
    component: SprintBacklog
  },
  {
    path: "/SprintPlaning",
    name: "SprintPlaning",
    component: SprintPlaning
  },
  {
    path: "/Statistic",
    name: "Statistic",
    component: Statistic
  },
  {
    path: "/Archive",
    name: "Archive",
    component: Archive
  },
  {
    path: "/Lane",
    name: "Lane",
    component: Lane
  },
  {
    path: "/Epic",
    name: "Epic",
    component: Epic
  },
  {
    path: "/Feature",
    name: "Feature",
    component: Feature
  },
  {
    path: "/Task",
    name: "Task",
    component: Task
  }

];

const router = new VueRouter({
  routes
});

export default router;
