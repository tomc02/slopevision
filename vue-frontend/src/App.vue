<template>
  <div id="app"
    class="flex flex-col bg-gradient-to-br from-app-light-bg dark:from-app-dark-bg to-item-secondary-light dark:to-item-dark-bg min-h-screen text-gray-900 dark:text-gray-100">
    <!-- Navbar Component -->
    <Navbar />

    <!-- Main Content Area -->
    <main class="flex-1 w-full">
      <!-- Router View for Dynamic Content -->
      <router-view />
    </main>


    <!-- Footer Component -->
    <footer class="bg-navbar-light-bg dark:bg-gray-900/95 p-2 h-10 text-sm text-center">
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
