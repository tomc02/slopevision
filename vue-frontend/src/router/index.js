import {createRouter, createWebHistory} from "vue-router";
import Home from "../views/HomeView.vue";
import PlaceDetail from "../views/PlaceDetail.vue";
import Login from "../views/LoginView.vue";
import Register from "../views/RegisterView.vue";
import LiveWebcams from "@/views/LiveWebcams.vue";
import UserProfile from "@/views/UserProfile.vue";
import EditProfile from "@/views/EditProfile.vue";
import AccessDenied from "@/views/AccessDenied.vue";
import UpgradeAccount from "@/views/UpgradeAccount.vue";
import PaymentPage from "@/views/PaymentPage.vue";
import LogoutView from "@/views/LogoutView.vue";
import store from '../store';
import Favorites from "@/views/Favorites.vue";
const routes = [
    {
        path: "/",
        name: "Home",
        component: Home,
        meta: {title: "Slope Vision", requiresAuth: false, requiresPremium: false}
    },
    {
        path: "/live-webcams",
        name: "LiveWebcams",
        component: LiveWebcams,
        meta: {title: "Live Webcams - Slope Vision", requiresAuth: true, requiresPremium: true}
    },
    {
        path: "/favorites",
        name: "Favorites",
        component: Favorites,
        meta: {title: "Favorites - Slope Vision", requiresAuth: true, requiresPremium: true}
    },
    {
        path: "/place/:id",
        name: "PlaceDetail",
        component: PlaceDetail,
        props: true,
        meta: {title: "Place Detail - Slope Vision", requiresAuth: true, requiresPremium: true}
    },
    {
        path: "/login",
        name: "LoginView",
        component: Login,
        meta: {title: "Login - Slope Vision", requiresAuth: false, requiresPremium: false}
    },
    {
        path: "/register",
        name: "RegisterView",
        component: Register,
        meta: {title: "Register - Slope Vision", requiresAuth: false, requiresPremium: false}
    },
    {
        path: "/profile",
        name: "Profile",
        component: UserProfile,
        meta: {title: "Profile - Slope Vision", requiresAuth: true, requiresPremium: false}
    },
    {
        path: "/profile/edit",
        name: "EditProfile",
        component: EditProfile,
        meta: {title: "Edit Profile - Slope Vision", requiresAuth: true, requiresPremium: false}
    },
    {
        path: "/access-denied",
        name: "AccessDenied",
        component: AccessDenied,
        meta: {title: "Access Denied - Slope Vision", requiresAuth: false, requiresPremium: false}
    },
    {
        path: "/upgrade-account",
        name: "UpgradeAccount",
        component: UpgradeAccount,
        meta: {title: "Upgrade Account - Slope Vision", requiresAuth: true, requiresPremium: false}
    },
    {
        path: "/payment/:plan/:price",
        name: "PaymentPage",
        component: PaymentPage,
        meta: {title: "Payment - Slope Vision", requiresAuth: true, requiresPremium: false},
    },
    {
        path: "/logout",
        name: "Logout",
        component: LogoutView,
        meta: {title: "Logout - Slope Vision", requiresAuth: true, requiresPremium: false}
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
    const isPremium = store.getters['auth/isPremium'];
    if (to.meta.requiresAuth && !isAuthenticated) {
        next({name: 'LoginView'});
    } else if (to.meta.requiresPremium && !isPremium) {
        next({name: 'AccessDenied'});
    } else {
        next();
    }
    if (to.meta.title) {
        document.title = to.meta.title;
    }
});

export default router;
