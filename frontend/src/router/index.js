import Vue from "vue";
import Router from "vue-router";

// Routes
import paths from "./paths";

function route(path, view, name, meta) {
  return {
    name: name || view,
    path,
    component: resolve => import(`@/views/${view}.vue`).then(resolve),
    meta
  };
}

Vue.use(Router);

// Create a new router
const router = new Router({
  mode: "history",
  routes: paths
    .map(path => route(path.path, path.view, path.name, path.meta))
    .concat([{
      path: "*",
      redirect: "/"
    }]),
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    }
    if (to.hash) {
      return {
        selector: to.hash
      };
    }
    return {
      x: 0,
      y: 0
    };
  }
});

router.beforeEach(function (to, from, next) {
  // console.log(to.matched)

  const user_pk = localStorage.getItem("pk")
  if (to.matched.some(function(routeInfo) {
    return routeInfo.meta.authRequired;
  })) {
    if (user_pk) {
      next();
    } else {
      alert('Login Please!');
      router.push("/");
    }
  } else {
    next();
  }
});

export default router;