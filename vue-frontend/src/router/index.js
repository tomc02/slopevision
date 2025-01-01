import {createRouter, createWebHistory} from "vue-router";
import Home from "../views/HomeView.vue";
import PlaceDetail from "../views/PlaceDetail.vue";

const routes = [
    {
        path: "/",
        name: "Home",
        component: Home,
        meta: {title: "Slope Vision"}
    },
    {
        path: "/place/:id",
        name: "PlaceDetail",
        component: PlaceDetail,
        props: true,
        meta: {title: "Slope Vision"}
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
