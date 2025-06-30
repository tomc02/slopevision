<template>
  <div class="py-8 min-h-fit">
    <div class="mx-auto px-4 container">
      <div class="flex md:flex-row flex-col justify-between items-center gap-4 mb-6">
        <h1 class="font-bold text-3xl">
          Webcams Map
          <span v-if="filteredPlaces.length > 0" class="font-normal text-gray-500 dark:text-gray-400 text-sm">
            ({{ filteredPlaces.length }} webcams)
          </span>
        </h1>
        <div class="flex items-center gap-2">
          <input v-model="searchQuery" type="text" placeholder="Search places..."
            class="dark:bg-gray-800 p-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 w-48 dark:text-gray-100" />
          <select v-model="selectedCountry" class="filter-select w-40">
            <option :value="null">All countries</option>
            <option v-for="country in availableCountries" :key="country" :value="country">
              {{ country }}
            </option>
          </select>
        </div>
      </div>
      <div class="shadow-lg rounded-lg overflow-hidden" style="height: 70vh; min-height: 400px;">
        <div ref="mapContainer" style="height: 100%; width: 100%;" />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch, computed, h , createApp} from "vue";
import WebcamVideo from "@/components/WebcamVideo.vue";
import { API_URL } from "@/config";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import WebcamPopup from '@/components/WebcamPopup.vue'

export default {
  name: "MapWebcams",
  components: { WebcamVideo },
  setup() {
    const map = ref(null);
    const mapContainer = ref(null);
    const places = ref([]);
    const markers = ref([]);
    const searchQuery = ref("");
    const selectedCountry = ref(null);
    const loading = ref(false);

    // Fetch places with webcam coordinates
    const fetchPlaces = async () => {
      loading.value = true;
      try {
        const response = await fetch(`${API_URL}/api/places/`);
        const data = await response.json();
        // Only include places with coordinates and webcam
        places.value = data.filter(
          p =>
            p.latitude &&
            p.longitude &&
            p.first_webcam_url &&
            typeof p.latitude === "number" &&
            typeof p.longitude === "number"
        );
      } catch (e) {
        // eslint-disable-next-line no-console
        console.error("Error fetching places:", e);
      }
      loading.value = false;
    };

    // Filtered places based on search/country
    const filteredPlaces = computed(() => {
      let result = [...places.value];
      if (searchQuery.value) {
        const q = searchQuery.value.toLowerCase();
        result = result.filter(
          p =>
            p.name.toLowerCase().includes(q) ||
            (p.description && p.description.toLowerCase().includes(q)) ||
            (p.nearest_city && p.nearest_city.toLowerCase().includes(q)) ||
            (p.mounain_range && p.mounain_range.toLowerCase().includes(q)) ||
            (p.country && p.country.toLowerCase().includes(q))
        );
      }
      if (selectedCountry.value) {
        result = result.filter(p => p.country === selectedCountry.value);
      }
      return result;
    });

    // Available countries for filter
    const availableCountries = computed(() => {
      const set = new Set();
      places.value.forEach(p => {
        if (p.country) set.add(p.country);
      });
      return Array.from(set).sort();
    });

    // Helper to clear all markers from map
    const clearMarkers = () => {
      markers.value.forEach(marker => marker.remove());
      markers.value = [];
    };

    // Add markers to map for filteredPlaces
    const updateMarkers = () => {
      if (!map.value) return;
      clearMarkers();

      filteredPlaces.value.forEach(place => {
        const marker = L.marker([place.latitude, place.longitude], {
          title: place.name,
        });

        // Dynamically render the Vue component
        const container = document.createElement('div');
        const app = createApp({
          render: () => h(WebcamPopup, { place }),
        });
        app.mount(container);

        // Bind the rendered component as popup content
        marker.bindPopup(container, { maxWidth: 380, className: 'webcam-popup' });
        marker.addTo(map.value);
        markers.value.push(marker);
      });

      // Fit bounds if there are markers
      if (markers.value.length > 0) {
        const group = L.featureGroup(markers.value);
        map.value.fitBounds(group.getBounds().pad(0.15), { maxZoom: 11 });
      }
    };

    // Watch for filter changes to update markers
    watch([filteredPlaces], updateMarkers);

    onMounted(async () => {
      await fetchPlaces();
      // Init map
      map.value = L.map(mapContainer.value, {
        center: [48.7, 15.4],
        zoom: 6,
        zoomControl: true,
        attributionControl: false,
      });
      L.tileLayer(
        "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        {
          attribution:
            '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
          maxZoom: 18,
        }
      ).addTo(map.value);

      updateMarkers();
    });

    return {
      mapContainer,
      searchQuery,
      selectedCountry,
      availableCountries,
      filteredPlaces,
      loading,
    };
  },
};
</script>

<style>
.filter-select {
  @apply dark:bg-gray-800 p-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:text-gray-100;
}

.leaflet-container {
  background: #f3f4f6;
  border-radius: 0.5rem;
}

.leaflet-popup.webcam-popup {
  border-radius: 12px;
  padding: 0;
}

.leaflet-popup-content {
  margin: 0;
}

</style>
