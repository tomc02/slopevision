<template>
  <div id="app" class="bg-app-light-bg dark:bg-app-dark-bg dark:text-gray-100 h-screen flex flex-col">
    <!-- Navbar Component -->
    <Navbar/>

    <!-- Main Content Area -->
    <div class="bg-app-light-bg dark:bg-app-dark-bg flex-1 w-full px-4 py-4">
      <!-- Router View for Dynamic Content -->
      <router-view/>
    </div>

    <!-- Footer Component -->
    <footer class="bg-navbar-light-bg dark:bg-navbar-dark-bg text-center h-10 text-sm p-2">
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

