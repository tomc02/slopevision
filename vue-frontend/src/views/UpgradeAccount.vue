<template>
  <div class="py-8">
    <div class="container mx-auto px-4">
      <!-- Page Title -->
      <h1 class="text-3xl font-bold mb-6 text-center text-primary-light dark:text-primary-dark">
        Upgrade Your Account
      </h1>

      <!-- Subtitle -->
      <p class="text-center text-sm text-secondary-light dark:text-secondary-dark mb-10">
        Unlock full access to webcams, historical imagery, and more by upgrading your plan.
      </p>

      <!-- Pricing Plans -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
        <!-- Free Plan -->
        <div class="p-6 bg-item-light-bg dark:bg-item-dark-bg rounded-lg shadow-lg border border-gray-200 dark:border-gray-700">
          <h2 class="text-xl font-bold text-primary-light dark:text-primary-dark text-center mb-4">
            Free
          </h2>
          <p class="text-center text-gray-600 dark:text-gray-400 mb-6">
            Explore basic features of the app.
          </p>
          <div class="text-center text-3xl font-bold text-indigo-600 mb-4">
            Free
          </div>
          <ul class="space-y-2 text-sm text-secondary-light dark:text-secondary-dark mb-6">
            <li>✔ User account management</li>
            <li>✔ Preview a single selected place</li>
            <li>✔ Access to informational pages</li>
            <li>✘ No access to webcams</li>
            <li>✘ No favorites or historical data</li>
          </ul>
          <div class="text-center">
            <span
              class="px-6 py-2 rounded-lg bg-gray-300 text-gray-600 text-sm cursor-not-allowed"
            >
              Current Plan
            </span>
          </div>
        </div>

        <!-- Premium Plan -->
        <div class="p-6 bg-item-light-bg dark:bg-item-dark-bg rounded-lg shadow-lg border-2 border-indigo-600">
          <h2 class="text-xl font-bold text-primary-light dark:text-primary-dark text-center mb-4">
            Premium
          </h2>
          <p class="text-center text-gray-600 dark:text-gray-400 mb-6">
            Unlock the full app experience.
          </p>
          <div class="text-center text-3xl font-bold text-indigo-600 mb-4">
            $9.99/month
          </div>
          <ul class="space-y-2 text-sm text-secondary-light dark:text-secondary-dark mb-6">
            <li>✔ Access all live webcams</li>
            <li>✔ Save your favorite spots</li>
            <li>✔ Browse historical images</li>
            <li>✔ Plan your perfect powder day</li>
          </ul>
          <div class="text-center">
            <button
              @click="selectPlan('Premium')"
              class="px-6 py-2 rounded-lg bg-indigo-600 text-white text-sm hover:bg-indigo-500 focus:ring-2 focus:ring-indigo-400"
            >
              Upgrade to Premium
            </button>
          </div>
        </div>

        <!-- Pro Plan -->
        <div class="p-6 bg-item-light-bg dark:bg-item-dark-bg rounded-lg shadow-lg border border-gray-200 dark:border-gray-700">
          <h2 class="text-xl font-bold text-primary-light dark:text-primary-dark text-center mb-4">
            Pro
          </h2>
          <p class="text-center text-gray-600 dark:text-gray-400 mb-6">
            For enthusiasts and supporters of the app.
          </p>
          <div class="text-center text-3xl font-bold text-indigo-600 mb-4">
            $29.99/month
          </div>
          <ul class="space-y-2 text-sm text-secondary-light dark:text-secondary-dark mb-6">
            <li>✔ All Premium features</li>
            <li>✔ Historical images in higher quality</li>
            <li>✔ Data-saving mode for efficient streaming</li>
            <li>✔ Support app development</li>
          </ul>
          <div class="text-center">
            <button
              @click="selectPlan('Pro')"
              class="px-6 py-2 rounded-lg bg-indigo-600 text-white text-sm hover:bg-indigo-500 focus:ring-2 focus:ring-indigo-400"
            >
              Upgrade to Pro
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    selectPlan(plan) {
      // Redirect to payment or plan details page
      console.log(`Plan selected: ${plan}`);
      const price = plan === "Premium" ? 9.99 : 29.99;
      this.$router.push({ name: "PaymentPage", params: { plan:plan, price:price} });
    },
  },
};
</script>

<style scoped>
/* Add any additional scoped styles if necessary */
</style>
