<template>
  <div class="py-4">
    <div class="mx-auto px-4 max-w-4xl container">
      <!-- Back Button -->
      <div class="mb-6">
        <router-link
          to="/profile"
          class="inline-flex items-center font-medium text-indigo-600 hover:text-indigo-500 dark:hover:text-indigo-300 dark:text-indigo-400 transition-colors duration-200"
        >
          <ArrowLeftIcon class="mr-2 w-5 h-5" />
          Back to Profile
        </router-link>
      </div>

      <!-- Profile Edit Form -->
      <div class="bg-white dark:bg-gray-800 shadow-2xl border border-gray-200 dark:border-gray-700 rounded-2xl overflow-hidden">
        <form @submit.prevent="updateProfile" class="p-8">
          <!-- Profile Image Section -->
          <div class="mb-10 text-center">
            <div class="inline-block relative">
              <div class="ring-opacity-50 shadow-lg mx-auto mb-6 rounded-full ring-4 ring-indigo-500 w-32 h-32 overflow-hidden">
                <img
                  :src="profileData.image || '/default-avatar.svg'"
                  alt="Profile Picture"
                  class="w-full h-full object-cover"
                />
              </div>
            </div>
            
            <div class="space-y-3">
              <label class="inline-flex relative justify-center items-center bg-gradient-to-r from-indigo-600 hover:from-indigo-500 to-purple-600 hover:to-purple-500 shadow-lg px-6 py-3 rounded-xl font-semibold text-white hover:scale-105 transition-all duration-200 cursor-pointer transform">
                <CloudArrowUpIcon class="mr-2 w-5 h-5" />
                Upload New Picture
                <input
                  type="file"
                  @change="handleFileUpload"
                  class="absolute inset-0 opacity-0 w-full h-full cursor-pointer"
                  accept="image/*"
                />
              </label>
              <p class="text-gray-500 dark:text-gray-400 text-sm">
                JPG, PNG or GIF (max. 5MB)
              </p>
            </div>
          </div>

          <!-- Form Fields -->
          <div class="gap-8 grid md:grid-cols-2">
            <!-- Left Column -->
            <div class="space-y-6">
              <!-- Full Name -->
              <div class="group">
                <label for="name" class="block mb-3 font-semibold text-gray-700 dark:text-gray-300 text-sm">
                  <UserIcon class="inline mr-2 w-4 h-4" />
                  Full Name
                </label>
                <input
                  id="name"
                  v-model="profileData.name"
                  type="text"
                  class="bg-gray-50 dark:bg-gray-700 p-4 border-2 border-gray-200 dark:border-gray-600 focus:border-transparent rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 w-full text-primary-light dark:text-primary-dark transition-all duration-200"
                  placeholder="Enter your full name"
                  required
                />
              </div>

              <!-- Username -->
              <div class="group">
                <label for="username" class="block mb-3 font-semibold text-gray-700 dark:text-gray-300 text-sm">
                  <AtSymbolIcon class="inline mr-2 w-4 h-4" />
                  Username
                </label>
                <input
                  id="username"
                  v-model="profileData.username"
                  type="text"
                  class="bg-gray-100 dark:bg-gray-600 p-4 border-2 border-gray-200 dark:border-gray-600 rounded-xl w-full text-gray-500 dark:text-gray-400 cursor-not-allowed"
                  placeholder="Enter your username"
                  disabled
                />
                <p class="mt-2 text-gray-500 dark:text-gray-400 text-xs">
                  Username cannot be changed
                </p>
              </div>
            </div>

            <!-- Right Column -->
            <div class="space-y-6">
              <!-- Email -->
              <div class="group">
                <label for="email" class="block mb-3 font-semibold text-gray-700 dark:text-gray-300 text-sm">
                  <EnvelopeIcon class="inline mr-2 w-4 h-4" />
                  Email Address
                </label>
                <input
                  id="email"
                  v-model="profileData.email"
                  type="email"
                  class="bg-gray-100 dark:bg-gray-600 p-4 border-2 border-gray-200 dark:border-gray-600 rounded-xl w-full text-gray-500 dark:text-gray-400 cursor-not-allowed"
                  placeholder="Enter your email address"
                  disabled
                />
                <p class="mt-2 text-gray-500 dark:text-gray-400 text-xs">
                  Email cannot be changed
                </p>
              </div>


            </div>
          </div>

          <!-- Form Actions -->
          <div class="flex sm:flex-row flex-col justify-center sm:space-x-6 space-y-4 sm:space-y-0 mt-12 pt-8 border-gray-200 dark:border-gray-700 border-t">
            <router-link
              to="/profile"
              class="sm:flex-initial flex-1 bg-gray-200 hover:bg-gray-300 dark:bg-gray-600 dark:hover:bg-gray-500 px-8 py-4 rounded-xl font-semibold text-gray-700 dark:text-gray-300 text-center transition-all duration-200"
            >
              Cancel
            </router-link>
            <button
              type="submit"
              :disabled="isLoading"
              class="sm:flex-initial flex-1 bg-gradient-to-r from-indigo-600 hover:from-indigo-500 disabled:from-gray-400 to-purple-600 hover:to-purple-500 disabled:to-gray-500 shadow-lg disabled:shadow-none px-8 py-4 rounded-xl font-semibold text-white disabled:transform-none hover:scale-105 transition-all duration-200 transform"
            >
              <ArrowPathIcon v-if="isLoading" class="inline mr-2 w-5 h-5 animate-spin" />
              <span v-if="isLoading">Saving...</span>
              <span v-else>
                <CheckIcon class="inline mr-2 w-5 h-5" />
                Save Changes
              </span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from "vue";
import store from "@/store";
import authService from "@/services/authService";
import {
  ArrowLeftIcon,
  CloudArrowUpIcon,
  UserIcon,
  AtSymbolIcon,
  EnvelopeIcon,
  DocumentTextIcon,
  ArrowPathIcon,
  CheckIcon
} from '@heroicons/vue/24/outline';

export default {
  data() {
    const user = computed(() => store.getters['auth/currentUser'] || {});
    return {
      isLoading: false,
      profileData: {
        image: user.value.profile_picture,
        name: user.value.name,
        email: user.value.email,
        username: user.value.username,
      },
    };
  },
  components: {
    ArrowLeftIcon,
    CloudArrowUpIcon,
    UserIcon,
    AtSymbolIcon,
    EnvelopeIcon,
    DocumentTextIcon,
    ArrowPathIcon,
    CheckIcon
  },
  methods: {
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        // Validate file size (5MB max)
        if (file.size > 5 * 1024 * 1024) {
          alert('File size must be less than 5MB');
          return;
        }
        
        // Validate file type
        if (!file.type.startsWith('image/')) {
          alert('Please select a valid image file');
          return;
        }
        
        const reader = new FileReader();
        reader.onload = (e) => {
          this.profileData.image = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    },
    async updateProfile() {
      this.isLoading = true;
      try {
        await authService.updateUser(this.profileData);
        await store.dispatch('auth/rehydrateState');
        
        this.$router.push('/profile');
      } catch (error) {
        console.error('Update profile error:', error);
        alert('Failed to update profile. Please try again.');
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>
<style scoped>
</style>