<template>
  <div class="">
    <header class="relative h-60">
      <div class="flex flex-col justify-center items-center h-full text-center">
        <h1 class="font-bold text-3xl md:text-6xl">Welcome to Slope Vision</h1>
        <p class="mt-4 text-secondary-light dark:text-secondary-dark text-lg md:text-xl text-center">
          Discover real-time webcams, historical imagery, and plan your perfect powder day.
        </p>
      </div>
    </header>

    <main class="mx-auto px-4 py-4 container">
      <!-- Features for All Users -->
      <section v-if="!isAuthenticated" class="gap-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
        <router-link
            class="flex flex-col items-center bg-item-light-bg dark:bg-item-dark-bg shadow-md p-6 rounded-lg text-center hover:scale-105 transition-transform transform"
            to="/live-webcams"
        >
          <VideoCameraIcon class="mb-4 w-12 h-12 text-indigo-t"/>
          <h3 class="mb-2 font-semibold text-xl">Live Webcams</h3>
          <p class="text-secondary-light dark:text-secondary-dark">
            Access live streams from mountains, ski resorts, and huts around the world.
          </p>
        </router-link>
        <router-link
            class="flex flex-col items-center bg-item-light-bg dark:bg-item-dark-bg shadow-md p-6 rounded-lg text-center hover:scale-105 transition-transform transform"
            to="/live-webcams"
        >
          <ClockIcon class="mb-4 w-12 h-12 text-indigo-t"/>
          <h3 class="mb-2 font-semibold text-xl">Historical Images</h3>
          <p class="text-secondary-light dark:text-secondary-dark">
            Browse historical images to study snow conditions and weather trends.
          </p>
        </router-link>
        <router-link
            class="flex flex-col items-center bg-item-light-bg dark:bg-item-dark-bg shadow-md p-6 rounded-lg text-center hover:scale-105 transition-transform transform"
            to="/map"
        >
          <MapIcon class="mb-4 w-12 h-12 text-indigo-t"/>
          <h3 class="mb-2 font-semibold text-xl">Map</h3>
          <p class="text-secondary-light dark:text-secondary-dark">
            Explore our interactive map to find webcams, ski resorts, and more.
          </p>
        </router-link>
      </section>

      <!-- Call to Action for Non-Logged Users -->
      <section v-if="!isAuthenticated" class="mt-16 text-center">
        <h2 class="mb-4 font-bold text-3xl">Ready to Start Your Adventure?</h2>
        <p class="mx-auto mb-6 max-w-2xl text-secondary-light dark:text-secondary-dark text-lg">
          Register now and join the Slope Vision community to access all the features and explore the mountains like
          never before.
        </p>
        <router-link
            class="bg-indigo-600 hover:bg-indigo-500 mr-4 px-6 py-2 rounded-lg font-semibold text-white"
            to="/register"
        >
          Sign Up Now
        </router-link>
        <router-link
            class="bg-gray-400 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 px-6 py-2 rounded-lg font-semibold text-gray-800 dark:text-gray-100"
            to="/login"
        >
          Log In
        </router-link>
      </section>

      <!-- Personalized Content for Logged-In Users -->
      <section v-else>
        <h2 class="mb-8 font-bold text-3xl text-center">Welcome Back, {{ username }}!</h2>
        <div class="gap-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
          <router-link
              class="flex flex-col items-center bg-item-light-bg dark:bg-item-dark-bg shadow-md p-6 rounded-lg text-center hover:scale-105 transition-transform transform"
              to="/live-webcams"
          >
            <VideoCameraIcon class="mb-4 w-12 h-12 text-indigo-t"/>
            <h3 class="mb-2 font-semibold text-xl">Live Webcams</h3>
            <p class="text-secondary-light dark:text-secondary-dark">
              Catch up with the latest live streams from your favorite places.
            </p>
          </router-link>
          <router-link
              class="flex flex-col items-center bg-item-light-bg dark:bg-item-dark-bg shadow-md p-6 rounded-lg text-center hover:scale-105 transition-transform transform"
              to="/map"
          >
            <MapIcon class="mb-4 w-12 h-12 text-indigo-t"/>
            <h3 class="mb-2 font-semibold text-xl">Map</h3>
            <p class="text-secondary-light dark:text-secondary-dark">
              Explore the map to find new webcams and plan your next trip.
            </p>
          </router-link>
          <router-link
              class="flex flex-col items-center bg-item-light-bg dark:bg-item-dark-bg shadow-md p-6 rounded-lg text-center hover:scale-105 transition-transform transform"
              to="/profile"
          >
            <UserIcon class="mb-4 w-12 h-12 text-indigo-t"/>
            <h3 class="mb-2 font-semibold text-xl">Your Profile</h3>
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
import {VideoCameraIcon, ClockIcon, MapIcon, UserIcon,} from "@heroicons/vue/24/outline";
import store from "@/store";
import {computed} from "vue";

export default {
  components: {
    VideoCameraIcon,
    ClockIcon,
    MapIcon,
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
