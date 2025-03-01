import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import './assets/main.css'
import axios from 'axios';
import store from './store';
axios.defaults.headers.common['Authorization'] = `Token ${localStorage.getItem('authToken')}`;
await store.dispatch('auth/rehydrateState');
const app = createApp(App)
app.use(router);
app.use(store);
app.mount("#app");