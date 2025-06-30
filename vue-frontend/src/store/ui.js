const savedDataSaver = localStorage.getItem('dataSaver');
const state = {
  dataSaver: savedDataSaver ? JSON.parse(savedDataSaver) : false,
};

const mutations = {
  SET_DATA_SAVER(state, value) {
    state.dataSaver = value;
    localStorage.setItem('dataSaver', JSON.stringify(value));
  },
};

const actions = {
  toggleDataSaver({ commit, state }) {
    commit('SET_DATA_SAVER', !state.dataSaver);
  },
  setDataSaver({ commit }, value) {
    commit('SET_DATA_SAVER', value);
  },
};

const getters = {
  dataSaver: (state) => state.dataSaver,
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
  getters,
};
