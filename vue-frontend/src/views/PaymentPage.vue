<template>
  <div class="min-h-screen py-8">
    <div class="container mx-auto px-4">
      <!-- Page Title -->
      <h1 class="text-3xl font-bold mb-6 text-center text-primary-light dark:text-primary-dark">
        Complete Your Subscription
      </h1>

      <!-- Plan Summary -->
      <div class="w-full max-w-lg mx-auto bg-item-light-bg dark:bg-item-dark-bg rounded-lg shadow-lg p-6 mb-8">
        <h2 class="text-lg font-bold text-primary-light dark:text-primary-dark text-center">
          You're Upgrading to the <span class="text-indigo-600">{{ selectedPlan }}</span> Plan
        </h2>
        <p class="text-sm text-secondary-light dark:text-secondary-dark text-center mt-2">
          Price: <span class="font-semibold">{{ planPrice }}</span>/month
        </p>
      </div>

      <!-- Payment Form -->
      <div class="w-full max-w-lg mx-auto bg-item-light-bg dark:bg-item-dark-bg rounded-lg shadow-lg p-6">
        <form @submit.prevent="handlePayment">
          <!-- Cardholder Name -->
          <div class="mb-4">
            <label class="block text-sm text-secondary-light dark:text-secondary-dark mb-1">
              Cardholder Name
            </label>
            <input
              v-model="cardholderName"
              type="text"
              placeholder="John Doe"
              class="w-full p-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:bg-item-secondary-dark dark:border-gray-700 dark:text-secondary-dark"
              required
            />
          </div>

          <!-- Card Number -->
          <div class="mb-4">
            <label class="block text-sm text-secondary-light dark:text-secondary-dark mb-1">
              Card Number
            </label>
            <input
              v-model="cardNumber"
              type="text"
              placeholder="1234 5678 9012 3456"
              class="w-full p-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:bg-item-secondary-dark dark:border-gray-700 dark:text-secondary-dark"
              required
            />
          </div>

          <!-- Expiration Date & CVV -->
          <div class="flex gap-4 mb-6">
            <div class="w-1/2">
              <label class="block text-sm text-secondary-light dark:text-secondary-dark mb-1">
                Expiration Date
              </label>
              <input
                v-model="expiryDate"
                type="text"
                placeholder="MM/YY"
                class="w-full p-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:bg-item-secondary-dark dark:border-gray-700 dark:text-secondary-dark"
                required
              />
            </div>
            <div class="w-1/2">
              <label class="block text-sm text-secondary-light dark:text-secondary-dark mb-1">
                CVV
              </label>
              <input
                v-model="cvv"
                type="text"
                placeholder="123"
                class="w-full p-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:bg-item-secondary-dark dark:border-gray-700 dark:text-secondary-dark"
                required
              />
            </div>
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            class="w-full py-3 rounded-lg bg-indigo-600 text-white text-sm hover:bg-indigo-500 focus:ring-2 focus:ring-indigo-400"
          >
            Confirm Payment
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  // get the plan name and price from the route
  mounted() {
    if (!this.$route.params.plan || !this.$route.params.price) {
      this.$router.push("/upgrade-account");
    }
  },
  data() {
    const selectedPlan = this.$route.params.plan;
    const planPrice = this.$route.params.price;
    console.log(`Plan selected: ${selectedPlan} - Price: ${planPrice}`);
    return {
      selectedPlan: this.$route.params.plan,
      planPrice: this.$route.params.price,
      cardholderName: "",
      cardNumber: "",
      expiryDate: "",
      cvv: "",
    };
  },
};
</script>

<style scoped>
/* Add any additional scoped styles if necessary */
</style>
