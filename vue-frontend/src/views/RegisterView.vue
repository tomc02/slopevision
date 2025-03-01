<template>
  <div class="flex items-center justify-center py-8">
    <div class="w-full max-w-md px-6 py-8 bg-item-light-bg dark:bg-item-dark-bg rounded-lg shadow-lg">
      <h2 class="text-3xl font-bold text-center mb-6 text-primary-light dark:text-primary-dark">Create an Account</h2>
      <form class="space-y-6" @submit.prevent="handleRegister">
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

        <!-- Email Input -->
        <div>
          <input
              v-model="email"
              class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-t dark:bg-item-secondary-dark dark:border-gray-600 dark:text-secondary-dark bg-item-secondary-light"
              placeholder="Email"
              required
              type="email"
          />
        </div>

        <!-- Password Input -->
        <div>
          <input
              v-model="password1"
              class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-t dark:bg-item-secondary-dark dark:border-gray-600 dark:text-secondary-dark bg-item-secondary-light"
              placeholder="Password"
              required
              type="password"
          />
        </div>

        <!-- Confirm Password Input -->
        <div>
          <input
              v-model="password2"
              class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-t dark:bg-item-secondary-dark dark:border-gray-600 dark:text-secondary-dark bg-item-secondary-light"
              placeholder="Confirm Password"
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
            Register
          </button>
        </div>

        <!-- Footer/Links -->
        <div class="text-center mt-4">
          <p class="text-sm text-gray-600 dark:text-gray-400">
            Already have an account?
            <a class="text-indigo-600 dark:text-indigo-400 hover:underline" href="/login">
              Login here
            </a>
          </p>
        </div>

        <!-- Error Message -->
        <div v-if="authError" class="text-center mt-4">
          <p v-for="(error, index) in formattedErrors" :key="index" class="text-sm text-red-500 dark:text-red-400">
            {{ error }}
          </p>
        </div>
      </form>
    </div>
  </div>
</template>



<script>
import { mapActions, mapGetters } from 'vuex';

export default {
  data() {
    return {
      username: '',
      email: '',
      password1: '',
      password2: '',
    };
  },
  computed: {
    ...mapGetters('auth', ['authError']),
    formattedErrors() {
      return this.authError ? this.authError.split('\n') : [];
    },
  },
  methods: {
    ...mapActions('auth', ['register']),
    async handleRegister() {
      try {
        await this.register({
          username: this.username,
          email: this.email,
          password1: this.password1,
          password2: this.password2,
        });
        this.$router.push('/login'); // Redirect on success
      } catch (error) {
        console.error('Registration failed:', error);
      }
    },
  },
};
</script>


