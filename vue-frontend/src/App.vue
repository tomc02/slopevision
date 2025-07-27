<template>
  <div id="app" class="flex flex-col bg-app-light-bg dark:bg-app-dark-bg h-screen dark:text-gray-100">
    <!-- Navbar Component -->
    <Navbar/>

    <!-- Main Content Area -->
    <div class="flex-1 bg-app-light-bg dark:bg-app-dark-bg w-full">
      <!-- Router View for Dynamic Content -->
      <router-view/>
    </div>

    <!-- Footer Component -->
    <footer class="bg-navbar-light-bg dark:bg-navbar-dark-bg p-2 h-10 text-sm text-center">
      <p class="text-secondary-light dark:text-secondary-dark">&copy; 2024 Slope Vision</p>
    </footer>
  </div>

</template>


<script>
import Navbar from "./components/AppNavbar.vue";

export default {
  name: "App",
  components: {
    Navbar,
  },
  setup() {
    if (localStorage.getItem('darkMode') === null) {
      // check if user has dark mode preference
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      localStorage.setItem('darkMode', JSON.stringify(prefersDark));
    }
    return {};
  },
};
</script>

