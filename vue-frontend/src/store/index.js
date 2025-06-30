import { createStore } from 'vuex';
import auth from './auth';
import ui from './ui'; // add this line

const store = createStore({
  modules: {
    auth,
    ui, // add this line
  },
});

export default store;
