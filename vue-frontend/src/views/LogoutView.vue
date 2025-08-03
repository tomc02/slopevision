<template>
  <div class="flex justify-center items-center px-4 py-12">
    <div class="w-full max-w-lg">
      <!-- Logout Success State -->
      <div v-if="loggedOut" class="text-center">
        <div class="bg-white dark:bg-gray-800 shadow-2xl p-8 border border-gray-200 dark:border-gray-700 rounded-2xl">
          <!-- Success Icon -->
          <div class="flex justify-center mb-6">
            <div class="bg-gradient-to-br from-green-500 to-blue-600 shadow-lg p-6 rounded-full">
              <CheckCircleIcon class="w-12 h-12 text-white" />
            </div>
          </div>
          
          <!-- Success Message -->
          <h2 class="mb-4 font-bold text-primary-light dark:text-primary-dark text-2xl">
            Successfully Logged Out
          </h2>
          <p class="mb-6 text-secondary-light dark:text-secondary-dark">
            Thank you for using SlopeVision! We hope to see you again soon.
          </p>

          <!-- Redirecting Message -->
          <div class="bg-blue-50 dark:bg-blue-900/20 mb-6 p-4 border border-blue-200 dark:border-blue-800 rounded-xl">
            <div class="flex justify-center items-center">
              <ArrowPathIcon class="mr-2 w-5 h-5 text-blue-500 animate-spin" />
              <span class="text-blue-700 dark:text-blue-400 text-sm">
                Redirecting to home page...
              </span>
            </div>
          </div>

          <!-- Quick Actions -->
          <div class="flex sm:flex-row flex-col gap-4">
            <router-link
              to="/login"
              @click="stopTimeout"
              class="flex-1 bg-gradient-to-r from-indigo-600 hover:from-indigo-500 to-purple-600 hover:to-purple-500 px-6 py-3 rounded-xl font-semibold text-white text-center hover:scale-105 transition-all duration-200 transform"
            >
              <ArrowRightOnRectangleIcon class="inline mr-2 w-5 h-5" />
              Sign In Again
            </router-link>
            <router-link
              to="/"
              class="flex-1 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 px-6 py-3 rounded-xl font-semibold text-gray-700 dark:text-gray-300 text-center transition-all duration-200"
            >
              <HomeIcon class="inline mr-2 w-5 h-5" />
              Go Home
            </router-link>
          </div>
        </div>
      </div>

      <!-- Logout Confirmation State -->
      <div v-else class="text-center">
        <div class="bg-white dark:bg-gray-800 shadow-2xl p-8 border border-gray-200 dark:border-gray-700 rounded-2xl">
          <!-- Warning Icon -->
          <div class="flex justify-center mb-6">
            <div class="bg-gradient-to-br from-orange-500 to-red-600 shadow-lg p-6 rounded-full">
              <ExclamationTriangleIcon class="w-12 h-12 text-white" />
            </div>
          </div>

          <!-- Confirmation Title -->
          <h2 class="mb-4 font-bold text-primary-light dark:text-primary-dark text-2xl">
            Confirm Logout
          </h2>
          <p class="mb-8 text-secondary-light dark:text-secondary-dark">
            Are you sure you want to log out? Any unsaved changes will be lost, and you'll need to sign in again to access your account.
          </p>

          <!-- Action Buttons -->
          <div class="flex sm:flex-row flex-col gap-4">
            <button
              @click="confirmLogout"
              :disabled="isLoggingOut"
              class="flex flex-1 justify-center items-center bg-gradient-to-r from-red-600 hover:from-red-500 disabled:from-gray-400 to-pink-600 hover:to-pink-500 disabled:to-gray-500 shadow-lg disabled:shadow-none px-6 py-4 rounded-xl font-semibold text-white disabled:transform-none hover:scale-105 transition-all duration-200 transform"
            >
              <ArrowPathIcon v-if="isLoggingOut" class="mr-2 w-5 h-5 animate-spin" />
              <span v-if="isLoggingOut">Logging Out...</span>
              <span v-else>
                <ArrowRightOnRectangleIcon class="inline mr-2 w-5 h-5" />
                Yes, Log Out
              </span>
            </button>
            <router-link
              to="/profile"
              class="flex flex-1 justify-center items-center bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 px-6 py-4 rounded-xl font-semibold text-gray-700 dark:text-gray-300 text-center transition-all duration-200"
            >
              <XMarkIcon class="inline mr-2 w-5 h-5" />
              Cancel
            </router-link>
          </div>

          <!-- Stay Signed In Option -->
          <div class="mt-6 pt-6 border-gray-200 dark:border-gray-700 border-t">
            <router-link
              to="/profile"
              class="inline-flex items-center font-medium text-indigo-600 hover:text-indigo-500 dark:hover:text-indigo-300 dark:text-indigo-400 text-sm"
            >
              <ArrowLeftIcon class="mr-2 w-4 h-4" />
              Return to Profile
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import store from '@/store';
import {
  CheckCircleIcon,
  ExclamationTriangleIcon,
  ArrowPathIcon,
  ArrowRightOnRectangleIcon,
  HomeIcon,
  XMarkIcon,
  ArrowLeftIcon
} from '@heroicons/vue/24/outline';

export default {
  components: {
    CheckCircleIcon,
    ExclamationTriangleIcon,
    ArrowPathIcon,
    ArrowRightOnRectangleIcon,
    HomeIcon,
    XMarkIcon,
    ArrowLeftIcon
  },
  data() {
    return {
      loggedOut: false,
      isLoggingOut: false,
    };
  },
  methods: {
    async confirmLogout() {
      this.isLoggingOut = true;
      try {
        await store.dispatch('auth/logout');
        localStorage.removeItem('token');
        this.loggedOut = true;
        
        // Wait 3 seconds before redirecting to the home page
        this.redirectTimeout = setTimeout(() => {
          this.$router.push({name: 'Home'});
        }, 3000);
      } catch (error) {
        console.error('Logout failed:', error);
        this.loggedOut = false;
      } finally {
        this.isLoggingOut = false;
      }
    },
    stopTimeout() {
      clearTimeout(this.redirectTimeout);
    }
  },
};
</script>

<style scoped>
/* Scoped styles for logout confirmation page */
</style>
