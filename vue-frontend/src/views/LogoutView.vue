<template>
  <div class="py-8">
    <!-- Logout Success -->
    <div v-if="loggedOut"
         class="w-full max-w-lg mx-auto bg-item-light-bg dark:bg-item-dark-bg rounded-lg shadow-lg p-6 mt-8">
      <div class="text-center">
        <h2 class="text-xl font-semibold text-primary-light dark:text-primary-dark">
          You have been successfully logged out.
        </h2>
        <p class="text-sm text-secondary-light dark:text-secondary-dark mt-2">
          Thank you for using our service! We hope to see you again soon.
        </p>
      </div>
    </div>
    <div v-else>
      <div class="container mx-auto px-4">
        <!-- Page Title -->
        <h1 class="text-3xl font-bold mb-8 text-center text-primary-light dark:text-primary-dark">
          Log Out
        </h1>

        <!-- Confirmation Card -->
        <div class="w-full max-w-lg mx-auto bg-item-light-bg dark:bg-item-dark-bg rounded-lg shadow-lg p-6">
          <!-- Confirmation Question -->
          <div class="text-center mb-6">
            <h2 class="text-xl font-semibold text-primary-light dark:text-primary-dark">
              Are you sure you want to log out?
            </h2>
            <p class="text-sm text-secondary-light dark:text-secondary-dark mt-2">
              You will be logged out of your account, and any unsaved changes will be lost.
            </p>
          </div>

          <!-- Action Buttons -->
          <div class="mt-8 flex justify-center space-x-6">
            <button
                class="px-6 py-3 rounded-lg bg-red-600 text-white hover:bg-red-500 focus:ring-2 focus:ring-red-400 transition-all duration-200"
                @click="confirmLogout"
            >
              Yes, Log Out
            </button>
            <router-link
                class="px-6 py-3 rounded-lg bg-gray-600 text-white hover:bg-gray-500 focus:ring-2 focus:ring-gray-400 transition-all duration-200"
                to="/profile"
            >
              Cancel
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import store from '@/store';

export default {
  data() {
    return {
      loggedOut: false,
    };
  },
  methods: {
    confirmLogout() {
      this.loggedOut = true;
      store.dispatch('auth/logout')
          .then(() => {
            // wait 3 seconds before redirecting to the home page
            setTimeout(() => {
              this.$router.push({name: 'Home'});
            }, 3000);
          })
          .catch((error) => {
            console.error('Logout failed:', error);
            this.loggedOut = false;
          });
    },
  },
};
</script>

<style scoped>
/* Scoped styles for logout confirmation page */
</style>
