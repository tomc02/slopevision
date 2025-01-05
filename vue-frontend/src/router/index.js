import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/HomeView.vue";
import PlaceDetail from "../views/PlaceDetail.vue";
import Login from "../views/LoginView.vue";
import Register from "../views/RegisterView.vue";
import LiveWebcams from "@/views/LiveWebcams.vue";
import UserProfile from "@/views/UserProfile.vue";
import EditProfile from "@/views/EditProfile.vue";
import store from '../store';

const routes = [
    {
        path: "/",
        name: "Home",
        component: Home,
        meta: { title: "Slope Vision", requiresAuth: false }
    },
    {
        path: "/live-webcams",
        name: "LiveWebcams",
        component: LiveWebcams,
        meta: { title: "Live Webcams - Slope Vision", requiresAuth: true }
    },
    {
        path: "/place/:id",
        name: "PlaceDetail",
        component: PlaceDetail,
        props: true,
        meta: { title: "Place Detail - Slope Vision", requiresAuth: true }
    },
    {
        path: "/login",
        name: "LoginView",
        component: Login,
        meta: { title: "Login - Slope Vision", requiresAuth: false }
    },
    {
        path: "/register",
        name: "RegisterView",
        component: Register,
        meta: { title: "Register - Slope Vision", requiresAuth: false }
    },
    {
        path: "/profile",
        name: "Profile",
        component: UserProfile,
        meta: { title: "Profile - Slope Vision", requiresAuth: true }
    },
    {
        path: "/profile/edit",
        name: "EditProfile",
        component: EditProfile,
        meta: { title: "Edit Profile - Slope Vision", requiresAuth: true }
    }
    /*{
        path: "/:catchAll(.*)",
        name: "NotFound",
        component: () => import("../views/NotFound.vue"),
        meta: { title: "Page Not Found" }
    },*/
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = store.getters['auth/isAuthenticated'];
  if (to.matched.some((record) => record.meta.requiresAuth) && !isAuthenticated) {
    next('/login');
  } else {
    next();
  }
  if (to.meta.title) {
    document.title = to.meta.title;
  }
});

export default router;
