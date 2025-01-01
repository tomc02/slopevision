<template>
  <div class="flex justify-center items-center">
    <div v-if="webcams.length"
         class="relative bg-gray-300 dark:bg-gray-700 shadow-lg rounded-lg rounded-t-lg w-full max-w-6xl 3xl:max-w-screen-2xl overflow-hidden">
      <!-- Webcam Image or History -->
      <div class="relative" ref="webcamContainer">
        <div v-if="selectedHistory">
          <WebcamVideo :url="selectedHistory.url" :altText="selectedHistory.timestamp" class="rounded-t-lg"/>
        </div>
        <div v-else>
          <WebcamVideo :url="currentWebcam.url" :altText="currentWebcam.name" class="rounded-t-lg"/>
        </div>

        <div class="absolute inset-0 flex justify-between items-center pointer-events-none">
          <!-- Left Arrow -->
          <button
              class="pointer-events-auto p-4 bg-white bg-opacity-10 rounded-full hover:bg-opacity-70 transform transition-transform duration-200 hover:scale-110 ml-2"
              @click="prevWebcam">
            <ChevronLeftIcon class="w-6 h-6" />
          </button>

          <!-- Right Arrow -->
          <button
              class="pointer-events-auto p-4 bg-white bg-opacity-10 rounded-full hover:bg-opacity-70 transform transition-transform duration-200 hover:scale-110 mr-2"
              @click="nextWebcam">
             <ChevronRightIcon class="w-6 h-6" />
          </button>
        </div>

        <!-- Fullscreen Button -->
        <button
            v-if="!isVideo(currentWebcam.url)"
            class="absolute bottom-2 right-2 p-2 bg-gray-800 bg-opacity-70 text-white rounded-full hover:bg-opacity-100 transform transition-transform duration-200 hover:scale-110"
            @click="toggleFullscreen">
            <ArrowsPointingOutIcon class="w-6 h-6" />
        </button>
      </div>

      <!-- Webcam Details & History Chooser in One Row on larger screens, stacked on mobile -->
      <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center p-6">
        <div class="flex flex-col w-full sm:w-1/2">
          <h3 class="text-2xl font-semibold text-gray-800 dark:text-gray-100">
            {{ currentWebcam.name }}
          </h3>
          <p class="text-gray-600 dark:text-gray-300 mt-2">
            {{ currentWebcam.description || "No description available." }}
          </p>
        </div>

        <!-- Webcam History Time Picker (right side on larger screens, below on mobile) -->
        <div class="flex justify-start sm:justify-end w-full sm:w-1/2 mt-4 sm:mt-0 flex-wrap h-full ">
          <DateTimePicker :webcamId="currentWebcam.id" @date-time-selected="handleDateTimeSelected"
                          ref="dateTimePickerRef" class="w-full sm:w-auto mt-2"/>
          <button
              class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-5 rounded flex items-center justify-center w-full sm:w-auto mb-0.5 lg:ml-2 mt-2 sm:mt-10 max-h-10"
              @click="switchToLive">
            LIVE
          </button>
        </div>
      </div>
    </div>
    <!-- Loading and Error States -->
    <div v-else class="text-center">
      <p class="text-gray-500 dark:text-gray-300">Loading webcams...</p>
    </div>
  </div>
</template>

<script>
import {ref, computed, onMounted} from "vue";
import WebcamVideo from "@/components/WebcamVideo.vue";
import DateTimePicker from "@/components/DateTimePicker.vue";
import {isVideo} from "@/utils";
import {ChevronLeftIcon, ChevronRightIcon, ArrowsPointingOutIcon} from "@heroicons/vue/24/outline";

export default {
  name: "WebcamDisplay",
  methods: {isVideo},
  components: {WebcamVideo, DateTimePicker, ChevronLeftIcon, ChevronRightIcon, ArrowsPointingOutIcon},
  props: {
    placeId: Number,
    placeName: String,
  },
  setup(props) {
    const webcams = ref([]);
    const history = ref([]);
    const selectedHistory = ref(null);
    const selectedHistoryId = ref(null);
    const currentIndex = ref(0);
    const webcamContainer = ref(null);
    const dateTimePickerRef = ref(null);

    const fetchWebcams = async () => {
      try {
        const response = await fetch(`/api/places/${props.placeId}/webcams`);
        if (response.ok) {
          webcams.value = await response.json();
          fetchHistory();
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
          const response = await fetch(`/api/webcams/${webcamId}/history/`);
          if (response.ok) {
            history.value = await response.json();
          } else {
            console.error("Failed to fetch history");
          }
        } catch (error) {
          console.error("Error fetching history:", error);
        }
      }
    };

    const fetchSelectedHistory = () => {
      selectedHistory.value = history.value.find(
          (item) => item.id === selectedHistoryId.value
      );
      selectedHistory.value.url = selectedHistory.value.image || selectedHistory.value.video;
    };

    const handleDateTimeSelected = ({timestamp}) => {
      const normalizeTimestamp = (ts) => {
        const date = new Date(ts);
        date.setSeconds(0, 0);
        return date.getTime();
      };

      const normalizedSelectedTimestamp = normalizeTimestamp(timestamp);

      const selectedItem = history.value.find(
          (item) => normalizeTimestamp(item.timestamp) === normalizedSelectedTimestamp
      );

      if (selectedItem) {
        selectedHistoryId.value = selectedItem.id;
        fetchSelectedHistory();
      }
    };


    const currentWebcam = computed(() => webcams.value[currentIndex.value]);

    const resetDateTimePicker = () => {
      // Reset the selected date and time when switching webcams
      selectedHistoryId.value = null;
      selectedHistory.value = null;
      // call the reset method on the DateTimePicker component
      if (dateTimePickerRef.value) {
        dateTimePickerRef.value.reset();
        dateTimePickerRef.value.setToday();
      }
    };

    const prevWebcam = async () => {
      if (currentIndex.value > 0) {
        currentIndex.value--;
      } else {
        currentIndex.value = webcams.value.length - 1; // Loop to the last webcam
      }
      await fetchHistory();
      resetDateTimePicker();
    };

    const nextWebcam = async () => {
      if (currentIndex.value < webcams.value.length - 1) {
        currentIndex.value++;
      } else {
        currentIndex.value = 0; // Loop to the first webcam
      }
      await fetchHistory();
      resetDateTimePicker();
    };

    const toggleFullscreen = () => {
      const element = webcamContainer.value;

      if (!document.fullscreenElement) {
        element.style.objectFit = "contain"; // Ensure the image doesn't get cropped
        element.requestFullscreen({navigationUI: "hide"}).catch((error) => {
          console.error("Failed to enter fullscreen mode:", error);
        });

        if (document.fullscreenElement) {
          document.documentElement.style.overflow = 'hidden';
        }
      } else {
        document.exitFullscreen();
        if (element) {
          element.style.objectFit = ""; // Remove object-fit style
        }
        document.documentElement.style.overflow = ''; // Restore default overflow behavior
      }
    };


    const switchToLive = () => {
      selectedHistory.value = null;
      selectedHistoryId.value = null;
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
      selectedHistoryId,
      dateTimePickerRef,
      fetchSelectedHistory,
      handleDateTimeSelected,
      switchToLive,
      resetDateTimePicker,
    };
  },
};
</script>

<style scoped>
</style>
