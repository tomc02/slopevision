<template>
  <div class="flex justify-center items-center">
    <!-- Loading State -->
    <div v-if="!webcams.length" class="py-12 w-full text-center">
      <div class="flex flex-col items-center">
        <div class="mb-4 border-indigo-500 border-t-2 border-b-2 rounded-full w-12 h-12 animate-spin"></div>
        <p class="text-gray-500 dark:text-gray-300">Loading webcams...</p>
      </div>
    </div>

    <!-- Main Content -->
    <div v-else class="mx-4 w-full max-w-[94%]">
      <!-- Webcam Tabs (Desktop) -->
      <div class="hidden md:flex mb-4 border-gray-200 dark:border-gray-700 border-b">
        <button v-for="(webcam, index) in webcams" :key="webcam.id" @click="switchWebcam(index)"
          class="px-4 py-2 focus:outline-none font-medium text-sm transition-colors" :class="{
            'text-indigo-600 border-b-2 border-indigo-600 dark:text-indigo-400 dark:border-indigo-400': currentIndex === index,
            'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300': currentIndex !== index
          }">
          {{ webcam.name }}
        </button>
      </div>

      <!-- Main Content Area -->
      <div class="flex lg:flex-row flex-col gap-6 mx-auto overflow-hidden">
        <!-- Webcam Viewer -->
        <div
          class="relative flex-col flex-1 bg-item-light-bg dark:bg-item-dark-bg shadow-lg rounded-lg overflow-hidden">
          <!-- Webcam Image/Video -->
          <div ref="webcamContainer" class="relative aspect-video">
            <!-- Historical Image -->
            <div v-if="selectedHistory" class="w-full h-full">
              <WebcamVideo :altText="selectedHistory.timestamp" :url="selectedHistory.url"
                class="w-full h-full object-cover" />

              <div
                class="absolute inset-0 flex flex-col justify-end bg-gradient-to-t from-black/80 via-black/20 to-transparent p-4">
                <div class="flex justify-between items-center">
                  <div>
                    <h2 class="font-bold text-white text-lg">
                      {{ currentWebcam.name }}
                    </h2>
                    <p class="text-gray-300 text-sm">
                      {{ formatDateTime(selectedHistory.timestamp) }} ({{ timeAgo(selectedHistory.timestamp) }})
                    </p>
                  </div>
                  <div class="flex space-x-2">
                    <button @click="downloadImage(selectedHistory.url)"
                      class="bg-white/10 hover:bg-white/20 p-2 rounded-full transition-colors"
                      title="Download snapshot">
                      <ArrowDownTrayIcon class="w-5 h-5 text-white" />
                    </button>
                    <button @click="toggleFullscreen"
                      class="bg-white/10 hover:bg-white/20 p-2 rounded-full transition-colors"
                      :title="fullscreenEnabled ? 'Exit fullscreen' : 'Enter fullscreen'">
                      <ArrowsPointingOutIcon v-if="!fullscreenEnabled" class="w-5 h-5 text-white" />
                      <ArrowsPointingInIcon v-else class="w-5 h-5 text-white" />
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Live Feed -->
            <div v-else class="w-full h-full">
              <WebcamVideo :altText="currentWebcam.name" :url="currentWebcam.url" class="w-full h-full object-cover"
                @loaded="handleVideoLoaded" />

              <div
                class="absolute inset-0 flex flex-col justify-end bg-gradient-to-t from-black/80 via-black/20 to-transparent p-4">
                <div class="flex justify-between items-center">
                  <div>
                    <h2 class="font-bold text-white text-lg">
                      {{ currentWebcam.name }}
                    </h2>
                    <div class="flex items-center space-x-2">
                      <span class="flex items-center text-sm">
                        <span class="bg-green-500 mr-1 rounded-full w-2 h-2 animate-pulse"></span>
                        <span class="text-green-400">LIVE</span>
                      </span>
                      <span v-if="lastUpdated" class="text-gray-300 text-sm">
                        Updated {{ timeAgo(lastUpdated) }}
                      </span>
                    </div>
                  </div>
                  <div class="flex space-x-2">
                    <button @click="downloadImage(currentWebcam.url)"
                      class="bg-white/10 hover:bg-white/20 p-2 rounded-full transition-colors"
                      title="Download snapshot">
                      <ArrowDownTrayIcon class="w-5 h-5 text-white" />
                    </button>
                    <button @click="toggleFullscreen"
                      class="bg-white/10 hover:bg-white/20 p-2 rounded-full transition-colors"
                      :title="fullscreenEnabled ? 'Exit fullscreen' : 'Enter fullscreen'">
                      <ArrowsPointingOutIcon v-if="!fullscreenEnabled" class="w-5 h-5 text-white" />
                      <ArrowsPointingInIcon v-else class="w-5 h-5 text-white" />
                    </button>
                  </div>
                </div>
              </div>
            </div>

            <!-- Navigation Arrows -->
            <div class="absolute inset-0 flex justify-between items-center px-2 pointer-events-none">
              <button @click="prevWebcam"
                class="bg-white/20 hover:bg-white/30 backdrop-blur-sm p-3 rounded-full hover:scale-110 transition-all pointer-events-auto"
                aria-label="Previous webcam">
                <ChevronLeftIcon class="w-6 h-6 text-white" />
              </button>
              <button @click="nextWebcam"
                class="bg-white/20 hover:bg-white/30 backdrop-blur-sm p-3 rounded-full hover:scale-110 transition-all pointer-events-auto"
                aria-label="Next webcam">
                <ChevronRightIcon class="w-6 h-6 text-white" />
              </button>
            </div>

            <!-- Switch to Live Button -->
            <button v-if="selectedHistory" @click="switchToLive"
              class="top-4 right-4 absolute flex items-center space-x-1 bg-amber-500 hover:bg-amber-600 px-4 py-2 rounded-full font-bold text-amber-900 text-sm transition-colors">
              <PlayIcon class="w-4 h-4" />
              <span>Live View</span>
            </button>
          </div>

          <!-- Webcam Description (Mobile) -->
          <div class="md:hidden p-4">
            <h3 class="font-semibold text-primary-light dark:text-primary-dark text-xl">
              {{ currentWebcam.name }}
            </h3>
            <p class="mt-1 text-secondary-light dark:text-secondary-dark text-sm">
              {{ currentWebcam.description || "No description available." }}
            </p>
          </div>
        </div>

        <!-- History Timeline (Desktop) -->
        <div class="hidden lg:flex flex-col flex-shrink-0 w-72 min-h-0">

          <div class="flex flex-col flex-1 bg-item-light-bg dark:bg-item-dark-bg shadow-lg p-4 rounded-lg min-h-0"
            :style="{ 'max-height': historyHeight + 'px' }">

            <!-- Header -->
            <div class="flex justify-between items-center mb-4">
              <h3 class="font-semibold text-primary-light dark:text-primary-dark">
                History Timeline
              </h3>
              <button @click="fetchHistory" class="text-indigo-600 dark:text-indigo-400 text-sm hover:underline">
                Refresh
              </button>
            </div>

            <!-- Scrollable History -->
            <div class="flex-1 min-h-0 overflow-y-auto history-panel">
              <div v-if="historyLoading" class="flex justify-center items-center h-full">
                <div class="border-indigo-500 border-t-2 border-b-2 rounded-full w-8 h-8 animate-spin"></div>
              </div>

              <div v-else-if="history.length === 0" class="py-8 text-gray-500 dark:text-gray-400 text-center">
                No history available for this date
              </div>

              <div v-else>
                <div v-for="item in history" :key="item.timestamp" @click="selectHistoryItem(item)"
                  class="group mr-2 mb-3 cursor-pointer">
                  <div class="relative border-2 rounded aspect-video overflow-hidden transition-all" :class="{
                    'border-indigo-500': selectedHistory && selectedHistory.timestamp === item.timestamp,
                    'border-transparent group-hover:border-gray-300 dark:group-hover:border-gray-600': !(selectedHistory && selectedHistory.timestamp === item.timestamp)
                  }">
                    <WebcamVideo :url="item.thumbnail || item.image || item.video" :alt="formatDateTime(item.timestamp)"
                      :controls="false" class="w-full h-full object-cover" />
                    <div class="absolute inset-0 bg-black/30 group-hover:bg-black/20 transition-colors"></div>
                    <div class="right-1 bottom-1 left-1 absolute bg-black/70 p-1 rounded text-white text-xs">
                      {{ formatTime(item.timestamp) }}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Date Picker -->
            <div class="mt-4 pt-4 border-gray-200 dark:border-gray-700 border-t">
              <label class="block mb-2 font-medium text-gray-700 dark:text-gray-300 text-sm">Select Date</label>
              <input type="date" v-model="selectedDate" @change="handleDateChange"
                class="bg-white dark:bg-gray-800 shadow-sm px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-1 focus:ring-indigo-500 w-full text-sm" />
            </div>

          </div>
        </div>
      </div>

      <!-- Mobile Controls -->
      <div class="lg:hidden mt-4">
        <div class="bg-item-light-bg dark:bg-item-dark-bg shadow-lg p-4 rounded-lg">
          <h3 class="mb-3 font-semibold text-primary-light dark:text-primary-dark">
            {{ currentWebcam.name }} History
          </h3>

          <div class="mb-4">
            <label class="block mb-2 font-medium text-gray-700 dark:text-gray-300 text-sm">Select Date</label>
            <input type="date" v-model="selectedDate" @change="handleDateChange"
              class="bg-white dark:bg-gray-800 shadow-sm px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-1 focus:ring-indigo-500 w-full text-sm" />
          </div>

          <div v-if="historyLoading" class="flex justify-center py-4">
            <div class="border-indigo-500 border-t-2 border-b-2 rounded-full w-8 h-8 animate-spin"></div>
          </div>

          <div v-else-if="history.length === 0" class="py-4 text-gray-500 dark:text-gray-400 text-center">
            No history available for this date
          </div>

          <div v-else class="gap-2 grid grid-cols-3">
            <div v-for="item in history" :key="item.timestamp" @click="selectHistoryItem(item)"
              class="relative aspect-square cursor-pointer">
              <img :src="item.thumbnail || item.image || item.video" :alt="formatDateTime(item.timestamp)"
                class="rounded w-full h-full object-cover" />
              <div class="absolute inset-0 bg-black/30 group-hover:bg-black/20 transition-colors"></div>
              <div class="right-0 bottom-0 left-0 absolute bg-black/70 p-1 text-white text-xs text-center">
                {{ formatTime(item.timestamp) }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, onMounted, ref, watch } from "vue";
import WebcamVideo from "@/components/WebcamVideo.vue";
import {
  ArrowsPointingOutIcon,
  ArrowsPointingInIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  ArrowDownTrayIcon,
  PlayIcon
} from "@heroicons/vue/24/outline";
import { API_URL } from '@/config';
import { format, parseISO, differenceInMinutes } from 'date-fns';

export default {
  name: "WebcamDisplay",
  components: {
    WebcamVideo,
    ChevronLeftIcon,
    ChevronRightIcon,
    ArrowsPointingOutIcon,
    ArrowsPointingInIcon,
    ArrowDownTrayIcon,
    PlayIcon
  },
  props: {
    placeId: Number,
    placeName: String,
  },
  setup(props) {
    const webcams = ref([]);
    const history = ref([]);
    const selectedHistory = ref(null);
    const currentIndex = ref(0);
    const webcamContainer = ref(null);
    const fullscreenEnabled = ref(false);
    const lastUpdated = ref(null);
    const historyLoading = ref(false);
    const historyHeight = ref(1500); // Default height for history panel
    const historyFetchToken = ref(0); // Token to track latest fetch
    const historyFetchTimeout = ref(null); // Timeout for debounce

    // Set default date to today
    const selectedDate = ref(format(new Date(), 'yyyy-MM-dd'));

    const formatDateTime = (timestamp) => {
      return format(parseISO(timestamp), 'MMM d, yyyy h:mm a');
    };

    const formatTime = (timestamp) => {
      return format(parseISO(timestamp), 'h:mm a');
    };

    const timeAgo = (timestamp) => {
      const minutes = differenceInMinutes(new Date(), parseISO(timestamp));
      if (minutes < 1) return "just now";
      if (minutes < 60) return `${minutes} min ago`;
      const hours = Math.floor(minutes / 60);
      if (hours < 24) return `${hours} hour${hours > 1 ? 's' : ''} ago`;
      const days = Math.floor(hours / 24);
      if (days < 30) return `${days} day${days > 1 ? 's' : ''} ago`;
      const months = Math.floor(days / 30);
      if (months < 12) return `${months} month${months > 1 ? 's' : ''} ago`;
      const years = Math.floor(months / 12);
      return `${years} year${years > 1 ? 's' : ''} ago `;
    };

    const fetchWebcams = async () => {
      try {
        const response = await fetch(`${API_URL}/api/places/${props.placeId}/webcams`);
        if (response.ok) {
          webcams.value = await response.json();
          // Fetch history for the first webcam
          await fetchHistory();
        } else {
          console.error("Failed to fetch webcams");
        }
      } catch (error) {
        console.error("Error fetching webcams:", error);
      }
    };

    const setHistoryPanelHeight = () => {
      if (webcamContainer.value) {
        historyHeight.value = webcamContainer.value.clientHeight; // Adjust for header and footer
      }
    };

    const fetchHistory = async () => {
      if (!webcams.value.length) return;
      historyLoading.value = true;
      const webcamId = webcams.value[currentIndex.value].id;
      historyFetchToken.value += 1;
      const thisFetchToken = historyFetchToken.value;
      try {
        const response = await fetch(
          `${API_URL}/api/webcams/${webcamId}/history/?date=${selectedDate.value}`
        );
        if (response.ok) {
          const data = await response.json();
          if (thisFetchToken === historyFetchToken.value) {
            history.value = data;
            history.value.sort((a, b) =>
              new Date(b.timestamp) - new Date(a.timestamp)
            );
          }
        } else {
          if (thisFetchToken === historyFetchToken.value) {
            console.error("Failed to fetch history");
            history.value = [];
          }
        }
      } catch (error) {
        if (thisFetchToken === historyFetchToken.value) {
          console.error("Error fetching history:", error);
          history.value = [];
        }
      } finally {
        if (thisFetchToken === historyFetchToken.value) {
          historyLoading.value = false;
        }
      }
    };

    // Debounced fetchHistory for webcam switching
    const debouncedFetchHistory = () => {
      if (historyFetchTimeout.value) {
        clearTimeout(historyFetchTimeout.value);
      }
      historyFetchTimeout.value = setTimeout(() => {
        fetchHistory();
        historyFetchTimeout.value = null;
      }, 500);
    };

    const selectHistoryItem = (item) => {
      selectedHistory.value = {
        ...item,
        url: item.image || item.video
      };
    };

    const handleDateChange = async () => {
      await fetchHistory();
      selectedHistory.value = null;
    };

    const currentWebcam = computed(() => webcams.value[currentIndex.value]);

    const switchWebcam = async (index) => {
      currentIndex.value = index;
      selectedHistory.value = null;
      debouncedFetchHistory();
    };

    const prevWebcam = async () => {
      const newIndex = currentIndex.value > 0
        ? currentIndex.value - 1
        : webcams.value.length - 1;
      await switchWebcam(newIndex);
    };

    const nextWebcam = async () => {
      const newIndex = currentIndex.value < webcams.value.length - 1
        ? currentIndex.value + 1
        : 0;
      await switchWebcam(newIndex);
    };

    const toggleFullscreen = () => {
      if (!document.fullscreenElement) {
        webcamContainer.value?.requestFullscreen({ navigationUI: "hide" })
          .then(() => {
            fullscreenEnabled.value = true;
          })
          .catch(console.error);
      } else {
        document.exitFullscreen();
        fullscreenEnabled.value = false;
      }
    };

    const switchToLive = () => {
      selectedHistory.value = null;
    };

    const handleVideoLoaded = () => {
      lastUpdated.value = new Date().toISOString();
    };

    const downloadImage = (url) => {
      const link = document.createElement('a');
      link.href = url;
      link.download = `${currentWebcam.value.name}_${selectedHistory.value ? formatDateTime(selectedHistory.value.timestamp) : 'live'}.jpg`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    };

    // Watch for webcam changes to fetch new history
    watch(currentIndex, debouncedFetchHistory);

    // Initialize
    onMounted(async () => {
      await fetchWebcams();
      setHistoryPanelHeight();
      window.addEventListener('resize', setHistoryPanelHeight);
    });

    return {
      webcams,
      currentWebcam,
      currentIndex,
      prevWebcam,
      nextWebcam,
      switchWebcam,
      toggleFullscreen,
      webcamContainer,
      history,
      selectedHistory,
      selectHistoryItem,
      switchToLive,
      formatDateTime,
      formatTime,
      timeAgo,
      fullscreenEnabled,
      lastUpdated,
      selectedDate,
      handleDateChange,
      historyLoading,
      handleVideoLoaded,
      downloadImage,
      historyHeight,
    };
  },
};
</script>

<style scoped>
/* Custom scrollbar for history panel */
.history-panel::-webkit-scrollbar {
  width: 12px;
}

.history-panel::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 10px;
}

.history-panel::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.4);
  border-radius: 10px;
}

.history-panel::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.5);
}
</style>