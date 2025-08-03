<template>
  <div class="bg-white dark:bg-gray-900 min-h-screen">
    <!-- Floating Snow Animation -->
    <div class="snowflakes" aria-hidden="true">
      <div class="dark:text-white snowflake">❅</div>
      <div class="dark:text-white snowflake">❆</div>
      <div class="dark:text-white snowflake">❅</div>
      <div class="dark:text-white snowflake">❆</div>
      <div class="dark:text-white snowflake">❅</div>
      <div class="dark:text-white snowflake">❆</div>
      <div class="dark:text-white snowflake">❅</div>
      <div class="dark:text-white snowflake">❆</div>
      <div class="dark:text-white snowflake">❅</div>
      <div class="dark:text-white snowflake">❆</div>
      
    </div>

    <!-- Hero Section -->
    <section class="relative bg-gradient-to-br from-blue-50 dark:from-gray-900 via-white dark:via-gray-800 to-indigo-50 dark:to-gray-900 overflow-hidden">
      <div class="absolute inset-0 bg-white/50 dark:bg-gray-900/50"></div>
      <div class="relative mx-auto px-4 sm:px-6 lg:px-8 py-32 max-w-7xl">
        <div class="space-y-8 text-center">
          <div
            class="inline-flex items-center bg-blue-100 dark:bg-blue-900/50 mb-4 px-4 py-2 rounded-full font-medium text-blue-600 dark:text-blue-300 text-sm">
            <StarIcon class="mr-2 w-4 h-4" />
            Trusted by 50,000+ winter sports enthusiasts
          </div>
          <h1 class="font-extrabold text-gray-900 dark:text-white text-5xl md:text-7xl tracking-tight">
            <span class="block mb-2">About</span>
            <span class="relative">
              <span
                class="z-10 relative bg-clip-text bg-gradient-to-r from-blue-500 to-indigo-500 text-transparent">SlopeVision</span>
              <span
                class="absolute inset-0 bg-clip-text bg-gradient-to-r from-blue-500 to-indigo-500 opacity-70 blur-md text-transparent"></span>
            </span>
          </h1>
          <p class="mx-auto max-w-3xl text-gray-600 dark:text-gray-300 text-xl md:text-2xl leading-relaxed">
            Your ultimate companion for discovering the perfect skiing conditions. We bring together webcams from ski
            resorts worldwide,
            so you never miss the perfect powder day.
          </p>
          <div class="flex justify-center gap-4 pt-4">
            <button
              class="inline-flex items-center bg-gradient-to-r from-blue-500 to-indigo-500 hover:shadow-lg px-6 py-3 rounded-lg font-medium text-white transition-all hover:-translate-y-0.5 duration-300 transform"
              @click="$router.push('/live-webcams')">
              Explore Webcams
              <ArrowRightIcon class="ml-2 w-4 h-4" />
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Mission Section -->
    <section class="bg-gray-50 dark:bg-gray-800 py-24">
      <div class="mx-auto px-4 sm:px-6 lg:px-8 max-w-7xl">
        <div class="items-center gap-16 grid lg:grid-cols-2">
          <div class="space-y-8">
            <div
              class="inline-block bg-blue-100 dark:bg-blue-900/30 px-4 py-2 rounded-full font-medium text-blue-600 dark:text-blue-300 text-sm">
              Our Mission
            </div>
            <h2 class="font-bold text-gray-900 dark:text-white text-4xl">
              Empowering your winter adventures with real-time mountain intelligence
            </h2>
            <div class="space-y-6 text-gray-600 dark:text-gray-300 text-lg">
              <p>
                At SlopeVision, we believe that every skier and snowboarder deserves access to real-time, accurate
                information about mountain conditions. No more guessing games, no more disappointments on the slopes.
              </p>
              <p>
                We've built the most comprehensive webcam aggregation platform that brings together feeds from hundreds
                of ski resorts worldwide, giving you the power to make informed decisions about your next adventure.
              </p>
              <p>
                Whether you're planning a weekend getaway or tracking conditions at your home mountain, SlopeVision
                puts the information you need right at your fingertips.
              </p>
            </div>
          </div>
          <div class="relative">
            <div class="relative shadow-2xl rounded-3xl aspect-video overflow-hidden">
              <div
                class="absolute inset-0 flex justify-center items-center bg-gradient-to-br from-blue-500 to-indigo-600">
                <div class="p-8 text-white text-center">
                  <div
                    class="inline-flex justify-center items-center bg-white/20 backdrop-blur-sm mb-6 rounded-full w-24 h-24">
                    <VideoCameraIcon class="w-12 h-12" />
                  </div>
                  <h3 class="font-bold text-2xl">Live Mountain Views</h3>
                  <p class="opacity-90 mt-2">Real-time conditions from resorts worldwide</p>
                </div>
              </div>
            </div>
            <div
              class="-bottom-6 -left-6 absolute bg-blue-400 opacity-20 dark:opacity-30 blur-xl rounded-full w-32 h-32 mix-blend-multiply filter">
            </div>
            <div
              class="-top-6 -right-6 absolute bg-indigo-400 opacity-20 dark:opacity-30 blur-xl rounded-full w-32 h-32 mix-blend-multiply filter">
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Grid -->
    <section class="bg-white dark:bg-gray-900 py-24">
      <div class="mx-auto px-4 sm:px-6 lg:px-8 max-w-7xl">
        <div class="mb-16 text-center">
          <div
            class="inline-block bg-blue-100 dark:bg-blue-900/30 mb-4 px-4 py-2 rounded-full font-medium text-blue-600 dark:text-blue-300 text-sm">
            Why Choose Us
          </div>
          <h2 class="mb-4 font-bold text-gray-900 dark:text-white text-4xl">
            Everything you need for the perfect ski day
          </h2>
          <p class="mx-auto max-w-3xl text-gray-600 dark:text-gray-300 text-xl">
            We've packed powerful features into an intuitive platform that makes checking snow conditions effortless.
          </p>
        </div>

        <div class="gap-8 grid md:grid-cols-2 lg:grid-cols-3">
          <!-- Feature 1 -->
          <div
            class="bg-gray-50 dark:bg-gray-800 shadow-lg hover:shadow-xl p-8 rounded-2xl transition-all hover:-translate-y-2 duration-300 transform">
            <div class="flex justify-center items-center bg-blue-100 dark:bg-blue-900/30 mb-6 rounded-xl w-14 h-14">
              <GlobeAltIcon class="w-7 h-7 text-blue-600 dark:text-blue-400" />
            </div>
            <h3 class="mb-4 font-bold text-gray-900 dark:text-white text-xl">Global Coverage</h3>
            <p class="text-gray-600 dark:text-gray-300">
              Access webcams from ski resorts across the globe. From the Alps to the Rockies, we've got you covered.
            </p>
          </div>

          <!-- Feature 2 -->
          <div
            class="bg-gray-50 dark:bg-gray-800 shadow-lg hover:shadow-xl p-8 rounded-2xl transition-all hover:-translate-y-2 duration-300 transform">
            <div class="flex justify-center items-center bg-green-100 dark:bg-green-900/30 mb-6 rounded-xl w-14 h-14">
              <ClockIcon class="w-7 h-7 text-green-600 dark:text-green-400" />
            </div>
            <h3 class="mb-4 font-bold text-gray-900 dark:text-white text-xl">Real-Time Updates</h3>
            <p class="text-gray-600 dark:text-gray-300">
              Our automated system continuously monitors and updates webcam feeds to ensure you get the latest
              conditions.
            </p>
          </div>

          <!-- Feature 3 -->
          <div
            class="bg-gray-50 dark:bg-gray-800 shadow-lg hover:shadow-xl p-8 rounded-2xl transition-all hover:-translate-y-2 duration-300 transform">
            <div class="flex justify-center items-center bg-purple-100 dark:bg-purple-900/30 mb-6 rounded-xl w-14 h-14">
              <ChartBarIcon class="w-7 h-7 text-purple-600 dark:text-purple-400" />
            </div>
            <h3 class="mb-4 font-bold text-gray-900 dark:text-white text-xl">Historical Data</h3>
            <p class="text-gray-600 dark:text-gray-300">
              Track snow conditions over time with our comprehensive historical webcam archives and trend analysis.
            </p>
          </div>

          <!-- Feature 4 -->
          <div
            class="bg-gray-50 dark:bg-gray-800 shadow-lg hover:shadow-xl p-8 rounded-2xl transition-all hover:-translate-y-2 duration-300 transform">
            <div class="flex justify-center items-center bg-red-100 dark:bg-red-900/30 mb-6 rounded-xl w-14 h-14">
              <MapPinIcon class="w-7 h-7 text-red-600 dark:text-red-400" />
            </div>
            <h3 class="mb-4 font-bold text-gray-900 dark:text-white text-xl">Interactive Maps</h3>
            <p class="text-gray-600 dark:text-gray-300">
              Discover new ski destinations with our interactive map interface. Find hidden gems and plan your next
              adventure.
            </p>
          </div>

          <!-- Feature 5 -->
          <div
            class="bg-gray-50 dark:bg-gray-800 shadow-lg hover:shadow-xl p-8 rounded-2xl transition-all hover:-translate-y-2 duration-300 transform">
            <div class="flex justify-center items-center bg-indigo-100 dark:bg-indigo-900/30 mb-6 rounded-xl w-14 h-14">
              <UserIcon class="w-7 h-7 text-indigo-600 dark:text-indigo-400" />
            </div>
            <h3 class="mb-4 font-bold text-gray-900 dark:text-white text-xl">Personal Dashboard</h3>
            <p class="text-gray-600 dark:text-gray-300">
              Create your account to save favorite resorts, track your preferred locations, and customize your
              experience.
            </p>
          </div>

          <!-- Feature 6 -->
          <div
            class="bg-gray-50 dark:bg-gray-800 shadow-lg hover:shadow-xl p-8 rounded-2xl transition-all hover:-translate-y-2 duration-300 transform">
            <div class="flex justify-center items-center bg-orange-100 dark:bg-orange-900/30 mb-6 rounded-xl w-14 h-14">
              <SignalIcon class="w-7 h-7 text-orange-600 dark:text-orange-400" />
            </div>
            <h3 class="mb-4 font-bold text-gray-900 dark:text-white text-xl">Data Saver Mode</h3>
            <p class="text-gray-600 dark:text-gray-300">
              Optimize your data usage with our intelligent Data Saver mode. Perfect for mobile users and areas with
              limited bandwidth.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Team Section -->
    <section class="bg-gray-50 dark:bg-gray-800 py-24">
      <div class="mx-auto px-4 sm:px-6 lg:px-8 max-w-7xl">
        <div class="mb-16 text-center">
          <div
            class="inline-block bg-blue-100 dark:bg-blue-900/30 mb-4 px-4 py-2 rounded-full font-medium text-blue-600 dark:text-blue-300 text-sm">
            Our Team
          </div>
          <h2 class="mb-4 font-bold text-gray-900 dark:text-white text-4xl">
            Made by Ski Enthusiasts
          </h2>
          <p class="mx-auto max-w-3xl text-gray-600 dark:text-gray-300 text-xl">
            SlopeVision was born from a passion for skiing and the frustration of not knowing current mountain
            conditions.
            We're a team of developers and snow sports enthusiasts who understand what you need.
          </p>
        </div>

        <div class="bg-white dark:bg-gray-900 shadow-2xl rounded-3xl overflow-hidden">
          <div class="grid md:grid-cols-2">
            <div class="p-12">
              <h3 class="mb-6 font-bold text-gray-900 dark:text-white text-2xl">Our Story</h3>
              <div class="space-y-4 text-gray-600 dark:text-gray-300">
                <p>
                  It started with a simple problem: planning the perfect ski day. We found ourselves constantly
                  jumping between different resort websites, trying to piece together current conditions from
                  scattered webcam feeds.
                </p>
                <p>
                  We knew there had to be a better way. So we built SlopeVision – a centralized platform that
                  aggregates webcam feeds from ski resorts worldwide, complete with historical data and intelligent
                  insights.
                </p>
                <p>
                  Today, thousands of skiers and snowboarders rely on SlopeVision to make informed decisions
                  about their mountain adventures. We're proud to be part of your snow day planning process.
                </p>
              </div>
            </div>
            <div
              class="flex flex-col justify-center items-center bg-gradient-to-br from-blue-500 to-indigo-600 p-12 text-white text-center">
              <div class="flex justify-center items-center bg-white/20 backdrop-blur-sm mb-6 rounded-full w-32 h-32">
                <HeartIcon class="w-16 h-16" />
              </div>
              <h4 class="mb-2 font-bold text-xl">Built with Passion</h4>
              <p class="opacity-90">For the skiing community</p>
              <div class="gap-4 grid grid-cols-3 mt-8">
                <div class="bg-white/10 backdrop-blur-sm p-4 rounded-lg">
                  <div class="font-bold text-2xl">2</div>
                  <div class="opacity-80 text-xs">Team Members</div>
                </div>
                <div class="bg-white/10 backdrop-blur-sm p-4 rounded-lg">
                  <div class="font-bold text-2xl">20+</div>
                  <div class="opacity-80 text-xs">Resorts</div>
                </div>
                <div class="bg-white/10 backdrop-blur-sm p-4 rounded-lg">
                  <div class="font-bold text-2xl">24/7</div>
                  <div class="opacity-80 text-xs">Monitoring</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <!-- <section class="bg-white dark:bg-gray-900 py-24 text-white">
      <div class="mx-auto px-4 sm:px-6 lg:px-8 max-w-7xl">
        <div class="mb-16 text-center">
          <div class="inline-block bg-blue-100 dark:bg-blue-900/30 mb-4 px-4 py-2 rounded-full font-medium text-blue-600 dark:text-blue-300 text-sm">
            By The Numbers
          </div>
          <h2 class="mb-4 font-bold text-gray-900 dark:text-white text-4xl">SlopeVision in Action</h2>
          <p class="mx-auto max-w-3xl text-gray-600 dark:text-gray-300 text-xl">
            Join thousands of skiers and snowboarders who trust SlopeVision for their mountain adventures.
          </p>
        </div>

        <div class="gap-8 grid md:grid-cols-4">
          <div class="bg-gray-50 dark:bg-gray-800 shadow-lg hover:shadow-xl backdrop-blur-sm p-8 rounded-xl text-center">
            <div class="mb-2 font-bold text-blue-500 dark:text-blue-400 text-5xl">500+</div>
            <div class="text-gray-600 dark:text-gray-300">Ski Resorts</div>
          </div>
          <div class="bg-gray-50 dark:bg-gray-800 shadow-lg hover:shadow-xl backdrop-blur-sm p-8 rounded-xl text-center">
            <div class="mb-2 font-bold text-green-500 dark:text-green-400 text-5xl">1,200+</div>
            <div class="text-gray-600 dark:text-gray-300">Webcam Feeds</div>
          </div>
          <div class="bg-gray-50 dark:bg-gray-800 shadow-lg hover:shadow-xl backdrop-blur-sm p-8 rounded-xl text-center">
            <div class="mb-2 font-bold text-purple-500 dark:text-purple-400 text-5xl">50+</div>
            <div class="text-gray-600 dark:text-gray-300">Countries</div>
          </div>
          <div class="bg-gray-50 dark:bg-gray-800 shadow-lg hover:shadow-xl backdrop-blur-sm p-8 rounded-xl text-center">
            <div class="mb-2 font-bold text-yellow-500 dark:text-yellow-400 text-5xl">24/7</div>
            <div class="text-gray-600 dark:text-gray-300">Monitoring</div>
          </div>
        </div>
      </div>
    </section>-->

    <!-- CTA Section -->
    <section class="relative bg-gradient-to-r from-blue-600 to-indigo-600 py-32 overflow-hidden">
      <div class="absolute inset-0 bg-blue-600/90"></div>
      <div class="relative mx-auto px-4 sm:px-6 lg:px-8 max-w-4xl text-center">
        <h2 class="mb-6 font-bold text-white text-4xl">Ready to Find Your Perfect Powder Day?</h2>
        <p class="mb-10 text-blue-100 text-xl">
          Join SlopeVision today and never miss another epic snow day. Start exploring webcams from ski resorts
          worldwide.
        </p>
        <div class="flex sm:flex-row flex-col justify-center gap-4">
          <router-link to="/register"
            class="inline-flex items-center bg-white hover:bg-gray-100 hover:shadow-lg px-8 py-4 rounded-lg font-semibold text-blue-600 transition-all hover:-translate-y-1 duration-300 transform">
            Get Started Free
            <ArrowRightIcon class="ml-2 w-5 h-5" />
          </router-link>
          <router-link to="/map"
            class="inline-flex items-center bg-blue-700 hover:bg-blue-800 hover:shadow-lg px-8 py-4 rounded-lg font-semibold text-white transition-all hover:-translate-y-1 duration-300 transform">
            Explore Webcams
            <MapPinIcon class="ml-2 w-5 h-5" />
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
import {
  StarIcon,
  ArrowRightIcon,
  VideoCameraIcon,
  GlobeAltIcon,
  ClockIcon,
  ChartBarIcon,
  MapPinIcon,
  UserIcon,
  SignalIcon,
  HeartIcon
} from '@heroicons/vue/24/outline';

export default {
  name: 'AboutView',
  components: {
    StarIcon,
    ArrowRightIcon,
    VideoCameraIcon,
    GlobeAltIcon,
    ClockIcon,
    ChartBarIcon,
    MapPinIcon,
    UserIcon,
    SignalIcon,
    HeartIcon
  },
  meta: {
    title: 'About - SlopeVision'
  }
}
</script>

<style scoped>
/* Snowflake animation */
.snowflakes {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.snowflake {
  position: absolute;
  opacity: 0.8;
  animation: fall linear infinite;
  color: black;
}

@keyframes fall {
  0% {
    transform: translateY(-10%) translateX(0) rotate(0deg);
    opacity: 0;
  }

  10% {
    opacity: 0.8;
  }

  90% {
    opacity: 0.8;
  }

  100% {
    transform: translateY(110vh) translateX(50px) rotate(360deg);
    opacity: 0;
  }
}

/* Individual snowflake positioning and animation */
.snowflake:nth-child(1) {
  left: 10%;
  animation-duration: 15s;
  animation-delay: 0s;
  font-size: 1em;
}

.snowflake:nth-child(2) {
  left: 25%;
  animation-duration: 18s;
  animation-delay: 2s;
  font-size: 0.8em;
}

.snowflake:nth-child(3) {
  left: 40%;
  animation-duration: 12s;
  animation-delay: 1s;
  font-size: 1.2em;
}

.snowflake:nth-child(4) {
  left: 55%;
  animation-duration: 16s;
  animation-delay: 3s;
  font-size: 0.9em;
}

.snowflake:nth-child(5) {
  left: 70%;
  animation-duration: 14s;
  animation-delay: 0.5s;
  font-size: 1.1em;
}

.snowflake:nth-child(6) {
  left: 85%;
  animation-duration: 17s;
  animation-delay: 4s;
  font-size: 0.7em;
}

.snowflake:nth-child(7) {
  left: 20%;
  animation-duration: 13s;
  animation-delay: 1.5s;
  font-size: 1em;
}

.snowflake:nth-child(8) {
  left: 35%;
  animation-duration: 19s;
  animation-delay: 2.5s;
  font-size: 0.9em;
}

.snowflake:nth-child(9) {
  left: 50%;
  animation-duration: 11s;
  animation-delay: 0.2s;
  font-size: 1.3em;
}

.snowflake:nth-child(10) {
  left: 65%;
  animation-duration: 20s;
  animation-delay: 3.5s;
  font-size: 0.8em;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .snowflakes {
    display: none;
  }
}
</style>