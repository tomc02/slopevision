<template>
  <div class="py-8">
    <div class="container mx-auto px-4">
      <!-- Page Title -->
      <h1 class="text-3xl font-bold mb-8 text-center text-primary-light dark:text-primary-dark">
        Edit Profile
      </h1>

      <!-- Profile Edit Form -->
      <div class="w-full max-w-2xl mx-auto bg-item-light-bg dark:bg-item-dark-bg rounded-lg shadow-lg p-6">
        <form @submit.prevent="updateProfile" class="space-y-6">
          <!-- Profile Image -->
          <div class="text-center">
            <div class="w-24 h-24 rounded-full overflow-hidden mx-auto shadow-md mb-4">
              <img
                :src="profileData.image || '/default-profile.png'"
                alt="Profile Picture"
                class="object-cover w-full h-full"
              />
            </div>
            <div>
              <label
                class="cursor-pointer inline-block px-4 py-2 bg-indigo-600 text-white text-sm rounded-lg hover:bg-indigo-500 focus:ring-2 focus:ring-indigo-400"
              >
                Change Picture
                <input
                  type="file"
                  @change="handleFileUpload"
                  class="hidden"
                  accept="image/*"
                />
              </label>
            </div>
          </div>

          <!-- Name -->
          <div>
            <label for="name" class="block text-sm text-gray-600 dark:text-gray-400 mb-2">
              Full Name
            </label>
            <input
              id="name"
              v-model="profileData.name"
              type="text"
              class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:bg-item-secondary-dark dark:border-gray-600 dark:text-secondary-dark"
              placeholder="Enter your full name"
              required
            />
          </div>

          <!-- Email -->
          <div>
            <label for="email" class="block text-sm text-gray-600 dark:text-gray-400 mb-2">
              Email
            </label>
            <input
              id="email"
              v-model="profileData.email"
              type="email"
              class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:bg-item-secondary-dark dark:border-gray-600 dark:text-secondary-dark"
              placeholder="Enter your email address"
              required
              disabled
            />
          </div>

          <!-- Username -->
          <div >
            <label for="username" class="block text-sm text-gray-600 dark:text-gray-400 mb-2">
              Username
            </label>
            <input
              id="username"
              v-model="profileData.username"
              type="text"
              class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:bg-item-secondary-dark dark:border-gray-600 dark:text-secondary-dark"
              placeholder="Enter your username"
              required
              disabled
            />
          </div>

          <!-- Save Button -->
          <div class="text-center">
            <button
              type="submit"
              class="px-6 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-500 focus:ring-2 focus:ring-indigo-400"
            >
              Save Changes
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

export default {
  data() {
    const user = computed(() => store.getters['auth/currentUser'] || 'User');
    return {
      profileData: {
        image: "/path-to-profile.jpg",
        name: user.value.name,
        email: user.value.email,
        username: user.value.username,
      },
    };
  },
  methods: {
    handleFileUpload(event) {
      const file = event.target.files[0];
      if (file) {
        // Simulate a file upload and preview (replace with actual file handling)
        const reader = new FileReader();
        reader.onload = (e) => {
          this.profileData.image = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    },
    async updateProfile() {
      // Logic for saving updated profile data
      try {
        await authService.updateUser(this.profileData);
        await store.dispatch('auth/rehydrateState');
        this.$router.push('/profile');
      } catch (error) {
        console.error(error);
      }
    },
  },
};
</script>
<style scoped>
</style>
