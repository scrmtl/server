import Vue from "vue";
import VueRouter from "vue-router";

import LogIn from "../views/LogIn.vue";
import Register from "../views/Register.vue";
import Home from "../views/Home.vue";
import ProductBacklog from "../views/ProductBacklog.vue";
import SprintBacklog from "../views/SprintBacklog.vue";
import SprintPlaning from "../views/SprintPlaning.vue";
import Statistic from "../views/Statistic.vue";
import Archive from "../views/Archive.vue";
import Project from "../views/Project.vue";
import ProjectDashboard from "../views/ProjectDashboard";

import Lane from "@/components/Lane.vue";
import Epic from "@/components/Epic.vue";
import Feature from "@/components/Feature.vue";
import Task from "@/components/Task.vue";
//import { component } from "vue/types/umd";






Vue.use(VueRouter);

const routes = [
  {
    path: "/login",
    name: "LogIn",
    component: LogIn
  },
  {
    path: "/register",
    name: "Register",
    component: Register
  },
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/project/:id",
    component: Project,
    props: true,
    children: [
      {
        // Default Child
        path: "",
        name: "ProjectDashboard",
        component: ProjectDashboard,
      },
      {
        path: "ProductBacklog",
        component: ProductBacklog,
      },
      {
        path: "SprintBacklog",
        component: SprintBacklog
      },
      {
        path: "SprintPlaning",
        component: SprintPlaning
      },
      {
        path: "Statistic",
        component: Statistic
      },
      {
        path: "Archive",
        component: Archive
      },
    ]
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
  },
];

const router = new VueRouter({
  routes
});

router.beforeEach((to, from, next) => {
  if (to.name !== "LogIn" && !localStorage.getItem('token') && to.name !== "Register") {
    if (to.name == "Register") {
      next({ name: "Register" });
    }
    else {
      next({ name: "LogIn" });
    }
  }
  else {
    next();
  }
});

export default router;
