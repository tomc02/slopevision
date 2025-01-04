import axios from 'axios';

const API_URL = '/api/auth/';
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.headers.common['Authorization'] = `Token ${localStorage.getItem('token')}`;
export default {
    register(user) {
        return axios.post(API_URL + 'registration/', {
            username: user.username,
            email: user.email,
            password1: user.password1,
            password2: user.password2,
        });
    },
    login(user) {
        return axios.post(API_URL + 'login/', {
            username: user.username,
            password: user.password,
        });
    },
    logout() {
        return axios.post(API_URL + 'logout/');
    },
    getUserDetails() {
        return axios.get(API_URL + 'user/');
    },
    getUser() {
        const token = localStorage.getItem('token');
        return axios.get(API_URL + 'user/', {
            headers: {
                Authorization: `Token ${token}`,
            }
        });
    },
};
