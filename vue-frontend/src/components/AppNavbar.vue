<template>
  <nav class="bg-gray-800 text-white shadow-lg">
    <div class="container mx-auto px-4 flex justify-between items-center h-20 lg:h-12">
      <!-- Left: Logo and Title -->
      <div class="flex items-center space-x-3">
        <router-link
          class="flex items-center space-x-3 hover:text-gray-400 transition duration-200"
          to="/"
        >
          <img alt="Logo" class="h-10 w-10" src="../../public/icon.png" />
          <span class="text-xl font-bold">Slope Vision</span>
        </router-link>
      </div>

      <!-- Right: Navigation and Dark Mode -->
      <div class="flex items-center space-x-6">
        <!-- Navigation Links -->
        <div class="hidden md:flex space-x-6">
          <router-link
            :class="{ 'text-gray-400': isActive('/') }"
            class="hover:text-gray-400 transition duration-200 flex items-center space-x-2"
            to="/"
          >
            <HomeIcon class="w-5 h-5" />
            <span>Home</span>
          </router-link>
          <router-link
            :class="{ 'text-gray-400': isActive('/favorites') }"
            class="hover:text-gray-400 transition duration-200 flex items-center space-x-2"
            to="/favorites"
          >
            <HeartIcon class="w-5 h-5" />
            <span>Favorites</span>
          </router-link>
          <router-link
            :class="{ 'text-gray-400': isActive('/about') }"
            class="hover:text-gray-400 transition duration-200 flex items-center space-x-2"
            to="/about"
          >
            <InformationCircleIcon class="w-5 h-5" />
            <span>About</span>
          </router-link>
        </div>

        <!-- Dark Mode Toggle -->
        <button
          aria-label="Toggle Dark Mode"
          @click="toggleDarkMode"
          class="p-2 bg-gray-700 text-white rounded hover:bg-gray-600 transition duration-200"
        >
          <MoonIcon v-if="darkMode" class="w-5 h-5" />
          <SunIcon v-else class="w-5 h-5" />
        </button>

        <!-- Mobile Menu Button -->
        <button aria-label="Toggle Menu" class="md:hidden focus:outline-none" @click="toggleMenu">
          <Bars3Icon v-if="!menuOpen" class="w-6 h-6" />
          <XMarkIcon v-else class="w-6 h-6" />
        </button>
      </div>
    </div>

    <!-- Mobile Menu -->
    <div v-if="menuOpen" class="md:hidden bg-gray-700 text-white py-2 px-4 space-y-2">
      <router-link
        :class="{ 'text-gray-400': isActive('/') }"
        class="block hover:text-gray-400 flex items-center space-x-2"
        to="/"
        @click="closeMenu"
      >
        <HomeIcon class="w-5 h-5" />
        <span>Home</span>
      </router-link>
      <router-link
        :class="{ 'text-gray-400': isActive('/favorites') }"
        class="block hover:text-gray-400 flex items-center space-x-2"
        to="/favorites"
        @click="closeMenu"
      >
        <HeartIcon class="w-5 h-5" />
        <span>Favorites</span>
      </router-link>
      <router-link
        :class="{ 'text-gray-400': isActive('/about') }"
        class="block hover:text-gray-400 flex items-center space-x-2"
        to="/about"
        @click="closeMenu"
      >
        <InformationCircleIcon class="w-5 h-5" />
        <span>About</span>
      </router-link>
    </div>
  </nav>
</template>

<script>
import {onMounted, ref} from "vue";
import { useRoute } from "vue-router";

// Import Heroicons components
import { HomeIcon, HeartIcon, InformationCircleIcon, MoonIcon, SunIcon, Bars3Icon, XMarkIcon } from "@heroicons/vue/24/outline";

export default {
  name: "AppNavbar",
  components: {
    HomeIcon,
    HeartIcon,
    InformationCircleIcon,
    MoonIcon,
    SunIcon,
    Bars3Icon,
    XMarkIcon
  },
  setup() {
    const menuOpen = ref(false);
    const darkMode = ref(false);
    const route = useRoute();

   onMounted(() => {
      const savedMode = localStorage.getItem("darkMode");
      if (savedMode) {
        darkMode.value = JSON.parse(savedMode);
        if (darkMode.value) {
          document.documentElement.classList.add("dark");
        }
      }
    });

    const toggleMenu = () => {
      menuOpen.value = !menuOpen.value;
    };

    const closeMenu = () => {
      menuOpen.value = false;
    };

    const isActive = (path) => {
      return route.path === path;
    };

    const toggleDarkMode = () => {
      darkMode.value = !darkMode.value;
      if (darkMode.value) {
        document.documentElement.classList.add("dark");
      } else {
        document.documentElement.classList.remove("dark");
      }
      localStorage.setItem("darkMode", JSON.stringify(darkMode.value));
    };

    return {
      menuOpen,
      darkMode,
      toggleMenu,
      closeMenu,
      isActive,
      toggleDarkMode,
    };
  },
};
</script>
