import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import './assets/main.css'
import store from './store';
import api from './services/api'
import axios from 'axios';

// Fetch CSRF token when app starts
const fetchCSRFToken = async () => {
  try {
    const response = await api.get('/api/csrf/')
    localStorage.setItem('csrfToken', response.data.csrfToken)
  } catch (error) {
    console.error('Error fetching CSRF token:', error)
  }
}

fetchCSRFToken();

axios.defaults.headers.common['Authorization'] = `Token ${localStorage.getItem('authToken')}`;
await store.dispatch('auth/rehydrateState');


const app = createApp(App)
app.use(router);
app.use(store);
app.mount("#app");