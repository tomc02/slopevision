<template>
  <div class="bg-gray-200 dark:bg-gray-900 dark:text-gray-100 min-h-fit py-8">
    <div class="container mx-auto px-4">
      <!-- Page Title -->
      <h1 class="text-3xl font-bold mb-8 text-center">
        Places Overview
      </h1>

      <!-- Search Bar -->
      <div class="mb-6 text-center">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search places..."
          class="p-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-100 w-3/4 sm:w-1/2"
        />
      </div>

      <!-- Places Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <router-link
          v-for="place in filteredPlaces"
          :key="place.id"
          :to="{ name: 'PlaceDetail', params: { id: place.id } }"
          class="bg-gray-300 dark:bg-gray-700 rounded-lg shadow-lg overflow-hidden transition-transform transform hover:scale-105"
        >
          <WebcamVideo :altText="place.name" :url="place.firstWebcam" style="pointer-events: none"/>

          <!-- Place Details -->
          <div class="p-4">
            <h2 class="text-xl font-semibold text-gray-800 dark:text-gray-100">{{ place.name }}</h2>
            <p class="text-gray-600 dark:text-gray-300 mt-2 text-sm line-clamp-3">
              {{ place.description || "No description available." }}
            </p>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { onMounted, ref, computed } from "vue";
import WebcamVideo from "@/components/WebcamVideo.vue";

export default {
  name: "PlaceOverview",
  components: { WebcamVideo },
  setup() {
    const places = ref([]);
    const searchQuery = ref("");

    const fetchPlaces = async () => {
      const response = await fetch(`/api/places/`, {
        method: 'GET',
      });
      const data = await response.json();
      for (let i = 0; i < data.length; i++) {
        data[i].firstWebcam = await fetchFirstWebcam(data[i].id);
      }
      places.value = data;
    };

    const fetchFirstWebcam = async (placeId) => {
      const response = await fetch(`/api/places/${placeId}/webcams/`);
      const data = await response.json();
      return data[0].url;
    };

    const filteredPlaces = computed(() => {
      return places.value.filter(place =>
        place.name.toLowerCase().includes(searchQuery.value.toLowerCase())
      );
    });

    onMounted(fetchPlaces);

    return {
      places,
      searchQuery,
      filteredPlaces
    };
  },
};
</script>

<style scoped>
</style>
