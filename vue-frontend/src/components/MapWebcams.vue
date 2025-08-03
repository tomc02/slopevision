<template>
  <div class="">
    <div class="mx-auto px-4 py-8 container">
      <!-- Header Section -->
      <div class="mb-8">
        <div
          class="bg-white/80 dark:bg-gray-800/80 shadow-xl backdrop-blur-md px-6 py-4 border border-gray-200 dark:border-gray-700 rounded-2xl">
          <div class="flex md:flex-row flex-col justify-between items-start md:items-center gap-6">
            <div class="flex items-center gap-3">
              <div class="bg-gradient-to-r from-blue-500 to-purple-600 shadow-lg p-3 rounded-xl">
                <MapPinIcon class="w-7 h-7 text-white" />
              </div>
              <div>
                <h1
                  class="bg-clip-text bg-gradient-to-r from-gray-900 dark:from-white to-gray-600 dark:to-gray-300 font-bold text-transparent text-2xl">
                  Webcams Map
                </h1>
                <p v-if="filteredPlaces.length > 0" class="mt-1 text-gray-600 dark:text-gray-400 text-sm">
                  Showing {{ filteredPlaces.length }} webcam{{ filteredPlaces.length !== 1 ? 's' : '' }}
                </p>
              </div>
            </div>

            <!-- Controls -->
            <div class="flex sm:flex-row flex-col items-stretch sm:items-center gap-4 w-full md:w-auto">
              <!-- Search Input with Suggestions -->
              <div class="relative flex-1 md:w-80">
                <div class="relative">
                  <MagnifyingGlassIcon
                    class="top-1/2 left-3 z-10 absolute w-5 h-5 text-gray-400 -translate-y-1/2 transform" />
                  <input ref="searchInput" v-model="searchQuery" @input="handleSearchInput"
                    @focus="showSuggestions = true" @blur="handleInputBlur" type="text"
                    placeholder="Search places worldwide..."
                    class="bg-white/80 dark:bg-gray-700/80 shadow-sm backdrop-blur-sm py-2 pr-10 pl-10 border border-gray-200 dark:border-gray-600 focus:border-transparent rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 w-full text-gray-900 dark:text-white transition-all duration-200 placeholder-gray-500 dark:placeholder-gray-400" />
                  <XMarkIcon v-if="searchQuery" @click="clearSearch"
                    class="top-1/2 right-3 absolute w-5 h-5 text-gray-400 hover:text-00 transition-colors -translate-y-1/2 cursor-pointer transform" />
                </div>
              </div>

              <!-- Country Filter -->
              <div class="relative">
                <select v-model="selectedCountry"
                  class="bg-white/80 dark:bg-gray-700/80 shadow-sm backdrop-blur-sm px-4 py-2 pr-10 border border-gray-200 dark:border-gray-600 focus:border-transparent rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 min-w-40 text-gray-900 dark:text-white transition-all duration-200 appearance-none">
                  <option :value="null">All countries</option>
                  <option v-for="country in availableCountries" :key="country" :value="country">
                    {{ country }}
                  </option>
                </select>
                <ChevronDownIcon
                  class="top-1/2 right-3 absolute w-5 h-5 text-gray-400 -translate-y-1/2 pointer-events-none transform" />
              </div>

              <!-- View Toggle Buttons -->
              <div
                class="flex bg-white/80 dark:bg-gray-700/80 shadow-sm backdrop-blur-sm p-1 border border-gray-200 dark:border-gray-600 rounded-xl">
                <button @click="mapView = 'terrain'"
                  :class="mapView === 'terrain' ? 'bg-blue-500 text-white shadow-sm' : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'"
                  class="px-3 py-2 rounded-lg font-medium text-sm transition-all duration-200">
                  <GlobeAltIcon class="w-4 h-4" />
                </button>
                <button @click="mapView = 'satellite'"
                  :class="mapView === 'satellite' ? 'bg-blue-500 text-white shadow-sm' : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'"
                  class="px-3 py-2 rounded-lg font-medium text-sm transition-all duration-200">
                  <PhotoIcon class="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Map Container -->
      <div class="relative">
        <div
          class="relative bg-white/80 dark:bg-gray-800/80 shadow-xl backdrop-blur-sm border border-white/20 dark:border-gray-700/30 rounded-2xl">
          <div class="z-10 absolute inset-0">
            <!-- Loading Overlay -->
            <div v-if="loading" class="flex flex-col items-center mt-8 text-center">
              <div class="relative">
                <div class="border-4 border-indigo-200 dark:border-indigo-800 rounded-full w-16 h-16 animate-spin">
                </div>
                <div
                  class="top-0 left-0 absolute border-4 border-t-indigo-600 border-transparent rounded-full w-16 h-16 animate-spin">
                </div>
              </div>
              <p class="mt-4 text-gray-600 dark:text-gray-400 text-lg">Loading map...</p>
            </div>

            <!-- Map -->
            <div ref="mapContainer" class="z-0 rounded-2xl w-full h-[70vh] min-h-[500px]"></div>

            <!-- Map Controls Overlay -->
            <div class="top-4 right-4 absolute flex flex-col gap-2">
              <button @click="centerOnUserLocation"
                class="bg-white/90 hover:bg-white dark:bg-gray-800/90 dark:hover:bg-gray-800 shadow-lg backdrop-blur-sm p-3 border border-gray-200 dark:border-gray-700 rounded-xl transition-all duration-200">
                <MapPinIcon class="w-5 h-5 text-gray-600 dark:text-gray-400" />
              </button>
              <button @click="fitAllMarkers"
                class="bg-white/90 hover:bg-white dark:bg-gray-800/90 dark:hover:bg-gray-800 shadow-lg backdrop-blur-sm p-3 border border-gray-200 dark:border-gray-700 rounded-xl transition-all duration-200">
                <ArrowsPointingOutIcon class="w-5 h-5 text-gray-600 dark:text-gray-400" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Search Suggestions Dropdown - Positioned at root level -->
    <Teleport to="body">
      <div v-if="showSuggestions && (searchSuggestions.length > 0 || isSearching)" :style="dropdownStyle"
        class="z-[99999] fixed bg-white dark:bg-gray-800 shadow-xl border border-gray-200 dark:border-gray-700 rounded-xl min-w-80 max-h-64 overflow-y-auto">
        <div v-if="isSearching" class="p-4 text-gray-500 dark:text-gray-400 text-center">
          <ArrowPathIcon class="mx-auto mb-2 w-5 h-5 animate-spin" />
          Searching locations...
        </div>
        <div v-else-if="searchSuggestions.length > 0">
          <div v-for="(suggestion, index) in searchSuggestions" :key="index" @mousedown="selectSuggestion(suggestion)"
            class="hover:bg-gray-50 dark:hover:bg-gray-700 p-3 border-gray-100 dark:border-gray-700 border-b last:border-b-0 transition-colors cursor-pointer">
            <div class="flex items-center gap-3">
              <MapPinIcon class="w-4 h-4 text-gray-400" />
              <div>
                <div class="font-medium text-gray-900 dark:text-white">{{ suggestion.display_name }}</div>
                <div class="text-gray-500 dark:text-gray-400 text-sm">{{ suggestion.type }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script>
import { ref, onMounted, watch, computed, h, createApp, nextTick, Teleport } from "vue";
import WebcamVideo from "@/components/WebcamVideo.vue";
import { API_URL } from "@/config";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import WebcamPopup from '@/components/WebcamPopup.vue';
import mapPinIcon from '@/assets/map-pin.svg';
import {
  MapPinIcon,
  MagnifyingGlassIcon,
  XMarkIcon,
  ChevronDownIcon,
  GlobeAltIcon,
  PhotoIcon,
  ArrowPathIcon,
  ArrowsPointingOutIcon,
  VideoCameraIcon,
  EyeIcon
} from '@heroicons/vue/24/outline';

export default {
  name: "MapWebcams",
  components: {
    WebcamVideo,
    MapPinIcon,
    MagnifyingGlassIcon,
    XMarkIcon,
    ChevronDownIcon,
    GlobeAltIcon,
    PhotoIcon,
    ArrowPathIcon,
    ArrowsPointingOutIcon,
    VideoCameraIcon,
    EyeIcon,
    Teleport
  },
  setup() {
    const map = ref(null);
    const mapContainer = ref(null);
    const places = ref([]);
    const markers = ref([]);
    const searchQuery = ref("");
    const selectedCountry = ref(null);
    const loading = ref(false);
    const mapView = ref('terrain');
    const showSuggestions = ref(false);
    const searchSuggestions = ref([]);
    const isSearching = ref(false);
    const searchTimeout = ref(null);
    const userLocation = ref(null);
    const searchInput = ref(null);
    const dropdownStyle = ref({});

    // Nominatim search for global locations
    const searchGlobalLocations = async (query) => {
      if (query.length < 3) {
        searchSuggestions.value = [];
        return;
      }

      isSearching.value = true;
      try {
        const response = await fetch(
          `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}&limit=5&addressdetails=1`
        );
        const data = await response.json();
        searchSuggestions.value = data.map(item => ({
          display_name: item.display_name,
          lat: parseFloat(item.lat),
          lon: parseFloat(item.lon),
          type: item.type || 'location',
          importance: item.importance || 0
        })).sort((a, b) => b.importance - a.importance);
      } catch (error) {
        console.error('Error searching locations:', error);
        searchSuggestions.value = [];
      } finally {
        isSearching.value = false;
      }
    };

    // Calculate dropdown position
    const updateDropdownPosition = () => {
      if (!searchInput.value) return;

      const rect = searchInput.value.getBoundingClientRect();
      dropdownStyle.value = {
        top: `${rect.bottom + window.scrollY + 8}px`,
        left: `${rect.left + window.scrollX}px`,
        width: `${rect.width}px`
      };
    };

    // Handle input blur with delay to allow click on suggestions
    const handleInputBlur = () => {
      setTimeout(() => {
        showSuggestions.value = false;
      }, 200);
    };

    // Handle search input with debouncing
    const handleSearchInput = () => {
      updateDropdownPosition();
      if (searchTimeout.value) {
        clearTimeout(searchTimeout.value);
      }
      searchTimeout.value = setTimeout(() => {
        searchGlobalLocations(searchQuery.value);
      }, 300);
    };

    // Select a search suggestion
    const selectSuggestion = (suggestion) => {
      searchQuery.value = suggestion.display_name;
      showSuggestions.value = false;

      // Pan to the selected location
      if (map.value) {
        map.value.setView([suggestion.lat, suggestion.lon], 10);
      }

      // Show webcams for this location + 30km radius
      markers.value.forEach(marker => marker.remove());
      markers.value = [];


    };

    // Clear search
    const clearSearch = () => {
      searchQuery.value = "";
      searchSuggestions.value = [];
      showSuggestions.value = false;
    };

    // Get user location
    const getUserLocation = () => {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            userLocation.value = {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            };
          },
          (error) => {
            console.error('Error getting user location:', error);
          }
        );
      }
    };

    // Center map on user location
    const centerOnUserLocation = () => {
      if (userLocation.value && map.value) {
        map.value.setView([userLocation.value.lat, userLocation.value.lng], 10);
      } else {
        getUserLocation();
      }
    };

    // Fit all markers in view
    const fitAllMarkers = () => {
      if (map.value && markers.value.length > 0) {
        const group = L.featureGroup(markers.value);
        map.value.fitBounds(group.getBounds().pad(0.1), { maxZoom: 12 });
      }
    };

    // Hide suggestions when clicking outside
    const hideSuggestions = (event) => {
      if (!event.target.closest('.relative')) {
        showSuggestions.value = false;
      }
    };

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
          icon: L.icon({
            iconUrl: mapPinIcon,
            iconSize: [32, 32],
            iconAnchor: [16, 16],
            popupAnchor: [0, -20],
          }),
        });

        // Dynamically render the Vue component
        const container = document.createElement('div');
        const app = createApp({
          render: () => h(WebcamPopup, { place }),
        });
        app.mount(container);

        // Bind the rendered component as popup content
        marker.bindPopup(container, {
          maxWidth: 400,
          className: 'webcam-popup',
          closeButton: true,
          autoClose: false,
          autoPan: true
        });
        marker.addTo(map.value);
        markers.value.push(marker);
      });

      // Fit bounds if there are markers
      if (markers.value.length > 0) {
        const group = L.featureGroup(markers.value);
        map.value.fitBounds(group.getBounds().pad(0.15), { maxZoom: 11 });
      }
    };

    // Update map layer based on view mode
    const updateMapLayer = () => {
      if (!map.value) return;

      // Remove existing tile layers
      map.value.eachLayer((layer) => {
        if (layer instanceof L.TileLayer) {
          map.value.removeLayer(layer);
        }
      });

      // Add new tile layer based on view mode
      let tileLayer;
      if (mapView.value === 'satellite') {
        tileLayer = L.tileLayer(
          'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
          {
            attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
            maxZoom: 18,
          }
        );
      } else {
        tileLayer = L.tileLayer(
          "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
          {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            maxZoom: 18,
          }
        );
      }

      tileLayer.addTo(map.value);
    };

    // Watch for filter changes to update markers
    watch([filteredPlaces], updateMarkers);

    // Watch for map view changes
    watch(mapView, updateMapLayer);

    onMounted(async () => {
      await fetchPlaces();
      getUserLocation();

      // Add click listener to hide suggestions
      document.addEventListener('click', hideSuggestions);

      // Init map
      map.value = L.map(mapContainer.value, {
        center: [48.7, 15.4],
        zoom: 6,
        zoomControl: false, // We'll add custom controls
        attributionControl: true,
      });

      // Add custom zoom control
      L.control.zoom({
        position: 'bottomright'
      }).addTo(map.value);

      updateMapLayer();
      updateMarkers();

      // Update dropdown position on window resize/scroll
      window.addEventListener('resize', updateDropdownPosition);
      window.addEventListener('scroll', updateDropdownPosition);
    });

    // Watch for suggestions visibility to update position
    watch(showSuggestions, (newVal) => {
      if (newVal) {
        nextTick(() => {
          updateDropdownPosition();
        });
      }
    });

    return {
      mapContainer,
      searchQuery,
      selectedCountry,
      availableCountries,
      filteredPlaces,
      loading,
      places,
      mapView,
      showSuggestions,
      searchSuggestions,
      isSearching,
      handleSearchInput,
      selectSuggestion,
      clearSearch,
      centerOnUserLocation,
      fitAllMarkers,
      searchInput,
      dropdownStyle,
      handleInputBlur,
    };
  },
};
</script>

<style scoped>
/* Popup styling */
:deep(.leaflet-popup.webcam-popup) {
  border-radius: 1rem;
  padding: 0;
  overflow: hidden;
}

:deep(.leaflet-popup-content) {
  margin: 0;
  border-radius: 1rem;
}

:deep(.leaflet-popup-content-wrapper) {
  border-radius: 1rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
}

:deep(.leaflet-popup-tip) {
  border-radius: 0.25rem;
}

/* Custom zoom controls */
:deep(.leaflet-control-zoom) {
  border: none !important;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05) !important;
  border-radius: 0.75rem !important;
  overflow: hidden;
}

:deep(.leaflet-control-zoom a) {
  background: rgba(255, 255, 255, 0.9) !important;
  border: none !important;
  color: #374151 !important;
  font-weight: 600;
  transition: all 0.2s ease;
  backdrop-filter: blur(10px);
}

:deep(.leaflet-control-zoom a:hover) {
  background: rgba(255, 255, 255, 1) !important;
  color: #1f2937 !important;
}

.dark :deep(.leaflet-control-zoom a) {
  background: rgba(31, 41, 55, 0.9) !important;
  color: #e5e7eb !important;
}

.dark :deep(.leaflet-control-zoom a:hover) {
  background: rgba(31, 41, 55, 1) !important;
  color: #f9fafb !important;
}

/* Attribution styling */
:deep(.leaflet-control-attribution) {
  background: rgba(255, 255, 255, 0.8) !important;
  border-radius: 0.5rem !important;
  font-size: 0.75rem !important;
  color: #6b7280 !important;
  backdrop-filter: blur(10px);
}

.dark :deep(.leaflet-control-attribution) {
  background: rgba(31, 41, 55, 0.8) !important;
  color: #9ca3af !important;
}

/* Marker animations */
:deep(.leaflet-marker-icon) {
  transition: all 0.3s ease;
}

:deep(.leaflet-marker-icon:hover) {
  transform: scale(1.1);
  filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.3));
}

:deep(.leaflet-popup-close-button) {
  color: #6b7280 !important;
  transition: color 0.2s ease;
  font-size: 1.5rem !important;
  margin: 0.25rem !important;
}
/* Search suggestions scrollbar */
.max-h-64::-webkit-scrollbar {
  width: 6px;
}

.max-h-64::-webkit-scrollbar-track {
  background: #f3f4f6;
  border-radius: 9999px;
}

.dark .max-h-64::-webkit-scrollbar-track {
  background: #374151;
}

.max-h-64::-webkit-scrollbar-thumb {
  background: #9ca3af;
  border-radius: 9999px;
}

.dark .max-h-64::-webkit-scrollbar-thumb {
  background: #6b7280;
}

.max-h-64::-webkit-scrollbar-thumb:hover {
  background: #6b7280;
}

.dark .max-h-64::-webkit-scrollbar-thumb:hover {
  background: #9ca3af;
}

/* Loading animation */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fadeInUp {
  animation: fadeInUp 0.5s ease-out;
}

/* Glassmorphism effect */
.glass {
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.18);
}

.dark .glass {
  background: rgba(31, 41, 55, 0.25);
  border: 1px solid rgba(75, 85, 99, 0.18);
}

/* Button hover effects */
button {
  transition: all 0.2s ease;
}

button:hover {
  transform: translateY(-1px);
}

button:active {
  transform: translateY(0);
}

/* Input focus effects */
input:focus,
select:focus {
  transform: translateY(-1px);
  box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.2);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  :deep(.leaflet-control-zoom) {
    transform: scale(0.9);
  }

  :deep(.leaflet-control-attribution) {
    font-size: 0.7rem !important;
  }
}

/* Dark mode transitions */
* {
  transition: background-color 0.2s ease, border-color 0.2s ease, color 0.2s ease;
}
</style>
