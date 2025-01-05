<template>
  <div class="py-8">
    <div class="container mx-auto px-4">
      <!-- Page Title -->
      <h1 class="text-3xl font-bold mb-8 text-center text-primary-light dark:text-primary-dark">
        User Profile
      </h1>

      <!-- Profile Card -->
      <div class="w-full max-w-2xl mx-auto bg-item-light-bg dark:bg-item-dark-bg rounded-lg shadow-lg p-6">
        <!-- Profile Image -->
        <div class="flex items-center justify-center mb-6">
          <div class="w-24 h-24 rounded-full overflow-hidden shadow-md">
            <img
              :src="userProfile.image"
              alt="Profile Picture"
              class="object-cover w-full h-full"
            />
          </div>
        </div>

        <!-- User Details -->
        <div class="text-center mb-6">
          <h2 class="text-xl font-semibold text-primary-light dark:text-primary-dark">
            {{ userProfile.name || "-" }}
          </h2>
          <p class="text-sm text-secondary-light dark:text-secondary-dark">
            {{ userProfile.email || "user@example.com" }}
          </p>
        </div>

        <!-- Profile Info -->
        <div class="space-y-4">
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-600 dark:text-gray-400">
              Username:
            </span>
            <span class="text-sm font-semibold text-primary-light dark:text-primary-dark">
              {{ userProfile.username || "johndoe" }}
            </span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-600 dark:text-gray-400">
              Account Type:
            </span>
            <span class="text-sm font-semibold text-primary-light dark:text-primary-dark">
              {{ userProfile.accountType || "Standard" }}
            </span>
          </div>
          <div class="flex justify-between items-center">
            <span class="text-sm text-gray-600 dark:text-gray-400">
              Member Since:
            </span>
            <span class="text-sm font-semibold text-primary-light dark:text-primary-dark">
              {{ userProfile.memberSince || "January 2022" }}
            </span>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="mt-8 flex justify-center space-x-4">
          <router-link
            to="/profile/edit"
            class="px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-500 focus:ring-2 focus:ring-indigo-400"
          >
          Edit Profile
          </router-link>
          <button
            @click="logout"
            class="px-4 py-2 rounded-lg bg-red-600 text-white hover:bg-red-500 focus:ring-2 focus:ring-red-400"
          >
            Logout
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {computed} from "vue";
import store from "@/store";
export default {
  data() {
    const user = computed(() => store.getters['auth/currentUser'] || 'User');
    const memberSince = new Date(user.value.date_joined);
    const accountType = user.value.account_type === 'free' ? 'Free' : 'Premium';
    return {
      userProfile: {
        image: user.value.profile_picture,
        name: user.value.name,
        email: user.value.email,
        username: user.value.username,
        accountType: accountType,
        memberSince: memberSince.toLocaleString('default', {month: 'long', year: 'numeric'}),
      },
    };
  },
  methods: {
    editProfile() {
    },
    logout() {
    },
  },
};
</script>

<style scoped>
</style>
