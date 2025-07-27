<template>
  <div class="bg-gradient-to-br from-blue-50 dark:from-gray-900 via-white dark:via-gray-800 to-indigo-50 dark:to-gray-900 min-h-screen">
    <!-- Hero Section -->
    <header class="relative overflow-hidden">
      <!-- Background Elements -->
      <div class="absolute inset-0 bg-gradient-to-r from-blue-600/10 dark:from-blue-900/20 to-indigo-600/10 dark:to-indigo-900/20"></div>
      <div class="top-10 left-10 absolute bg-blue-200/30 dark:bg-blue-800/30 blur-xl rounded-full w-32 h-32"></div>
      <div class="right-10 bottom-10 absolute bg-indigo-200/30 dark:bg-indigo-800/30 blur-xl rounded-full w-24 h-24"></div>
      
      <div class="relative mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16 max-w-7xl">
        <div class="text-center">
          <!-- Logo/Icon -->
          <div class="flex justify-center mb-8">
            <div class="relative">
              <div class="flex justify-center items-center bg-gradient-to-br from-blue-500 to-indigo-600 shadow-lg rounded-2xl w-20 h-20">
                <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
              </div>
              <div class="-top-1 -right-1 absolute flex justify-center items-center bg-green-400 rounded-full w-6 h-6">
                <div class="bg-white rounded-full w-2 h-2 animate-pulse"></div>
              </div>
            </div>
          </div>

          <!-- Main Heading -->
          <h1 class="mb-6 font-bold text-gray-900 dark:text-white text-5xl md:text-7xl leading-tight">
            Welcome to
            <span class="bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600 text-transparent">
              SlopeVision
            </span>
          </h1>
          
          <!-- Subheading -->
          <p class="mx-auto mb-8 max-w-4xl text-gray-600 dark:text-gray-300 text-xl md:text-2xl leading-relaxed">
            Your ultimate companion for discovering perfect skiing conditions. Real-time webcams, historical data, 
            and intelligent insights from ski resorts worldwide.
          </p>

          <!-- Stats Bar -->
          <div class="flex flex-wrap justify-center gap-8 mb-12 text-gray-500 dark:text-gray-400 text-sm">
            <div class="flex items-center gap-2">
              <div class="bg-green-400 rounded-full w-2 h-2"></div>
              <span>10+ Resorts</span>
            </div>
            <div class="flex items-center gap-2">
              <div class="bg-blue-400 rounded-full w-2 h-2"></div>
              <span>100+ Webcams</span>
            </div>
            <div class="flex items-center gap-2">
              <div class="bg-purple-400 rounded-full w-2 h-2"></div>
              <span>4 Countries</span>
            </div>
            <div class="flex items-center gap-2">
              <div class="bg-yellow-400 rounded-full w-2 h-2 animate-pulse"></div>
              <span>Live Updates</span>
            </div>
          </div>

          <!-- CTA Buttons -->
          <div v-if="!isAuthenticated" class="flex sm:flex-row flex-col justify-center gap-4 mb-16">
            <router-link
              to="/register"
              class="inline-flex items-center bg-gradient-to-r from-blue-600 hover:from-blue-700 to-indigo-600 hover:to-indigo-700 shadow-lg hover:shadow-xl px-8 py-4 rounded-xl font-semibold text-white hover:scale-105 transition-all duration-200 transform"
            >
              Get Started Free
              <ArrowRightIcon class="ml-2 w-5 h-5" />
            </router-link>
            <router-link
              to="/about"
              class="inline-flex items-center bg-white/80 hover:bg-white dark:bg-gray-800/80 dark:hover:bg-gray-800 shadow-lg backdrop-blur-sm px-8 py-4 border border-gray-200 dark:border-gray-700 rounded-xl font-semibold text-gray-900 dark:text-white hover:scale-105 transition-all duration-200 transform"
            >
              Learn More
              <InformationCircleIcon class="ml-2 w-5 h-5" />
            </router-link>
          </div>

          <div v-else class="mb-16">
            <div class="inline-flex items-center bg-green-100 dark:bg-green-900/30 px-6 py-3 rounded-full font-medium text-green-800 dark:text-green-300 text-lg">
              <CheckCircleIcon class="mr-2 w-5 h-5" />
              Welcome back, {{ username }}!
            </div>
          </div>
        </div>
      </div>

      <!-- Floating Elements -->
      <!-- <div class="top-1/4 left-4 absolute animate-float">
        <div class="flex justify-center items-center bg-white/10 dark:bg-gray-800/30 backdrop-blur-sm rounded-2xl w-16 h-16">
          <svg class="w-8 h-8 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
      </div>
      <div class="top-1/3 right-8 absolute animate-float-delayed">
        <div class="flex justify-center items-center bg-white/10 dark:bg-gray-800/30 backdrop-blur-sm rounded-xl w-12 h-12">
          <svg class="w-6 h-6 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
        </div>
      </div> -->
    </header>

    <main class="relative">
      <!-- Features Section -->
      <section class="mx-auto px-4 sm:px-6 lg:px-8 py-20 max-w-7xl">
        <!-- Section Header -->
        <div class="mb-16 text-center">
          <h2 class="mb-6 font-bold text-gray-900 dark:text-white text-4xl md:text-5xl">
            <span v-if="!isAuthenticated">Everything You Need</span>
            <span v-else>Your Dashboard</span>
          </h2>
          <p class="mx-auto max-w-3xl text-gray-600 dark:text-gray-300 text-xl">
            <span v-if="!isAuthenticated">
              Powerful features designed to help you find the perfect skiing conditions and plan your mountain adventures.
            </span>
            <span v-else>
              Welcome back! Here's what's waiting for you today.
            </span>
          </p>
        </div>

        <!-- Features Grid -->
        <div class="gap-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
          <!-- Live Webcams -->
          <router-link
            :to="isAuthenticated ? '/live-webcams' : '/register'"
            class="group relative bg-white dark:bg-gray-800 shadow-lg hover:shadow-2xl p-8 border border-gray-100 dark:border-gray-700 rounded-2xl overflow-hidden transition-all hover:-translate-y-2 duration-300 transform"
          >
            <!-- Background Gradient -->
            <div class="absolute inset-0 bg-gradient-to-br from-blue-50 dark:from-blue-900/20 to-blue-100 dark:to-blue-800/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            
            <div class="z-10 relative">
              <!-- Icon -->
              <div class="flex justify-center items-center bg-gradient-to-br from-blue-500 to-blue-600 mb-6 rounded-xl w-16 h-16 group-hover:scale-110 transition-transform duration-300">
                <VideoCameraIcon class="w-8 h-8 text-white"/>
              </div>
              
              <!-- Content -->
              <h3 class="mb-4 font-bold text-gray-900 dark:group-hover:text-blue-400 dark:text-white group-hover:text-blue-600 text-2xl transition-colors">
                Live Webcams
              </h3>
              <p class="mb-6 text-gray-600 dark:text-gray-300 leading-relaxed">
                Access real-time streams from ski resorts, mountain peaks, and weather stations around the world.
              </p>
              
              <!-- Features List -->
              <ul class="space-y-2 text-gray-500 dark:text-gray-400 text-sm">
                <li class="flex items-center">
                  <CheckIcon class="mr-2 w-4 h-4 text-green-500" />
                  HD Quality Streams
                </li>
                <li class="flex items-center">
                  <CheckIcon class="mr-2 w-4 h-4 text-green-500" />
                  24/7 Monitoring
                </li>
                <li class="flex items-center">
                  <CheckIcon class="mr-2 w-4 h-4 text-green-500" />
                  Real-time Updates
                </li>
              </ul>
            </div>
            
            <!-- Hover Arrow -->
            <div class="right-6 bottom-6 absolute opacity-0 group-hover:opacity-100 transition-opacity duration-300">
              <ArrowRightIcon class="w-6 h-6 text-blue-500" />
            </div>
          </router-link>

          <!-- Historical Data -->
          <router-link
            :to="isAuthenticated ? '/live-webcams' : '/register'"
            class="group relative bg-white dark:bg-gray-800 shadow-lg hover:shadow-2xl p-8 border border-gray-100 dark:border-gray-700 rounded-2xl overflow-hidden transition-all hover:-translate-y-2 duration-300 transform"
          >
            <!-- Background Gradient -->
            <div class="absolute inset-0 bg-gradient-to-br from-green-50 dark:from-green-900/20 to-green-100 dark:to-green-800/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            
            <div class="z-10 relative">
              <!-- Icon -->
              <div class="flex justify-center items-center bg-gradient-to-br from-green-500 to-green-600 mb-6 rounded-xl w-16 h-16 group-hover:scale-110 transition-transform duration-300">
                <ClockIcon class="w-8 h-8 text-white"/>
              </div>
              
              <!-- Content -->
              <h3 class="mb-4 font-bold text-gray-900 dark:group-hover:text-green-400 dark:text-white group-hover:text-green-600 text-2xl transition-colors">
                Historical Data
              </h3>
              <p class="mb-6 text-gray-600 dark:text-gray-300 leading-relaxed">
                Browse archived webcam images to analyze snow patterns, weather trends, and seasonal changes.
              </p>
              
              <!-- Features List -->
              <ul class="space-y-2 text-gray-500 dark:text-gray-400 text-sm">
                <li class="flex items-center">
                  <CheckIcon class="mr-2 w-4 h-4 text-green-500" />
                  Years of Archives
                </li>
                <li class="flex items-center">
                  <CheckIcon class="mr-2 w-4 h-4 text-green-500" />
                  Weather Patterns
                </li>
                <li class="flex items-center">
                  <CheckIcon class="mr-2 w-4 h-4 text-green-500" />
                  Snow Tracking
                </li>
              </ul>
            </div>
            
            <!-- Hover Arrow -->
            <div class="right-6 bottom-6 absolute opacity-0 group-hover:opacity-100 transition-opacity duration-300">
              <ArrowRightIcon class="w-6 h-6 text-green-500" />
            </div>
          </router-link>

          <!-- Interactive Map -->
          <router-link
            :to="isAuthenticated ? '/map' : '/register'"
            class="group relative bg-white dark:bg-gray-800 shadow-lg hover:shadow-2xl p-8 border border-gray-100 dark:border-gray-700 rounded-2xl overflow-hidden transition-all hover:-translate-y-2 duration-300 transform"
          >
            <!-- Background Gradient -->
            <div class="absolute inset-0 bg-gradient-to-br from-purple-50 dark:from-purple-900/20 to-purple-100 dark:to-purple-800/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            
            <div class="z-10 relative">
              <!-- Icon -->
              <div class="flex justify-center items-center bg-gradient-to-br from-purple-500 to-purple-600 mb-6 rounded-xl w-16 h-16 group-hover:scale-110 transition-transform duration-300">
                <MapIcon class="w-8 h-8 text-white"/>
              </div>
              
              <!-- Content -->
              <h3 class="mb-4 font-bold text-gray-900 dark:group-hover:text-purple-400 dark:text-white group-hover:text-purple-600 text-2xl transition-colors">
                Interactive Map
              </h3>
              <p class="mb-6 text-gray-600 dark:text-gray-300 leading-relaxed">
                Explore our interactive map to discover webcams, ski resorts, and plan your next mountain adventure.
              </p>
              
              <!-- Features List -->
              <ul class="space-y-2 text-gray-500 dark:text-gray-400 text-sm">
                <li class="flex items-center">
                  <CheckIcon class="mr-2 w-4 h-4 text-green-500" />
                  Global Coverage
                </li>
                <li class="flex items-center">
                  <CheckIcon class="mr-2 w-4 h-4 text-green-500" />
                  Search & Filter
                </li>
                <li class="flex items-center">
                  <CheckIcon class="mr-2 w-4 h-4 text-green-500" />
                  Resort Details
                </li>
              </ul>
            </div>
            
            <!-- Hover Arrow -->
            <div class="right-6 bottom-6 absolute opacity-0 group-hover:opacity-100 transition-opacity duration-300">
              <ArrowRightIcon class="w-6 h-6 text-purple-500" />
            </div>
          </router-link>

          <!-- Conditional: Profile for authenticated users -->
          <router-link
            v-if="isAuthenticated"
            to="/profile"
            class="group relative bg-white dark:bg-gray-800 shadow-lg hover:shadow-2xl p-8 border border-gray-100 dark:border-gray-700 rounded-2xl overflow-hidden transition-all hover:-translate-y-2 duration-300 transform"
          >
            <!-- Background Gradient -->
            <div class="absolute inset-0 bg-gradient-to-br from-indigo-50 dark:from-indigo-900/20 to-indigo-100 dark:to-indigo-800/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            
            <div class="z-10 relative">
              <!-- Icon -->
              <div class="flex justify-center items-center bg-gradient-to-br from-indigo-500 to-indigo-600 mb-6 rounded-xl w-16 h-16 group-hover:scale-110 transition-transform duration-300">
                <UserIcon class="w-8 h-8 text-white"/>
              </div>
              
              <!-- Content -->
              <h3 class="mb-4 font-bold text-gray-900 dark:group-hover:text-indigo-400 dark:text-white group-hover:text-indigo-600 text-2xl transition-colors">
                Your Profile
              </h3>
              <p class="mb-6 text-gray-600 dark:text-gray-300 leading-relaxed">
                Manage your account preferences, favorite locations, and customize your SlopeVision experience.
              </p>
              
              <!-- Features List -->
              <ul class="space-y-2 text-gray-500 dark:text-gray-400 text-sm">
                <li class="flex items-center">
                  <CheckIcon class="mr-2 w-4 h-4 text-green-500" />
                  Favorite Places
                </li>
                <li class="flex items-center">
                  <CheckIcon class="mr-2 w-4 h-4 text-green-500" />
                  Preferences
                </li>
                <li class="flex items-center">
                  <CheckIcon class="mr-2 w-4 h-4 text-green-500" />
                  Account Settings
                </li>
              </ul>
            </div>
            
            <!-- Hover Arrow -->
            <div class="right-6 bottom-6 absolute opacity-0 group-hover:opacity-100 transition-opacity duration-300">
              <ArrowRightIcon class="w-6 h-6 text-indigo-500" />
            </div>
          </router-link>
        </div>
      </section>

      <!-- Call to Action Section for Non-Authenticated Users -->
      <section v-if="!isAuthenticated" class="relative bg-gradient-to-r from-blue-600 to-indigo-600 overflow-hidden">
        <!-- Background Pattern -->
        <div class="absolute inset-0 bg-black/10"></div>
        <div class="top-0 left-0 absolute w-full h-full">
          <svg class="opacity-10 w-full h-full" viewBox="0 0 100 100" fill="none">
            <defs>
              <pattern id="pattern" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
                <circle cx="10" cy="10" r="1" fill="white"/>
              </pattern>
            </defs>
            <rect width="100" height="100" fill="url(#pattern)"/>
          </svg>
        </div>
        
        <div class="relative mx-auto px-4 sm:px-6 lg:px-8 py-20 max-w-4xl text-center">
          <h2 class="mb-6 font-bold text-white text-4xl md:text-5xl">
            Ready to Start Your Adventure?
          </h2>
          <p class="mx-auto mb-10 max-w-3xl text-blue-100 text-xl leading-relaxed">
            Join thousands of skiers and snowboarders who trust SlopeVision to find the perfect conditions. 
            Create your free account and discover your next powder day.
          </p>
          
          <!-- Benefits -->
          <div class="gap-6 grid md:grid-cols-3 mb-12">
            <div class="text-center">
              <div class="flex justify-center items-center bg-white/20 mx-auto mb-4 rounded-xl w-12 h-12">
                <SparklesIcon class="w-6 h-6 text-white" />
              </div>
              <h3 class="mb-2 font-semibold text-white text-lg">Free to Start</h3>
              <p class="text-blue-100 text-sm">No credit card required</p>
            </div>
            <div class="text-center">
              <div class="flex justify-center items-center bg-white/20 mx-auto mb-4 rounded-xl w-12 h-12">
                <GlobeAltIcon class="w-6 h-6 text-white" />
              </div>
              <h3 class="mb-2 font-semibold text-white text-lg">Global Access</h3>
              <p class="text-blue-100 text-sm">Worldwide webcam coverage</p>
            </div>
            <div class="text-center">
              <div class="flex justify-center items-center bg-white/20 mx-auto mb-4 rounded-xl w-12 h-12">
                <BoltIcon class="w-6 h-6 text-white" />
              </div>
              <h3 class="mb-2 font-semibold text-white text-lg">Instant Access</h3>
              <p class="text-blue-100 text-sm">Start exploring immediately</p>
            </div>
          </div>
          
          <!-- CTA Buttons -->
          <div class="flex sm:flex-row flex-col justify-center gap-4">
            <router-link
              to="/register"
              class="inline-flex items-center bg-white hover:bg-gray-100 shadow-lg px-8 py-4 rounded-xl font-bold text-blue-600 hover:scale-105 transition-all duration-200 transform"
            >
              Create Free Account
              <ArrowRightIcon class="ml-2 w-5 h-5" />
            </router-link>
            <router-link
              to="/login"
              class="inline-flex items-center bg-blue-700/50 hover:bg-blue-700/70 backdrop-blur-sm px-8 py-4 border border-white/20 rounded-xl font-semibold text-white transition-all duration-200"
            >
              Already have an account?
            </router-link>
          </div>
        </div>
      </section>

      <!-- Welcome Back Section for Authenticated Users -->
      <section v-else class="bg-gradient-to-r from-green-50 dark:from-gray-800 to-emerald-50 dark:to-gray-900">
        <div class="mx-auto px-4 sm:px-6 lg:px-8 py-20 max-w-4xl text-center">
          <div class="mb-8">
            <div class="flex justify-center items-center bg-gradient-to-br from-green-500 to-emerald-600 mx-auto mb-6 rounded-full w-20 h-20">
              <CheckCircleIcon class="w-10 h-10 text-white" />
            </div>
            <h2 class="mb-4 font-bold text-gray-900 dark:text-white text-4xl">
              Welcome back, {{ username }}!
            </h2>
            <p class="mx-auto max-w-2xl text-gray-600 dark:text-gray-300 text-xl">
              Ready to discover perfect skiing conditions? Your dashboard is updated with the latest webcam feeds and weather data.
            </p>
          </div>
          
          <!-- Quick Actions -->
          <div class="gap-6 grid md:grid-cols-2">
            <router-link
              to="/live-webcams"
              class="group bg-white dark:bg-gray-800 shadow-lg hover:shadow-xl p-6 rounded-xl transition-all hover:-translate-y-1 duration-300 transform"
            >
              <div class="flex justify-between items-center">
                <div class="text-left">
                  <h3 class="mb-2 font-semibold text-gray-900 dark:text-white text-lg">Check Live Conditions</h3>
                  <p class="text-gray-600 dark:text-gray-300 text-sm">View current webcam feeds</p>
                </div>
                <ArrowRightIcon class="w-6 h-6 text-green-500 transition-transform group-hover:translate-x-1" />
              </div>
            </router-link>
            
            <router-link
              to="/map"
              class="group bg-white dark:bg-gray-800 shadow-lg hover:shadow-xl p-6 rounded-xl transition-all hover:-translate-y-1 duration-300 transform"
            >
              <div class="flex justify-between items-center">
                <div class="text-left">
                  <h3 class="mb-2 font-semibold text-gray-900 dark:text-white text-lg">Explore New Places</h3>
                  <p class="text-gray-600 dark:text-gray-300 text-sm">Discover webcams on the map</p>
                </div>
                <ArrowRightIcon class="w-6 h-6 text-green-500 transition-transform group-hover:translate-x-1" />
              </div>
            </router-link>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import {
  VideoCameraIcon, 
  ClockIcon, 
  MapIcon, 
  UserIcon,
  ArrowRightIcon,
  InformationCircleIcon,
  CheckCircleIcon,
  CheckIcon,
  SparklesIcon,
  GlobeAltIcon,
  BoltIcon
} from "@heroicons/vue/24/outline";
import store from "@/store";
import { computed } from "vue";

export default {
  components: {
    VideoCameraIcon,
    ClockIcon,
    MapIcon,
    UserIcon,
    ArrowRightIcon,
    InformationCircleIcon,
    CheckCircleIcon,
    CheckIcon,
    SparklesIcon,
    GlobeAltIcon,
    BoltIcon
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

<style scoped>
/* Custom animations */
@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
}

@keyframes float-delayed {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-8px);
  }
}

.animate-float {
  animation: float 3s ease-in-out infinite;
}

.animate-float-delayed {
  animation: float-delayed 4s ease-in-out infinite;
  animation-delay: 0.5s;
}

/* Custom gradient backgrounds */
.bg-app-light-bg {
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}

.dark .bg-app-dark-bg {
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
}

/* Smooth transitions for all interactive elements */
* {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

/* Custom hover effects */
.group:hover .group-hover\:translate-x-1 {
  transform: translateX(0.25rem);
}

/* Enhanced shadows */
.shadow-lg {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

.hover\:shadow-2xl:hover {
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

/* Backdrop blur for modern glass effect */
.backdrop-blur-sm {
  backdrop-filter: blur(4px);
}
</style>
