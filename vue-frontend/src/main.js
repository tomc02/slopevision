import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import './assets/main.css'
import axios from 'axios';
const axiosClient = axios.create({
    baseURL: process.env.VUE_APP_API_BASE_URL,  // Access the base URL from the environment variable
    headers: {
        'Content-Type': 'application/json',
    },
});
export default axiosClient;
import store from './store';
axiosClient.defaults.headers.common['Authorization'] = `Token ${localStorage.getItem('authToken')}`;
await store.dispatch('auth/rehydrateState');
const app = createApp(App)
app.use(router);
app.use(store);
app.mount("#app");