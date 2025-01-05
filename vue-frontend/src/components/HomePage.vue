<template>
  <div class="">
    <header class="relative h-60">
      <div class="h-full flex flex-col justify-center items-center text-center">
        <h1 class="text-3xl md:text-6xl font-bold ">Welcome to Slope Vision</h1>
        <p class="mt-4 text-lg md:text-xl text-secondary-light dark:text-secondary-dark text-center">
          Discover real-time webcams, historical imagery, and plan your perfect powder day.
        </p>
      </div>
    </header>

    <main class="container mx-auto px-4 py-4">
      <!-- Features for All Users -->
      <section v-if="!isAuthenticated" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <router-link
            class="flex flex-col items-center text-center bg-item-light-bg dark:bg-item-dark-bg rounded-lg p-6 shadow-md transition-transform transform hover:scale-105"
            to="/live-webcams"
        >
          <VideoCameraIcon class="w-12 h-12 text-indigo-t mb-4"/>
          <h3 class="text-xl font-semibold mb-2">Live Webcams</h3>
          <p class="text-secondary-light dark:text-secondary-dark">
            Access live streams from mountains, ski resorts, and huts around the world.
          </p>
        </router-link>
        <router-link
            class="flex flex-col items-center text-center bg-item-light-bg dark:bg-item-dark-bg rounded-lg p-6 shadow-md transition-transform transform hover:scale-105"
            to="/live-webcams"
        >
          <ClockIcon class="w-12 h-12 text-indigo-t mb-4"/>
          <h3 class="text-xl font-semibold mb-2">Historical Images</h3>
          <p class="text-secondary-light dark:text-secondary-dark">
            Browse historical images to study snow conditions and weather trends.
          </p>
        </router-link>
        <router-link
            class="flex flex-col items-center text-center bg-item-light-bg dark:bg-item-dark-bg rounded-lg p-6 shadow-md transition-transform transform hover:scale-105"
            to="/favorites"
        >
          <HeartIcon class="w-12 h-12 text-indigo-t mb-4"/>
          <h3 class="text-xl font-semibold mb-2">Favorites</h3>
          <p class="text-secondary-light dark:text-secondary-dark">
            Keep track of your most cherished spots by saving them to your personal favorites list.
          </p>
        </router-link>
      </section>

      <!-- Call to Action for Non-Logged Users -->
      <section v-if="!isAuthenticated" class="text-center mt-16">
        <h2 class="text-3xl font-bold mb-4">Ready to Start Your Adventure?</h2>
        <p class="text-lg text-secondary-light dark:text-secondary-dark max-w-2xl mx-auto mb-6">
          Register now and join the Slope Vision community to access all the features and explore the mountains like
          never before.
        </p>
        <router-link
            class="bg-indigo-600 hover:bg-indigo-500 text-white font-semibold py-2 px-6 rounded-lg mr-4"
            to="/register"
        >
          Sign Up Now
        </router-link>
        <router-link
            class="bg-gray-400 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-100 font-semibold py-2 px-6 rounded-lg"
            to="/login"
        >
          Log In
        </router-link>
      </section>

      <!-- Personalized Content for Logged-In Users -->
      <section v-else>
        <h2 class="text-3xl font-bold mb-8 text-center">Welcome Back, {{ username }}!</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <router-link
              class="flex flex-col items-center text-center bg-item-light-bg dark:bg-item-dark-bg rounded-lg p-6 shadow-md transition-transform transform hover:scale-105"
              to="/live-webcams"
          >
            <VideoCameraIcon class="w-12 h-12 text-indigo-t mb-4"/>
            <h3 class="text-xl font-semibold mb-2">Live Webcams</h3>
            <p class="text-secondary-light dark:text-secondary-dark">
              Catch up with the latest live streams from your favorite places.
            </p>
          </router-link>
          <router-link
              class="flex flex-col items-center text-center bg-item-light-bg dark:bg-item-dark-bg rounded-lg p-6 shadow-md transition-transform transform hover:scale-105"
              to="/favorites"
          >
            <HeartIcon class="w-12 h-12 text-indigo-t mb-4"/>
            <h3 class="text-xl font-semibold mb-2">Your Favorites</h3>
            <p class="text-secondary-light dark:text-secondary-dark">
              Revisit your saved spots and see what’s happening.
            </p>
          </router-link>
          <router-link
              class="flex flex-col items-center text-center bg-item-light-bg dark:bg-item-dark-bg rounded-lg p-6 shadow-md transition-transform transform hover:scale-105"
              to="/profile"
          >
            <UserIcon class="w-12 h-12 text-indigo-t mb-4"/>
            <h3 class="text-xl font-semibold mb-2">Your Profile</h3>
            <p class="text-secondary-light dark:text-secondary-dark">
              Manage your account and preferences.
            </p>
          </router-link>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import {VideoCameraIcon, ClockIcon, HeartIcon, UserIcon,} from "@heroicons/vue/24/outline";
import store from "@/store";
import {computed} from "vue";

export default {
  components: {
    VideoCameraIcon,
    ClockIcon,
    HeartIcon,
    UserIcon,
  },
  setup() {
    const isAuthenticated = computed(() => store.getters['auth/isAuthenticated']);
    const username = computed(() => store.getters['auth/currentUser']?.username || 'User');

    return {
      isAuthenticated,
      username,
    }
  },
}

</script>

<style>
</style>
