<template>
  <div class="py-8">
    <div class="container mx-auto px-4">
      <!-- Page Title -->
      <h1 class="text-3xl font-bold mb-6 text-center text-primary-light dark:text-primary-dark">
        Premium Access Required
      </h1>

      <!-- Message Card -->
      <div class="w-full max-w-xl mx-auto bg-item-light-bg dark:bg-item-dark-bg rounded-lg shadow-lg p-6 text-center">
        <div class="mb-4">
          <!-- Lock Icon -->
          <div class="mx-auto w-16 h-16 bg-indigo-600 text-white rounded-full flex items-center justify-center">
            <LockClosedIcon class="w-8 h-8"/>
          </div>
          <p class="text-lg font-semibold text-primary-light dark:text-primary-dark mb-2 mt-2">
            Access Restricted
          </p>
          <p class="text-sm text-secondary-light dark:text-secondary-dark mb-6">
            This feature is available only for premium users. Upgrade your account to enjoy full access.
          </p>

          <!-- Upgrade Button -->
          <div>
            <router-link
                class="px-6 py-2 rounded-lg bg-indigo-600 text-white text-sm hover:bg-indigo-500 focus:ring-2 focus:ring-indigo-400"
                to="/upgrade-account"
            >
              Upgrade to Premium
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {LockClosedIcon} from "@heroicons/vue/24/outline";

export default {
  name: "AccessDenied",
  components: {
    LockClosedIcon,
  },
};
</script>

<style scoped>
/* Add any additional scoped styles if necessary */
</style>
