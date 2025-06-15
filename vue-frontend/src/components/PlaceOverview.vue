<template>
  <div class="py-8 min-h-fit">
    <div class="mx-auto px-4 container">
      <!-- Page Title -->
      <h1 class="mb-8 font-bold text-3xl text-center">
        Places Overview
      </h1>

      <!-- Search Bar -->
      <div class="mb-6 text-center">
        <input
            v-model="searchQuery"
            class="dark:bg-gray-800 p-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 w-3/4 sm:w-1/2 dark:text-gray-100"
            placeholder="Search places..."
            type="text"
        />
      </div>

      <!-- Places Grid -->
      <div class="gap-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
        <router-link
            v-for="place in filteredPlaces"
            :key="place.id"
            :to="{ name: 'PlaceDetail', params: { id: place.id } }"
            class="relative bg-item-light-bg dark:bg-item-dark-bg shadow-lg rounded-lg overflow-hidden hover:scale-105 transition-transform transform"
        >
          <WebcamVideo :altText="place.name" :url="place.firstWebcam" style="pointer-events: none"/>

          <!-- Place Details -->
          <div class="p-4">
            <h2 class="font-semibold text-primary-light dark:text-primary-dark text-xl">{{ place.name }}</h2>
            <p class="mt-2 text-secondary-light dark:text-secondary-dark text-sm line-clamp-3">
              {{ place.description || "No description available." }}
            </p>
          </div>

          <!-- Favorite Button -->
          <button
              class="right-4 bottom-4 absolute flex justify-center items-center bg-transparent shadow-md rounded-full w-10 h-10"
              @click.stop.prevent="toggleFavorite(place.id)"
          >
            <HeartIcon
                :class="isFavorite(place.id) ? 'text-red-500' : 'text-gray-400'"
                :filled="isFavorite(place.id)"
                class="w-6 h-6"
            />
          </button>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import {computed, onMounted, ref} from "vue";
import WebcamVideo from "@/components/WebcamVideo.vue";
import {HeartIcon} from '@heroicons/vue/24/outline';
import {API_URL} from '@/config';

export default {
  name: "PlaceOverview",
  components: {WebcamVideo, HeartIcon},
  setup() {
    const places = ref([]);
    const searchQuery = ref("");
    const favorites = ref(new Set()); // Track favorites as a Set for quick lookup.

    const fetchPlaces = async () => {
      const response = await fetch(`${API_URL}/api/places/`, {method: "GET"});
      const data = await response.json();
      for (let i = 0; i < data.length; i++) {
        data[i].firstWebcam = await fetchFirstWebcam(data[i].id);
      }
      places.value = data;
    };

    const fetchFirstWebcam = async (placeId) => {
      const response = await fetch(`${API_URL}/api/places/${placeId}/webcams/`);
      const data = await response.json();
      return data[0]?.url || "";
    };

    const filteredPlaces = computed(() =>
        places.value.filter((place) =>
            place.name.toLowerCase().includes(searchQuery.value.toLowerCase())
        )
    );

    const toggleFavorite = (placeId) => {
      if (favorites.value.has(placeId)) {
        favorites.value.delete(placeId);
      } else {
        favorites.value.add(placeId);
      }
    };

    const isFavorite = (placeId) => favorites.value.has(placeId);

    onMounted(fetchPlaces);

    return {
      places,
      searchQuery,
      filteredPlaces,
      toggleFavorite,
      isFavorite
    };
  },
};
</script>

<style scoped>
button {
  transition: transform 0.2s ease-in-out;
}

button:hover {
  transform: scale(1.1);
}
</style>
