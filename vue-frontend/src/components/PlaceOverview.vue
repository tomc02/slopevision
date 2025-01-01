<template>
  <div class="bg-gray-200 dark:bg-gray-900 dark:text-gray-100 min-h-fit py-8">
    <div class="container mx-auto px-4">
      <!-- Page Title -->
      <h1 class="text-3xl font-bold mb-8 text-center">
        Places Overview
      </h1>

      <!-- Places Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <router-link
            v-for="place in places"
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
import {onMounted, ref} from "vue";
import WebcamVideo from "@/components/WebcamVideo.vue";

export default {
  name: "PlaceOverview",
  components: {WebcamVideo},
  setup() {
    const places = ref([]);

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
    }

    onMounted(fetchPlaces);
    return {
      places,
    };
  },
};
</script>
<style scoped>
</style>

