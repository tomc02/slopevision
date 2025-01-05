<template>
  <div class="flex items-center justify-center py-8">
    <div class="w-full max-w-md px-6 py-8 bg-item-light-bg dark:bg-item-dark-bg rounded-lg shadow-lg">
      <h2 class="text-3xl font-bold text-center mb-6 text-primary-light dark:text-primary-dark">Login to Your Account</h2>
      <form class="space-y-6" @submit.prevent="handleLogin">
        <!-- Username Input -->
        <div>
          <input
              v-model="username"
              class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-t dark:bg-item-secondary-dark dark:border-gray-600 dark:text-secondary-dark bg-item-secondary-light"
              placeholder="Username"
              required
              type="text"
          />
        </div>

        <!-- Password Input -->
        <div>
          <input
              v-model="password"
              class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-t dark:bg-item-secondary-dark dark:border-gray-600 dark:text-secondary-dark bg-item-secondary-light"
              placeholder="Password"
              required
              type="password"
          />
        </div>

        <!-- Submit Button -->
        <div>
          <button
              class="submit-button"
              type="submit"
          >
            Login
          </button>
        </div>

        <!-- Footer/Links -->
        <div class="text-center mt-4">
          <p class="text-sm text-gray-600 dark:text-gray-400">
            Don't have an account?
            <a class="text-indigo-600 dark:text-indigo-400 hover:underline" href="/register">
              Register here
            </a>
          </p>
        </div>

        <!-- Error Message -->
        <div v-if="authError" class="text-center mt-4">
          <p v-for="(error, index) in formattedErrors" :key="index" class="text-sm text-red-500 dark:text-red-400">
            {{ error }}</p>
        </div>
      </form>
    </div>
  </div>
</template>


<script>
import {mapActions, mapGetters} from 'vuex';

export default {
  data() {
    return {
      username: '',
      password: '',
    };
  },
  computed: {
    ...mapGetters('auth', ['authError']),
    formattedErrors() {
      // if err contain 'non_field_errors' display it without the field name
      if (this.authError && this.authError.includes('non_field_errors')) {
        return this.authError.split(':')[1].split('\n');
      } else {
        return this.authError ? this.authError.split('\n') : [];
      }
    },
  },
  methods: {
    ...mapActions('auth', ['login']),
    async handleLogin() {
      try {
        await this.login({
          username: this.username,
          password: this.password,
        });
        this.$router.push('/'); // Redirect on success
      } catch (error) {
        // Show error message to user
      }
    },
  },
};
</script>
