<template>
  <nav class="bg-gray-800 dark:bg-gray-700 text-white shadow-lg">
    <div class="container mx-auto px-4 flex justify-between items-center h-20 lg:h-12">
      <!-- Left: Logo and Title -->
      <div class="flex items-center space-x-3">
        <router-link
            class="flex items-center space-x-3 hover:text-gray-400 transition duration-200"
            to="/"
        >
          <img alt="Logo" class="h-10 w-10" src="../../public/icon.png"/>
          <span class="text-xl font-bold">Slope Vision</span>
        </router-link>
      </div>

      <!-- Right: Navigation, Dark Mode, and User Menu -->
      <div class="flex items-center space-x-6">
        <!-- Navigation Links -->
        <div class="hidden md:flex space-x-6">
          <router-link
              :class="{ 'text-gray-400': isActive('/') }"
              class="hover:text-gray-400 transition duration-200 flex items-center space-x-2"
              to="/"
          >
            <HomeIcon class="w-5 h-5"/>
            <span>Home</span>
          </router-link>
          <router-link
              :class="{ 'text-gray-400': isActive('/favorites') }"
              class="hover:text-gray-400 transition duration-200 flex items-center space-x-2"
              to="/favorites"
          >
            <HeartIcon class="w-5 h-5"/>
            <span>Favorites</span>
          </router-link>
          <router-link
              :class="{ 'text-gray-400': isActive('/about') }"
              class="hover:text-gray-400 transition duration-200 flex items-center space-x-2"
              to="/about"
          >
            <InformationCircleIcon class="w-5 h-5"/>
            <span>About</span>
          </router-link>
        </div>

        <!-- Dark Mode Toggle -->
        <button
            aria-label="Toggle Dark Mode"
            class="p-2 bg-gray-700 dark:bg-gray-600 text-white rounded hover:bg-gray-600 dark:hover:bg-gray-500 transition duration-200"
            @click="toggleDarkMode"
        >
          <MoonIcon v-if="darkMode" class="w-5 h-5"/>
          <SunIcon v-else class="w-5 h-5"/>
        </button>

        <!-- User Account Menu -->
        <div class="relative">
          <button
              class="relative p-2 bg-gray-700 dark:bg-gray-600 text-white rounded-full hover:bg-gray-600 dark:hover:bg-gray-500 transition duration-200"
              @click="toggleUserMenu"
          >
            <UserIcon class="w-6 h-6"/>
          </button>

          <div
              v-if="userMenuOpen"
              class="absolute right-0 mt-2 bg-white dark:bg-gray-700 text-black dark:text-white rounded shadow-lg w-40"
          >
            <template v-if="isAuthenticated">
              <p class="p-2 border-b text-gray-800 dark:text-gray-200 font-semibold">{{ username }}</p>
              <router-link
                  class="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600"
                  to="/profile"
                  @click="closeUserMenu"
              >
                Profile
              </router-link>
              <button
                  class="block w-full text-left px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600"
                  @click="logout"
              >
                Logout
              </button>
            </template>
            <template v-else>
              <router-link
                  class="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600"
                  to="/login"
                  @click="closeUserMenu"
              >
                Login
              </router-link>
              <router-link
                  class="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600"
                  to="/register"
                  @click="closeUserMenu"
              >
                Register
              </router-link>
            </template>
          </div>
        </div>

        <!-- Mobile Menu Button -->
        <button aria-label="Toggle Menu" class="md:hidden focus:outline-none" @click="toggleMenu">
          <Bars3Icon v-if="!menuOpen" class="w-6 h-6"/>
          <XMarkIcon v-else class="w-6 h-6"/>
        </button>
      </div>
    </div>

    <!-- Mobile Menu -->
    <div v-if="menuOpen" class="md:hidden bg-gray-700 dark:bg-gray-600 text-white py-2 px-4 space-y-2">
      <router-link
          :class="{ 'text-gray-400': isActive('/') }"
          class="block hover:text-gray-400 flex items-center space-x-2"
          to="/"
          @click="closeMenu"
      >
        <HomeIcon class="w-5 h-5"/>
        <span>Home</span>
      </router-link>
      <router-link
          :class="{ 'text-gray-400': isActive('/favorites') }"
          class="block hover:text-gray-400 flex items-center space-x-2"
          to="/favorites"
          @click="closeMenu"
      >
        <HeartIcon class="w-5 h-5"/>
        <span>Favorites</span>
      </router-link>
      <router-link
          :class="{ 'text-gray-400': isActive('/about') }"
          class="block hover:text-gray-400 flex items-center space-x-2"
          to="/about"
          @click="closeMenu"
      >
        <InformationCircleIcon class="w-5 h-5"/>
        <span>About</span>
      </router-link>
    </div>
  </nav>
</template>


<script>
import {computed, onMounted, onUnmounted, ref} from 'vue';
import {useRoute} from 'vue-router';
import {useStore} from 'vuex';
import {
  Bars3Icon,
  HeartIcon,
  HomeIcon,
  InformationCircleIcon,
  MoonIcon,
  SunIcon,
  UserIcon,
  XMarkIcon
} from '@heroicons/vue/24/outline';

export default {
  name: 'AppNavbar',
  components: {
    HomeIcon,
    HeartIcon,
    InformationCircleIcon,
    MoonIcon,
    SunIcon,
    Bars3Icon,
    XMarkIcon,
    UserIcon,
  },
  setup() {
    const store = useStore();
    const route = useRoute();
    const menuOpen = ref(false);
    const darkMode = ref(false);
    const userMenuOpen = ref(false);

    onMounted(() => {
      const savedMode = localStorage.getItem("darkMode");
      if (savedMode) {
        darkMode.value = JSON.parse(savedMode);
        if (darkMode.value) {
          document.documentElement.classList.add("dark");
        }
      }

      document.addEventListener('click', handleOutsideClick);
    });

    onUnmounted(() => {
      document.removeEventListener('click', handleOutsideClick);
    });

    const handleOutsideClick = (event) => {
      if(userMenuOpen.value){
        if (!event.target.closest('.relative')) {
          userMenuOpen.value = false;
        }
      }
    };

    const isAuthenticated = computed(() => store.getters['auth/isAuthenticated']);
    const username = computed(() => store.getters['auth/currentUser']?.username || 'User');

    const toggleMenu = () => (menuOpen.value = !menuOpen.value);
    const closeMenu = () => (menuOpen.value = false);
    const toggleDarkMode = () => {
      darkMode.value = !darkMode.value;
      document.documentElement.classList.toggle('dark', darkMode.value);
      localStorage.setItem('darkMode', JSON.stringify(darkMode.value));
    };
    const toggleUserMenu = () => (userMenuOpen.value = !userMenuOpen.value);
    const closeUserMenu = () => (userMenuOpen.value = false);

    const logout = async () => {
      await store.dispatch('auth/logout');
      closeUserMenu();
    };

    const isActive = (path) => route.path === path;

    return {
      menuOpen,
      darkMode,
      userMenuOpen,
      isAuthenticated,
      username,
      toggleMenu,
      closeMenu,
      toggleDarkMode,
      toggleUserMenu,
      closeUserMenu,
      logout,
      isActive,
    };
  },
};
</script>
