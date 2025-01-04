import { createStore } from 'vuex';
import VuexPersist from 'vuex-persist';
import auth from './auth';

const vuexPersist = new VuexPersist({
  key: 'auth',
  storage: window.localStorage,
  modules: ['auth'],
});

const store = createStore({
  modules: {
    auth,
  },
  plugins: [vuexPersist.plugin],
});

export default store;
