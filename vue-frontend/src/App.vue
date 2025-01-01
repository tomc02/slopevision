<template>
  <div id="app" class="bg-gray-200 dark:bg-gray-900 dark:text-gray-100 h-screen flex flex-col">
    <!-- Navbar Component -->
    <Navbar/>

    <!-- Main Content Area -->
    <div class="bg-gray-200 dark:bg-gray-900 flex-1 w-full px-4 py-4">
      <!-- Router View for Dynamic Content -->
      <router-view/>
    </div>

    <!-- Footer Component -->
    <footer class="bg-gray-800 dark:bg-gray-700 text-white text-center h-10 text-sm p-2">
      <p class="text-gray-200 dark:text-gray-400">&copy; 2024 Slope Vision</p>
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
};
</script>

