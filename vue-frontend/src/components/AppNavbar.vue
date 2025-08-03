<template>
  <nav class="top-0 z-50 sticky bg-white/95 dark:bg-gray-900/95 backdrop-blur-md border-gray-200 dark:border-gray-800 border-b">
    <div class="mx-auto px-4 sm:px-6 lg:px-8 max-w-7xl">
      <div class="flex justify-between items-center h-16">
        <!-- Left: Logo and Title -->
        <div class="flex items-center">
          <router-link class="group flex items-center space-x-3" to="/">
            <!-- Logo with modern styling -->
            <div class="relative">
              <div class="flex justify-center items-center bg-gradient-to-br from-indigo-500 to-purple-600 shadow-lg rounded-xl w-10 h-10 group-hover:scale-105 transition-transform duration-200">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
              </div>
              <!-- Live indicator -->
              <div class="-top-1 -right-1 absolute bg-green-500 rounded-full w-3 h-3 animate-pulse"></div>
            </div>
            <span class="bg-clip-text bg-gradient-to-r from-gray-900 dark:from-white to-gray-700 dark:to-gray-300 font-bold text-transparent text-xl">
              SlopeVision
            </span>
          </router-link>
        </div>

        <!-- Center: Navigation Links (Desktop) -->
        <div class="hidden md:flex items-center space-x-1">
          <router-link
            :class="{ 
              'text-indigo-600 dark:text-indigo-400 bg-indigo-50 dark:bg-indigo-900/30': isActive('/live-webcams'),
              'text-gray-700 dark:text-gray-300 hover:text-indigo-600 dark:hover:text-indigo-400 hover:bg-gray-50 dark:hover:bg-gray-800/50': !isActive('/live-webcams')
            }"
            class="flex items-center space-x-2 px-4 py-2 rounded-xl font-medium transition-all duration-200"
            to="/live-webcams"
          >
            <VideoCameraIcon class="w-5 h-5" />
            <span>Webcams</span>
          </router-link>
          
          <router-link
            :class="{ 
              'text-indigo-600 dark:text-indigo-400 bg-indigo-50 dark:bg-indigo-900/30': isActive('/map'),
              'text-gray-700 dark:text-gray-300 hover:text-indigo-600 dark:hover:text-indigo-400 hover:bg-gray-50 dark:hover:bg-gray-800/50': !isActive('/map')
            }"
            class="flex items-center space-x-2 px-4 py-2 rounded-xl font-medium transition-all duration-200"
            to="/map"
          >
            <MapIcon class="w-5 h-5" />
            <span>Map</span>
          </router-link>
          
          <router-link
            :class="{ 
              'text-indigo-600 dark:text-indigo-400 bg-indigo-50 dark:bg-indigo-900/30': isActive('/about'),
              'text-gray-700 dark:text-gray-300 hover:text-indigo-600 dark:hover:text-indigo-400 hover:bg-gray-50 dark:hover:bg-gray-800/50': !isActive('/about')
            }"
            class="flex items-center space-x-2 px-4 py-2 rounded-xl font-medium transition-all duration-200"
            to="/about"
          >
            <InformationCircleIcon class="w-5 h-5" />
            <span>About</span>
          </router-link>
        </div>

        <!-- Right: Controls and User Menu -->
        <div class="flex items-center space-x-3">
          <!-- Dark Mode Toggle -->
          <button 
            aria-label="Toggle Dark Mode" 
            class="hover:bg-gray-100 dark:hover:bg-gray-800 p-2 rounded-xl text-gray-600 hover:text-gray-900 dark:hover:text-gray-100 dark:text-gray-400 transition-all duration-200"
            @click="toggleDarkMode"
          >
            <MoonIcon v-if="darkMode" class="w-5 h-5" />
            <SunIcon v-else class="w-5 h-5" />
          </button>

          <!-- Data Saver Toggle -->
          <div class="group relative">
            <button 
              aria-label="Toggle Data Saver Mode" 
              :class="{
                'text-orange-600 dark:text-orange-400 bg-orange-50 dark:bg-orange-900/30': dataSaver,
                'text-gray-600 dark:text-gray-400 hover:text-orange-600 dark:hover:text-orange-400 hover:bg-gray-100 dark:hover:bg-gray-800': !dataSaver
              }"
              class="flex justify-center items-center p-2 rounded-xl min-w-[2.5rem] font-bold text-sm transition-all duration-200"
              @click="toggleDataSaver"
            >
              DS
            </button>
            
            <!-- Tooltip -->
            <div class="top-12 left-1/2 absolute bg-gray-900 dark:bg-gray-700 opacity-0 group-hover:opacity-100 mb-2 px-3 py-2 rounded-lg text-white text-xs whitespace-nowrap transition-opacity -translate-x-1/2 duration-200 pointer-events-none transform">
              {{ dataSaver ? 'Disable' : 'Enable' }} Data Saver
              <div class="bottom-full left-1/2 absolute border-t-4 border-t-gray-900 border-transparent dark:border-t-gray-700 border-r-4 border-l-4 w-0 h-0 rotate-180 -translate-x-1/2 transform"></div>
            </div>
          </div>

          <!-- User Menu -->
          <div class="relative">
            <button 
              class="flex items-center hover:bg-gray-100 dark:hover:bg-gray-800 p-2 rounded-xl text-gray-600 hover:text-gray-900 dark:hover:text-gray-100 dark:text-gray-400 transition-all duration-200"
              @click="toggleUserMenu"
            >
              <UserIcon class="w-5 h-5" />
            </button>

            <!-- User Dropdown -->
            <transition
              enter-active-class="transition ease-out duration-100"
              enter-from-class="transform opacity-0 scale-95"
              enter-to-class="transform opacity-100 scale-100"
              leave-active-class="transition ease-in duration-75"
              leave-from-class="transform opacity-100 scale-100"
              leave-to-class="transform opacity-0 scale-95"
            >
              <div 
                v-if="userMenuOpen" 
                class="right-0 z-50 absolute bg-white dark:bg-gray-800 shadow-xl mt-2 py-2 border border-gray-200 dark:border-gray-700 rounded-2xl w-48"
              >
                <template v-if="isAuthenticated">
                  <div class="px-4 py-3 border-gray-200 dark:border-gray-700 border-b">
                    <p class="font-medium text-gray-900 dark:text-white text-sm">{{ username }}</p>
                    <p class="text-gray-500 dark:text-gray-400 text-xs">Signed in</p>
                  </div>
                  <router-link 
                    class="flex items-center hover:bg-gray-50 dark:hover:bg-gray-700 px-4 py-3 text-gray-700 hover:text-gray-900 dark:hover:text-white dark:text-gray-300 text-sm transition-colors duration-200"
                    to="/profile" 
                    @click="closeUserMenu"
                  >
                    <UserIcon class="mr-3 w-4 h-4" />
                    Profile Settings
                  </router-link>
                  <button 
                    class="flex items-center hover:bg-red-50 dark:hover:bg-red-900/20 px-4 py-3 w-full text-red-600 dark:text-red-400 text-sm transition-colors duration-200"
                    @click="logout"
                  >
                    <svg class="mr-3 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                    </svg>
                    Sign Out
                  </button>
                </template>
                <template v-else>
                  <router-link 
                    class="flex items-center hover:bg-gray-50 dark:hover:bg-gray-700 px-4 py-3 text-gray-700 hover:text-gray-900 dark:hover:text-white dark:text-gray-300 text-sm transition-colors duration-200"
                    to="/login" 
                    @click="closeUserMenu"
                  >
                    <svg class="mr-3 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                    </svg>
                    Sign In
                  </router-link>
                  <router-link 
                    class="flex items-center hover:bg-gray-50 dark:hover:bg-gray-700 px-4 py-3 text-gray-700 hover:text-gray-900 dark:hover:text-white dark:text-gray-300 text-sm transition-colors duration-200"
                    to="/register" 
                    @click="closeUserMenu"
                  >
                    <svg class="mr-3 w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                    </svg>
                    Create Account
                  </router-link>
                </template>
              </div>
            </transition>
          </div>

          <!-- Mobile Menu Button -->
          <button 
            aria-label="Toggle Menu" 
            class="md:hidden hover:bg-gray-100 dark:hover:bg-gray-800 p-2 rounded-xl text-gray-600 hover:text-gray-900 dark:hover:text-gray-100 dark:text-gray-400 transition-all duration-200"
            @click="toggleMenu"
          >
            <Bars3Icon v-if="!menuOpen" class="w-6 h-6" />
            <XMarkIcon v-else class="w-6 h-6" />
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile Menu -->
    <transition
      enter-active-class="transition ease-out duration-100"
      enter-from-class="transform opacity-0 scale-95"
      enter-to-class="transform opacity-100 scale-100"
      leave-active-class="transition ease-in duration-75"
      leave-from-class="transform opacity-100 scale-100"
      leave-to-class="transform opacity-0 scale-95"
    >
      <div v-if="menuOpen" class="md:hidden bg-white/95 dark:bg-gray-900/95 backdrop-blur-md border-gray-200 dark:border-gray-800 border-t">
        <div class="space-y-2 px-4 py-4">
          <router-link
            :class="{ 
              'text-indigo-600 dark:text-indigo-400 bg-indigo-50 dark:bg-indigo-900/30': isActive('/live-webcams'),
              'text-gray-700 dark:text-gray-300': !isActive('/live-webcams')
            }"
            class="flex items-center space-x-3 px-4 py-3 rounded-xl font-medium transition-all duration-200"
            to="/live-webcams" 
            @click="closeMenu"
          >
            <VideoCameraIcon class="w-5 h-5" />
            <span>Webcams</span>
          </router-link>
          
          <router-link
            :class="{ 
              'text-indigo-600 dark:text-indigo-400 bg-indigo-50 dark:bg-indigo-900/30': isActive('/map'),
              'text-gray-700 dark:text-gray-300': !isActive('/map')
            }"
            class="flex items-center space-x-3 px-4 py-3 rounded-xl font-medium transition-all duration-200"
            to="/map" 
            @click="closeMenu"
          >
            <MapIcon class="w-5 h-5" />
            <span>Map</span>
          </router-link>
          
          <router-link
            :class="{ 
              'text-indigo-600 dark:text-indigo-400 bg-indigo-50 dark:bg-indigo-900/30': isActive('/about'),
              'text-gray-700 dark:text-gray-300': !isActive('/about')
            }"
            class="flex items-center space-x-3 px-4 py-3 rounded-xl font-medium transition-all duration-200"
            to="/about" 
            @click="closeMenu"
          >
            <InformationCircleIcon class="w-5 h-5" />
            <span>About</span>
          </router-link>
        </div>
      </div>
    </transition>
  </nav>
</template>


<script>
import { computed, onMounted, onUnmounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { useStore } from 'vuex';
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
