import axios from 'axios';
import api from './api'

const AUTH_API_URL = '/api/auth/';
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.headers.common['Authorization'] = `Token ${localStorage.getItem('token')}`;
export default {
    register(user) {
        return api.post(AUTH_API_URL + 'registration/', {
            username: user.username, email: user.email, password1: user.password1, password2: user.password2,
        });
    }, login(user) {
        return api.post(AUTH_API_URL + 'login/', {
            username: user.username, password: user.password,
        });
    }, logout() {
        return api.post(AUTH_API_URL + 'logout/');
    }, getUserDetails() {
        return api.get(AUTH_API_URL + 'user/');
    }, getUser() {
        const token = localStorage.getItem('token');
        return api.get(AUTH_API_URL + 'user/', {
            headers: {
                'X-CSRFToken': `${token}`,
            }
        });
    }, updateUser(user) {
        if (user.image && !user.image.startsWith('http')) {
            user.profile_picture = user.image;
        }
        user.image = null;
        return api.put(AUTH_API_URL + 'user/', user);
    },
    refreshCsrfToken() {
        return api.get('/api/csrf/').then(response => {
            localStorage.setItem('csrfToken', response.data.csrfToken);
        }).catch(error => {
            console.error('Error fetching CSRF token:', error);
        });
    }
};
