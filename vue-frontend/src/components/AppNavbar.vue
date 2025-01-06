<template>
  <nav class="navbar-colors shadow-lg">
    <div class="container mx-auto px-4 flex justify-between items-center h-20 lg:h-12">
      <!-- Left: Logo and Title -->
      <div class="flex items-center space-x-3">
        <router-link
            class="flex items-center space-x-3 navbar-text-hover transition duration-200"
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
              :class="{ 'navbar-text-active': isActive('/live-webcams') }"
              class="navbar-text-hover flex items-center space-x-2"
              to="/live-webcams"
          >
            <VideoCameraIcon class="w-5 h-5"/>
            <span>Webcams</span>
          </router-link>
          <router-link
              :class="{ 'navbar-text-active': isActive('/favorites') }"
              class="navbar-text-hover flex items-center space-x-2"
              to="/favorites"
          >
            <HeartIcon class="w-5 h-5"/>
            <span>Favorites</span>
          </router-link>
          <router-link
              :class="{ 'navbar-text-active': isActive('/about') }"
              class="navbar-text-hover flex items-center space-x-2"
              to="/about"
          >
            <InformationCircleIcon class="w-5 h-5"/>
            <span>About</span>
          </router-link>
        </div>

        <!-- Dark Mode Toggle -->
        <button
            aria-label="Toggle Dark Mode"
            class="p-2 navbar-button rounded"
            @click="toggleDarkMode"
        >
          <MoonIcon v-if="darkMode" class="w-5 h-5"/>
          <SunIcon v-else class="w-5 h-5"/>
        </button>

        <!-- User Account Menu -->
        <div class="relative">
          <button
              class="relative p-1.5 navbar-button rounded-full border"
              @click="toggleUserMenu"
          >
            <UserIcon class="w-6 h-6"/>
          </button>

          <div
              v-if="userMenuOpen"
              class="navbar-menu absolute right-0 mt-2 rounded shadow-lg w-40 z-10"
          >
            <template v-if="isAuthenticated">
              <p class="p-2 border-b text-gray-800 dark:text-gray-200 font-semibold">{{ username }}</p>
              <router-link
                  class="navbar-menu-item block px-4 py-2 rounded-tl-lg rounded-tr-lg navbar-menu-border"
                  to="/profile"
                  @click="closeUserMenu"
              >
                Profile
              </router-link>
              <button
                  class="navbar-menu-item block w-full text-left px-4 py-2 0 rounded-b-lg text-danger"
                  @click="logout"
              >
                Logout
              </button>
            </template>
            <template v-else>
              <router-link
                  class="navbar-menu-item block px-4 py-2 rounded-tl-lg rounded-tr-lg navbar-menu-border"
                  to="/login"
                  @click="closeUserMenu"
              >
                Login
              </router-link>
              <router-link
                  class="navbar-menu-item block px-4 py-2 rounded-b-lg"
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
    <div v-if="menuOpen" class="md:hidden navbar-menu py-2 px-4 space-y-2">
      <router-link
          :class="{ 'navbar-text-active': isActive('/live-webcams') }"
          class="navbar-text-hover navbar-menu-border navbar-menu-item flex items-center space-x-2 pb-2"
          to="/live-webcams"
          @click="closeMenu"
      >
        <VideoCameraIcon class="w-5 h-5"/>
        <span>Webcams</span>
      </router-link>
      <router-link
          :class="{ 'navbar-text-active': isActive('/favorites') }"
          class="navbar-text-hover navbar-menu-border navbar-menu-item flex items-center space-x-2 pb-2"
          to="/favorites"
          @click="closeMenu"
      >
        <HeartIcon class="w-5 h-5"/>
        <span>Favorites</span>
      </router-link>
      <router-link
          :class="{ 'navbar-text-active': isActive('/about') }"
          class="navbar-text-hover navbar-menu-item flex items-center space-x-2 pb-2"
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
  VideoCameraIcon,
  InformationCircleIcon,
  MoonIcon,
  SunIcon,
  UserIcon,
  XMarkIcon
} from '@heroicons/vue/24/outline';
import router from "@/router";

export default {
  name: 'AppNavbar',
  components: {
    VideoCameraIcon,
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
      if (userMenuOpen.value) {
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
      // use router to navigate to the logout view
      await router.push({ name: 'Logout' });
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
