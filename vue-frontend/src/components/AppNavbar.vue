<template>
  <nav class="shadow-lg navbar-colors">
    <div class="flex justify-between items-center mx-auto px-4 h-20 lg:h-12 container">
      <!-- Left: Logo and Title -->
      <div class="flex items-center space-x-3">
        <router-link
            class="flex items-center space-x-3 navbar-text-hover transition duration-200"
            to="/"
        >
          <img alt="Logo" class="w-10 h-10" src="../../public/icon.png"/>
          <span class="font-bold text-xl">Slope Vision</span>
        </router-link>
      </div>

      <!-- Right: Navigation, Dark Mode, and User Menu -->
      <div class="flex items-center space-x-6">
        <!-- Navigation Links -->
        <div class="hidden md:flex space-x-6">
          <router-link
              :class="{ 'navbar-text-active': isActive('/live-webcams') }"
              class="flex items-center space-x-2 navbar-text-hover"
              to="/live-webcams"
          >
            <VideoCameraIcon class="w-5 h-5"/>
            <span>Webcams</span>
          </router-link>
          <router-link
              :class="{ 'navbar-text-active': isActive('/map') }"
              class="flex items-center space-x-2 navbar-text-hover"
              to="/map"
          >
            <MapIcon class="w-5 h-5"/>
            <span>Map</span>
          </router-link>
          <router-link
              :class="{ 'navbar-text-active': isActive('/about') }"
              class="flex items-center space-x-2 navbar-text-hover"
              to="/about"
          >
            <InformationCircleIcon class="w-5 h-5"/>
            <span>About</span>
          </router-link>
        </div>

        <!-- Dark Mode Toggle -->
        <button
            aria-label="Toggle Dark Mode"
            class="p-2 rounded navbar-button"
            @click="toggleDarkMode"
        >
          <MoonIcon v-if="darkMode" class="w-5 h-5"/>
          <SunIcon v-else class="w-5 h-5"/>
        </button>

        <!-- Data Saver Toggle -->
        <button
            aria-label="Toggle Data Saver Mode"
            class="p-2 rounded navbar-button"
            @click="toggleDataSaver"
        >
          <span v-if="dataSaver" class="font-semibold text-xs">DS</span>
          <span v-else class="font-light text-xs">DS</span>
        </button>

        <!-- User Account Menu -->
        <div class="relative">
          <button
              class="relative p-1.5 border rounded-full navbar-button"
              @click="toggleUserMenu"
          >
            <UserIcon class="w-6 h-6"/>
          </button>

          <div
              v-if="userMenuOpen"
              class="right-0 z-10 absolute shadow-lg mt-2 rounded w-40 navbar-menu"
          >
            <template v-if="isAuthenticated">
              <p class="p-2 border-b font-semibold text-gray-800 dark:text-gray-200">{{ username }}</p>
              <router-link
                  class="block px-4 py-2 navbar-menu-border rounded-tl-lg rounded-tr-lg navbar-menu-item"
                  to="/profile"
                  @click="closeUserMenu"
              >
                Profile
              </router-link>
              <button
                  class="block px-4 py-2 rounded-b-lg w-full text-danger text-left navbar-menu-item 0"
                  @click="logout"
              >
                Logout
              </button>
            </template>
            <template v-else>
              <router-link
                  class="block px-4 py-2 navbar-menu-border rounded-tl-lg rounded-tr-lg navbar-menu-item"
                  to="/login"
                  @click="closeUserMenu"
              >
                Login
              </router-link>
              <router-link
                  class="block px-4 py-2 rounded-b-lg navbar-menu-item"
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
    <div v-if="menuOpen" class="md:hidden space-y-2 px-4 py-2 navbar-menu">
      <router-link
          :class="{ 'navbar-text-active': isActive('/live-webcams') }"
          class="flex items-center space-x-2 pb-2 navbar-menu-border navbar-text-hover navbar-menu-item"
          to="/live-webcams"
          @click="closeMenu"
      >
        <VideoCameraIcon class="w-5 h-5"/>
        <span>Webcams</span>
      </router-link>
      <router-link
          :class="{ 'navbar-text-active': isActive('/map') }"
          class="flex items-center space-x-2 pb-2 navbar-menu-border navbar-text-hover navbar-menu-item"
          to="/map"
          @click="closeMenu"
      >
        <MapIcon class="w-5 h-5"/>
        <span>Map</span>
      </router-link>
      <router-link
          :class="{ 'navbar-text-active': isActive('/about') }"
          class="flex items-center space-x-2 pb-2 navbar-text-hover navbar-menu-item"
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
  MapIcon,
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
    MapIcon,
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
    const dataSaver = computed(() => store.getters['ui/dataSaver']);

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
    const toggleDataSaver = () => {
      store.dispatch('ui/toggleDataSaver');
      // If is on /live-webcams, reload the page to apply data saver mode
      if (route.path === '/live-webcams') {
        window.location.reload();
      }
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
      dataSaver,
      isAuthenticated,
      username,
      toggleMenu,
      closeMenu,
      toggleDarkMode,
      toggleDataSaver,
      toggleUserMenu,
      closeUserMenu,
      logout,
      isActive,
    };
  },
};
</script>
