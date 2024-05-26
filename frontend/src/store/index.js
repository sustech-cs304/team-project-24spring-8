// src/store/index.js
import { createStore } from 'vuex';

const store = createStore({
  state() {
    return {
      isAuthenticated: false
    };
  },
  mutations: {
    authenticate(state) {
      state.isAuthenticated = true;
    },
    logout(state) {
      state.isAuthenticated = false;
    }
  },
  actions: {
    authenticate({ commit }) {
      commit('authenticate');
    },
    logout({ commit }) {
      commit('logout');
    }
  },
  getters: {
    isAuthenticated: (state) => state.isAuthenticated
  }
});

export default store;
