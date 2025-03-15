import axiosClient from '../main';
const API_URL = '';
export default {
    register(user) {
        return axiosClient.post(API_URL + 'registration/', {
            username: user.username, email: user.email, password: user.password1
        });
    }, login(user) {
        return axiosClient.post(API_URL + 'login/', {
            username: user.username, password: user.password,
        });
    }, logout() {
        return axiosClient.post(API_URL + 'logout/');
    }, getUserDetails() {
        return axiosClient.get(API_URL + 'user/');
    }, getUser() {
        const token = localStorage.getItem('token');
        return axiosClient.get(API_URL + 'user/', {
            headers: {
                Authorization: `Token ${token}`,
            }
        });
    }, updateUser(user) {
        if (user.image && !user.image.startsWith('http')) {
            user.profile_picture = user.image;
        }
        user.image = null;
        return axiosClient.put(API_URL + 'user/', user);
    },
};
