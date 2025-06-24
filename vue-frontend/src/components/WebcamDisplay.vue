<template>
  <div class="flex justify-center items-center">
    <div v-if="webcams.length"
      class="relative bg-item-light-bg dark:bg-item-dark-bg shadow-lg rounded-lg rounded-t-lg w-full 3xl:max-w-screen-2xl max-w-6xl overflow-hidden">
      <!-- Webcam Image or History -->
      <div ref="webcamContainer" class="relative">
        <!-- Historical Image -->
        <div v-if="selectedHistory" class="flex flex-col justify-center w-full h-full">
          <WebcamVideo :altText="selectedHistory.timestamp" :url="selectedHistory.url"
            class="w-full h-full object-contain" />

          <div class="right-0 bottom-0 left-0 absolute bg-gradient-to-t from-black/70 to-transparent p-4">
            <div class="flex justify-between items-center">
              <div>
                <p class="font-medium text-white text-sm">
                  {{ currentWebcam.name }} - {{ formatDateTime(selectedHistory.timestamp) }}
                </p>
                <p class="text-gray-300 text-xs">
                  Historical view - {{ timeAgo(selectedHistory.timestamp) }}
                </p>
              </div>
              <div class="flex space-x-2">
                <button @click="downloadImage(selectedHistory.url)"
                  class="bg-black/50 hover:bg-black/70 p-2 rounded-full">
                  <ArrowDownTrayIcon class="w-5 h-5 text-white" />
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Live Feed -->
        <div v-else class="w-full h-full">
          <WebcamVideo :altText="currentWebcam.name" :url="currentWebcam.url" class="w-full h-full object-contain" />

          <div class="right-0 bottom-0 left-0 absolute bg-gradient-to-t from-black/70 to-transparent p-4">
            <div class="flex justify-between items-center">
              <div>
                <p class="font-medium text-white text-sm">
                  {{ currentWebcam.name }}
                </p>
                <div class="flex items-center">
                  <span class="flex items-center">
                    <span class="bg-green-500 mr-1 rounded-full w-2 h-2 animate-pulse"></span>
                    <span class="text-green-400 text-xs">LIVE</span>
                  </span>
                  <span v-if="lastUpdated" class="ml-2 text-gray-300 text-xs">
                    Updated {{ timeAgo(lastUpdated) }}
                  </span>
                </div>
              </div>
              <div class="flex space-x-2">
                <button @click="downloadImage(currentWebcam.url)"
                  class="hidden bg-black/50 hover:bg-black/70 p-2 rounded-full">
                  <ArrowDownTrayIcon class="w-5 h-5 text-white" />
                </button>
                <button id="fullscreenToggle" @click="toggleFullscreen"
                  class="bg-black/50 hover:bg-black/70 p-2 rounded-full">
                  <ArrowsPointingOutIcon v-if="!fullscreenEnabled" class="w-5 h-5 text-white" />
                  <ArrowsPointingInIcon v-else class="w-5 h-5 text-white" />
                </button>
              </div>
            </div>
          </div>
        </div>
        <div class="absolute inset-0 flex justify-between items-center pointer-events-none">
          <!-- Left Arrow -->
          <button
            class="bg-white bg-opacity-10 hover:bg-opacity-60 ml-2 p-4 rounded-full hover:scale-110 transition-transform duration-200 pointer-events-auto transform"
            @click="prevWebcam">
            <ChevronLeftIcon class="w-6 h-6" />
          </button>

          <!-- Right Arrow -->
          <button
            class="bg-white bg-opacity-10 hover:bg-opacity-60 mr-2 p-4 rounded-full hover:scale-110 transition-transform duration-200 pointer-events-auto transform"
            @click="nextWebcam">
            <ChevronRightIcon class="w-6 h-6" />
          </button>
        </div>
        <div class="top-4 right-4 absolute">
          <button v-if="selectedHistory" @click="switchToLive"
            class="bg-amber-500 hover:bg-amber-600 px-3 py-1 rounded-full font-bold text-amber-900 text-sm transition-colors">
            Switch to Live
          </button>
        </div>

      </div>

      <!-- Webcam Details & History Chooser in One Row on larger screens, stacked on mobile -->
      <div class="flex sm:flex-row flex-col sm:justify-between sm:items-center p-6">
        <div class="flex flex-col w-full sm:w-1/2">
          <h3 class="font-semibold text-primary-light dark:text-primary-dark text-2xl">
            {{ currentWebcam.name }}
          </h3>
          <p class="mt-2 text-secondary-light dark:text-secondary-dark">
            {{ currentWebcam.description || "No description available." }}
          </p>
        </div>

        <!-- Webcam History Time Picker (right side on larger screens, below on mobile) -->
        <div class="flex flex-wrap justify-start sm:justify-end mt-4 sm:mt-0 w-full sm:w-1/2 h-full">
          <DateTimePicker ref="dateTimePickerRef" :webcamId="currentWebcam.id" class="mt-2 w-full sm:w-auto"
            @date-time-selected="handleDateTimeSelected" @date-selected="handleDateSelected" />
        </div>
      </div>
    </div>
    <!-- Loading and Error States -->
    <div v-else class="py-12 w-full text-center">
      <div class="flex flex-col items-center">
        <div class="mb-4 border-indigo-500 border-t-2 border-b-2 rounded-full w-12 h-12 animate-spin"></div>
        <p class="text-gray-500 dark:text-gray-300">Loading webcams...</p>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, onMounted, ref } from "vue";
import WebcamVideo from "@/components/WebcamVideo.vue";
import DateTimePicker from "@/components/DateTimePicker.vue";
import { isVideo } from "@/utils";
import { ArrowsPointingOutIcon, ArrowsPointingInIcon, ChevronLeftIcon, ChevronRightIcon } from "@heroicons/vue/24/outline";
import { API_URL } from '@/config';
import { format, parseISO, differenceInMinutes } from 'date-fns';

export default {
  name: "WebcamDisplay",
  methods: { isVideo },
  components: { WebcamVideo, DateTimePicker, ChevronLeftIcon, ChevronRightIcon, ArrowsPointingOutIcon, ArrowsPointingInIcon },
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
    const dateTimePickerRef = ref(null);
    const selectedDate = ref(null);
    const fullscreenEnabled = ref(false);

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
        } else {
          console.error("Failed to fetch webcams");
        }
      } catch (error) {
        console.error("Error fetching webcams:", error);
      }
    };

    const fetchHistory = async () => {
      if (webcams.value.length > 0) {
        const webcamId = webcams.value[currentIndex.value].id;
        try {
          const response = await fetch(`${API_URL}/api/webcams/${webcamId}/history/?date=${selectedDate.value}`);
          if (response.ok) {
            history.value = await response.json();
            console.log("History fetched:", history.value);
          } else {
            console.error("Failed to fetch history");
          }
        } catch (error) {
          console.error("Error fetching history:", error);
        }
      }
    };

    const handleDateTimeSelected = ({ timestamp }) => {
      const normalizeTimestamp = (ts) => new Date(ts).setSeconds(0, 0);
      const normalizedSelectedTimestamp = normalizeTimestamp(timestamp);
      const selectedItem = history.value.find(item => normalizeTimestamp(item.timestamp) === normalizedSelectedTimestamp);

      if (selectedItem) {
        selectedHistory.value = {
          ...selectedItem,
          url: selectedItem.image || selectedItem.video
        };
      } else {
        setTimeout(handleDateTimeSelected, 500, { timestamp });
      }
      selectedDate.value = normalizedSelectedTimestamp;
    };

    const handleDateSelected = async ({ date }) => {
      selectedDate.value = date;
      await fetchHistory();
    };


    const currentWebcam = computed(() => webcams.value[currentIndex.value]);

    const resetDateTimePicker = () => {
      selectedHistory.value = null;
      // call the reset method on the DateTimePicker component
      if (dateTimePickerRef.value) {
        dateTimePickerRef.value.reset();
      }
    };

    const prevWebcam = async () => {
      if (currentIndex.value > 0) {
        currentIndex.value--;
      } else {
        currentIndex.value = webcams.value.length - 1; // Loop to the last webcam
      }
      resetDateTimePicker();
    };

    const nextWebcam = async () => {
      if (currentIndex.value < webcams.value.length - 1) {
        currentIndex.value++;
      } else {
        currentIndex.value = 0; // Loop to the first webcam
      }
      resetDateTimePicker();
    };

    const toggleFullscreen = () => {
      const element = webcamContainer.value;

      if (!document.fullscreenElement) {
        element.style.objectFit = "contain"; // Ensure the image doesn't get cropped
        element.requestFullscreen({ navigationUI: "hide" }).catch((error) => {
          console.error("Failed to enter fullscreen mode:", error);
        });

        if (document.fullscreenElement) {
          document.documentElement.style.overflow = 'hidden';
        }
        fullscreenEnabled.value = true;
      } else {
        document.exitFullscreen();
        if (element) {
          element.style.objectFit = ""; // Remove object-fit style
        }
        document.documentElement.style.overflow = ''; // Restore default overflow behavior
        fullscreenEnabled.value = false;
      }
    };


    const switchToLive = () => {
      selectedHistory.value = null;
    };

    onMounted(fetchWebcams);

    return {
      webcams,
      currentWebcam,
      prevWebcam,
      nextWebcam,
      toggleFullscreen,
      webcamContainer,
      history,
      selectedHistory,
      dateTimePickerRef,
      handleDateTimeSelected,
      handleDateSelected,
      switchToLive,
      resetDateTimePicker,
      formatDateTime,
      formatTime,
      timeAgo,
      fullscreenEnabled,
    };
  },
};
</script>

<style scoped></style>
