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
import PlanningPoker from "../views/PlanningPoker";

Vue.use(VueRouter);

const routes = [
  {
    path: "/login",
    name: "LogIn",
    component: LogIn,
  },
  {
    path: "/register",
    name: "Register",
    component: Register,
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
        component: SprintBacklog,
      },
      {
        path: "SprintPlaning",
        component: SprintPlaning,
      },
      {
        path: "Statistic",
        component: Statistic,
      },
      {
        path: "Archive",
        component: Archive,
      },
    ],
  },
  {
    path: "/poker",
    name: "PlanningPoker",
    component: PlanningPoker,
  },
];

const router = new VueRouter({
  routes,
});

router.beforeEach((to, from, next) => {
  if (
    to.name !== "LogIn" &&
    !localStorage.getItem("token") &&
    to.name !== "Register"
  ) {
    if (to.name == "Register") {
      next({ name: "Register" });
    } else {
      next({ name: "LogIn" });
    }
  } else {
    next();
  }
});

export default router;
