<template>
  <div class="bg-gray-200 dark:bg-gray-900 dark:text-gray-100 flex items-center justify-center py-8">
    <div class="w-full max-w-md px-6 py-8 bg-white dark:bg-gray-800 rounded-lg shadow-lg">
      <h2 class="text-3xl font-bold text-center mb-6 text-gray-800 dark:text-gray-100">Create an Account</h2>
      <form class="space-y-6" @submit.prevent="handleRegister">
        <!-- Username Input -->
        <div>
          <input
              v-model="username"
              class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-100"
              placeholder="Username"
              required
              type="text"
          />
        </div>

        <!-- Email Input -->
        <div>
          <input
              v-model="email"
              class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-100"
              placeholder="Email"
              required
              type="email"
          />
        </div>

        <!-- Password Input -->
        <div>
          <input
              v-model="password1"
              class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-100"
              placeholder="Password"
              required
              type="password"
          />
        </div>

        <!-- Confirm Password Input -->
        <div>
          <input
              v-model="password2"
              class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:bg-gray-700 dark:border-gray-600 dark:text-gray-100"
              placeholder="Confirm Password"
              required
              type="password"
          />
        </div>

        <!-- Submit Button -->
        <div>
          <button
              class="w-full py-3 bg-indigo-600 text-white font-semibold rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:bg-indigo-800 dark:hover:bg-indigo-700"
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
        <div v-if="authError" class="error">
          <p v-for="(error, index) in formattedErrors" :key="index" class="text-sm text-red-500 dark:text-red-400">{{ error }}</p>
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


