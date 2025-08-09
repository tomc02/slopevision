<template>
  <div class="flex justify-center items-center p-4">
    <div class="w-full max-w-md">
      <!-- Header -->
      <div class="mb-6 text-center">
        <div class="flex justify-center mb-4">
          <div class="bg-gradient-to-br from-indigo-500 to-purple-600 shadow-lg p-3 rounded-2xl">
            <LockClosedIcon class="w-10 h-10 text-white" />
          </div>
        </div>
        <h2 class="mb-2 font-bold text-primary-light dark:text-primary-dark text-2xl">
          Welcome Back
        </h2>
        <p class="text-secondary-light dark:text-secondary-dark text-sm">
          Sign in to your account to continue
        </p>
      </div>

      <!-- Login Form -->
      <div class="bg-white dark:bg-gray-800 shadow-2xl p-6 border border-gray-200 dark:border-gray-700 rounded-2xl">
        <form class="space-y-4" @submit.prevent="handleLogin">
          <!-- Username Input -->
          <div class="group">
            <label for="username" class="block mb-2 font-semibold text-gray-700 dark:text-gray-300 text-sm">
              <UserIcon class="inline mr-2 w-4 h-4" />
              Username
            </label>
            <input
              id="username"
              v-model="username"
              type="text"
              class="bg-gray-50 dark:bg-gray-700 p-3 border-2 border-gray-200 dark:border-gray-600 focus:border-transparent rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 w-full text-primary-light dark:text-primary-dark transition-all duration-200"
              placeholder="Enter your username"
              required
            />
          </div>

          <!-- Password Input -->
          <div class="group">
            <label for="password" class="block mb-2 font-semibold text-gray-700 dark:text-gray-300 text-sm">
              <LockClosedIcon class="inline mr-2 w-4 h-4" />
              Password
            </label>
            <div class="relative">
              <input
                id="password"
                v-model="password"
                :type="showPassword ? 'text' : 'password'"
                class="bg-gray-50 dark:bg-gray-700 p-3 pr-12 border-2 border-gray-200 dark:border-gray-600 focus:border-transparent rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 w-full text-primary-light dark:text-primary-dark transition-all duration-200"
                placeholder="Enter your password"
                required
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="right-0 absolute inset-y-0 flex items-center pr-3 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors duration-200"
              >
                <EyeIcon v-if="!showPassword" class="w-4 h-4" />
                <EyeSlashIcon v-else class="w-4 h-4" />
              </button>
            </div>
          </div>

          <!-- Remember Me & Forgot Password -->
          <div class="flex justify-between items-center pt-2">
            <div class="flex items-center">
              <input
                id="remember-me"
                v-model="rememberMe"
                type="checkbox"
                class="bg-gray-100 dark:bg-gray-700 mt-0.5 border-gray-300 dark:border-gray-600 rounded focus:ring-2 focus:ring-indigo-500 w-4 h-4 text-indigo-600"
              />
              <label for="remember-me" class="ml-2 text-gray-600 dark:text-gray-400 text-xs">
                Remember me
              </label>
            </div>
            <a href="#" class="text-indigo-600 dark:text-indigo-400 text-xs hover:underline">
              Forgot password?
            </a>
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            :disabled="isLoading"
            class="flex justify-center items-center bg-gradient-to-r from-indigo-600 hover:from-indigo-500 disabled:from-gray-400 to-purple-600 hover:to-purple-500 disabled:to-gray-500 shadow-lg disabled:shadow-none px-6 py-3 rounded-xl w-full font-semibold text-white disabled:transform-none hover:scale-105 transition-all duration-200 transform"
          >
            <ArrowPathIcon v-if="isLoading" class="mr-2 w-4 h-4 animate-spin" />
            <span v-if="isLoading">Signing In...</span>
            <span v-else>
              <ArrowRightOnRectangleIcon class="inline mr-2 w-4 h-4" />
              Sign In
            </span>
          </button>

          <!-- Divider -->
          <div class="relative my-4">
            <div class="absolute inset-0 flex items-center">
              <div class="border-gray-300 dark:border-gray-600 border-t w-full"></div>
            </div>
            <div class="relative flex justify-center text-xs">
              <span class="bg-white dark:bg-gray-800 px-3 text-gray-500 dark:text-gray-400">
                Don't have an account?
              </span>
            </div>
          </div>

          <!-- Register Link -->
          <router-link
            to="/register"
            class="block bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 px-4 py-3 rounded-xl w-full font-medium text-gray-700 dark:text-gray-300 text-sm text-center transition-all duration-200"
          >
            <UserPlusIcon class="inline mr-2 w-4 h-4" />
            Create New Account
          </router-link>

          <!-- Error Messages -->
          <div v-if="authError" class="bg-red-50 dark:bg-red-900/20 p-3 border border-red-200 dark:border-red-800 rounded-xl">
            <div class="flex items-start">
              <ExclamationTriangleIcon class="flex-shrink-0 mt-0.5 mr-2 w-4 h-4 text-red-400" />
              <div class="text-xs">
                <p v-for="(error, index) in formattedErrors" :key="index" class="text-red-700 dark:text-red-400">
                  {{ error }}
                </p>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>


<script>
import {mapActions, mapGetters} from 'vuex';
import {
  LockClosedIcon,
  UserIcon,
  EyeIcon,
  EyeSlashIcon,
  ArrowPathIcon,
  ArrowRightOnRectangleIcon,
  UserPlusIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline';

export default {
  components: {
    LockClosedIcon,
    UserIcon,
    EyeIcon,
    EyeSlashIcon,
    ArrowPathIcon,
    ArrowRightOnRectangleIcon,
    UserPlusIcon,
    ExclamationTriangleIcon
  },
  data() {
    return {
      username: '',
      password: '',
      showPassword: false,
      rememberMe: false,
      isLoading: false,
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
      this.isLoading = true;
      try {
        await this.login({
          username: this.username,
          password: this.password,
        });
        this.$router.push('/'); // Redirect on success
      } catch (error) {
        // Show error message to user
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>
