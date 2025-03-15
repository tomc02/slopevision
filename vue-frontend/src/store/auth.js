import AuthService from '@/services/authService';

const state = {
    user: null,
    isAuthenticated: false,
    errorMessage: null,
};

const mutations = {
    SET_USER(state, user) {
        console.log('SET_USER', user);
        state.user = user;
        state.isAuthenticated = !!user;
        state.isPremium = true;//user?.account_type !== 'free';
        console.log('state.isPremium', state.isPremium);
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
            await AuthService.register(user);
            const userDetail = await AuthService.getUserDetails();
            commit('SET_USER', userDetail.data);
            commit('CLEAR_ERROR');
        } catch (error) {
            commit('SET_ERROR', error.response.key);
        }
    },
    async login({commit}, user) {
        try {
            const response = await AuthService.login(user);
            localStorage.setItem('token', response.data.token);
            commit('SET_USER', response.data.user);
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
    async rehydrateState({commit}) {
        const token = localStorage.getItem('token');
        if (token) {
            try {
                const response = await AuthService.getUser();
                commit('SET_USER', response.data);
            } catch {
                localStorage.removeItem('token');
                commit('SET_USER', null);
            }
        }
    },
};

const getters = {
    isAuthenticated: (state) => state.isAuthenticated,
    currentUser: (state) => state.user,
    authError: (state) => state.errorMessage,
    isPremium: (state) => state.isPremium,
};

export default {
    namespaced: true,
    state,
    mutations,
    actions,
    getters,
};
