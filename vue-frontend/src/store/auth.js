import AuthService from '@/services/authService';

const state = {
    user: null,
    isAuthenticated: false,
    errorMessage: null,
};

const mutations = {
    SET_USER(state, user) {
        state.user = user;
        state.isAuthenticated = !!user;
    },
    SET_ERROR(state, errors) {
        if (errors && typeof errors === 'object') {
            state.errorMessage = Object.entries(errors)
                .map(([field, messages]) => `${field}: ${messages.join(', ')}`)
                .join('\n');
        } else {
            state.errorMessage = 'An unexpected error occurred.';
        }
    },
    CLEAR_ERROR(state) {
        state.errorMessage = null;
    },
};

const actions = {
    async register({commit}, user) {
        try {
            const response = await AuthService.register(user);
            const userDetail = await AuthService.getUserDetails();
            userDetail.data.key = response.data.key;
            commit('SET_USER', userDetail.data);
            commit('CLEAR_ERROR');
        } catch (error) {
            commit('SET_ERROR', error.response.key);
        }
    },
    async login({commit}, user) {
        try {
            const response = await AuthService.login(user);
            const userDetail = await AuthService.getUserDetails();
            userDetail.data.key = response.data.key;
            commit('SET_USER', userDetail.data);
            commit('CLEAR_ERROR');
        } catch (error) {
            commit('SET_ERROR', error.response.data);
            throw error;
        }
    },
    async logout({commit}) {
        try {
            await AuthService.logout();
            commit('SET_USER', null);
            commit('CLEAR_ERROR');
        } catch (error) {
            commit('SET_ERROR', error.response.data);
            throw error;
        }
    },
};

const getters = {
    isAuthenticated: (state) => state.isAuthenticated,
    currentUser: (state) => state.user,
    authError: (state) => state.errorMessage,
};

export default {
    namespaced: true,
    state,
    mutations,
    actions,
    getters,
};
