<template>
  <div class="py-8">
    <div class="mx-auto px-4 max-w-6xl container">
      <!-- Page Header -->
      <div class="mb-12 text-center">
        <h1 class="mb-4 font-bold text-primary-light dark:text-primary-dark text-4xl">
          User Profile
        </h1>
        <p class="text-secondary-light dark:text-secondary-dark text-lg">
          Manage your account settings and subscription
        </p>
      </div>

      <div class="gap-8 grid lg:grid-cols-3">
        <!-- Profile Card -->
        <div class="lg:col-span-2">
          <div class="bg-white dark:bg-gray-800 shadow-xl p-8 border border-gray-200 dark:border-gray-700 rounded-2xl">
            <!-- Profile Header -->
            <div class="flex sm:flex-row flex-col items-center sm:items-start sm:space-x-6 space-y-4 sm:space-y-0 mb-8">
              <div class="relative">
                <div class="ring-opacity-50 rounded-full ring-4 ring-indigo-500 w-32 h-32 overflow-hidden">
                  <img
                    :src="userProfile.image || '/default-avatar.svg'"
                    alt="Profile Picture"
                    class="w-full h-full object-cover"
                  />
                </div>
                <div class="-right-2 -bottom-2 absolute">
                  <span class="inline-flex items-center px-3 py-1 rounded-full font-medium text-xs"
                        :class="userProfile.accountType === 'Premium' ? 'bg-yellow-500 text-white' : 'bg-gray-200 dark:bg-gray-600 text-gray-700 dark:text-gray-300'">
                    {{ userProfile.accountType }}
                  </span>
                </div>
              </div>
              
              <div class="flex-1 sm:text-left text-center">
                <h2 class="mb-2 font-bold text-primary-light dark:text-primary-dark text-2xl">
                  {{ userProfile.name || "User Name" }}
                </h2>
                <p class="mb-2 text-secondary-light dark:text-secondary-dark text-lg">
                  {{ userProfile.email || "user@example.com" }}
                </p>
                <p class="text-gray-500 dark:text-gray-400 text-sm">
                  @{{ userProfile.username || "username" }}
                </p>
              </div>
            </div>

            <!-- Profile Details Grid -->
            <div class="gap-6 grid md:grid-cols-2 mb-8">
              <div class="bg-gray-50 dark:bg-gray-700 p-4 rounded-xl">
                <div class="flex items-center space-x-3">
                  <div class="bg-indigo-100 dark:bg-indigo-900 p-2 rounded-lg">
                    <UserIcon class="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
                  </div>
                  <div>
                    <p class="text-gray-500 dark:text-gray-400 text-xs uppercase tracking-wide">Username</p>
                    <p class="font-semibold text-primary-light dark:text-primary-dark">{{ userProfile.username }}</p>
                  </div>
                </div>
              </div>

              <div class="bg-gray-50 dark:bg-gray-700 p-4 rounded-xl">
                <div class="flex items-center space-x-3">
                  <div class="bg-green-100 dark:bg-green-900 p-2 rounded-lg">
                    <CalendarDaysIcon class="w-5 h-5 text-green-600 dark:text-green-400" />
                  </div>
                  <div>
                    <p class="text-gray-500 dark:text-gray-400 text-xs uppercase tracking-wide">Member Since</p>
                    <p class="font-semibold text-primary-light dark:text-primary-dark">{{ userProfile.memberSince }}</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="flex sm:flex-row flex-col sm:space-x-4 space-y-3 sm:space-y-0">
              <router-link
                to="/profile/edit"
                class="flex-1 bg-indigo-600 hover:bg-indigo-500 px-6 py-3 rounded-xl font-semibold text-white text-center hover:scale-105 transition-all duration-200 transform"
              >
                <PencilIcon class="inline mr-2 w-5 h-5" />
                Edit Profile
              </router-link>
              <button
                @click="logout"
                class="flex-1 bg-red-500 hover:bg-red-400 px-6 py-3 rounded-xl font-semibold text-white hover:scale-105 transition-all duration-200 transform"
              >
                <ArrowRightOnRectangleIcon class="inline mr-2 w-5 h-5" />
                Logout
              </button>
            </div>
          </div>
        </div>

        <!-- Subscription Card -->
        <div class="lg:col-span-1">
          <div class="bg-white dark:bg-gray-800 shadow-xl p-6 border border-gray-200 dark:border-gray-700 rounded-2xl h-fit">
            <div class="mb-6 text-center">
              <div class="flex justify-center items-center bg-indigo-600 mx-auto mb-4 rounded-full w-16 h-16">
                <CreditCardIcon class="w-8 h-8 text-white" />
              </div>
              <h3 class="mb-2 font-bold text-primary-light dark:text-primary-dark text-xl">
                Subscription
              </h3>
            </div>

            <div class="space-y-4">
              <!-- Current Plan -->
              <div class="bg-gray-50 dark:bg-gray-700 p-4 rounded-xl">
                <div class="flex justify-between items-center mb-2">
                  <span class="text-gray-500 dark:text-gray-400 text-sm">Current Plan</span>
                  <span class="font-semibold text-lg"
                        :class="userProfile.accountType === 'Premium' ? 'text-yellow-600 dark:text-yellow-400' : 'text-gray-600 dark:text-gray-400'">
                    {{ userProfile.accountType }}
                  </span>
                </div>
              </div>

              <!-- Next Payment (only for Premium) -->
              <div v-if="userProfile.accountType === 'Premium'" class="bg-gray-50 dark:bg-gray-700 p-4 rounded-xl">
                <div class="flex justify-between items-center mb-2">
                  <span class="text-gray-500 dark:text-gray-400 text-sm">Next Payment</span>
                  <span class="font-semibold text-primary-light dark:text-primary-dark">
                    {{ subscription.nextPayment }}
                  </span>
                </div>
                <div class="flex justify-between items-center">
                  <span class="text-gray-500 dark:text-gray-400 text-sm">Amount</span>
                  <span class="font-semibold text-primary-light dark:text-primary-dark">
                    ${{ subscription.amount }}/month
                  </span>
                </div>
              </div>

              <!-- Subscription Actions -->
              <div class="space-y-3">
                <router-link
                  v-if="userProfile.accountType === 'Free'"
                  to="/upgrade-account"
                  class="block bg-yellow-500 hover:bg-yellow-400 px-4 py-3 rounded-xl w-full font-semibold text-white text-center hover:scale-105 transition-all duration-200 transform"
                >
                  <StarIcon class="inline mr-2 w-5 h-5" />
                  Upgrade to Premium
                </router-link>
                
                <div v-else class="space-y-2">
                  <button class="bg-gray-200 hover:bg-gray-300 dark:bg-gray-600 dark:hover:bg-gray-500 px-4 py-3 rounded-xl w-full font-medium text-gray-700 dark:text-gray-300 transition-colors duration-200">
                    Manage Subscription
                  </button>
                  <button class="bg-red-500 hover:bg-red-400 px-4 py-2 rounded-xl w-full font-medium text-white text-sm transition-colors duration-200">
                    Cancel Subscription
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {computed, onMounted, ref, getCurrentInstance} from "vue";
import store from "@/store";
import subscriptionService from "@/services/subscriptionService";
import {
  UserIcon,
  CalendarDaysIcon,
  PencilIcon,
  ArrowRightOnRectangleIcon,
  CreditCardIcon,
  StarIcon
} from '@heroicons/vue/24/outline';

export default {
  setup() {
    const instance = getCurrentInstance();
    const user = computed(() => store.getters['auth/currentUser'] || {});
    const subscription = ref({
      nextPayment: null,
      amount: null,
      status: 'inactive'
    });
    const isLoadingSubscription = ref(false);

    const memberSince = user.value.date_joined ? new Date(user.value.date_joined) : new Date();
    const accountType = user.value.account_type === 'free' ? 'Free' : 'Premium';
    
    const userProfile = ref({
      image: user.value.profile_picture,
      name: user.value.name,
      email: user.value.email,
      username: user.value.username,
      accountType: accountType,
      memberSince: memberSince.toLocaleString('default', {month: 'long', year: 'numeric'}),
    });

    const fetchSubscriptionData = async () => {
      if (accountType === 'Premium') {
        isLoadingSubscription.value = true;
        try {
          const response = await subscriptionService.getSubscription();
          subscription.value = {
            nextPayment: new Date(response.data.next_payment_date).toLocaleDateString(),
            amount: response.data.amount,
            status: response.data.status
          };
        } catch (error) {
          console.error('Failed to fetch subscription data:', error);
          // Fallback to mock data
          const nextPaymentDate = new Date();
          nextPaymentDate.setMonth(nextPaymentDate.getMonth() + 1);
          subscription.value = {
            nextPayment: nextPaymentDate.toLocaleDateString(),
            amount: 9.99,
            status: 'active'
          };
        } finally {
          isLoadingSubscription.value = false;
        }
      }
    };

    const logout = async () => {
      try {
        await store.dispatch('auth/logout');
        localStorage.removeItem('token');
        instance.proxy.$router.push('/login');
      } catch (error) {
        console.error('Logout error:', error);
      }
    };

    onMounted(() => {
      fetchSubscriptionData();
    });

    return {
      userProfile,
      subscription,
      isLoadingSubscription,
      logout
    };
  },
  components: {
    UserIcon,
    CalendarDaysIcon,
    PencilIcon,
    ArrowRightOnRectangleIcon,
    CreditCardIcon,
    StarIcon
  },
};
</script>

<style scoped>
</style>