<template>
  <div class="flex justify-center items-center">
    <div v-if="webcams.length"
         class="relative bg-item-light-bg dark:bg-item-dark-bg shadow-lg rounded-lg rounded-t-lg w-full 3xl:max-w-screen-2xl max-w-6xl overflow-hidden">
      <!-- Webcam Image or History -->
      <div ref="webcamContainer" class="relative">
        <div v-if="selectedHistory">
          <WebcamVideo :altText="selectedHistory.timestamp" :url="selectedHistory.url" class="rounded-t-lg"/>
        </div>
        <div v-else>
          <WebcamVideo :altText="currentWebcam.name" :url="currentWebcam.url" class="rounded-t-lg"/>
        </div>

        <div class="absolute inset-0 flex justify-between items-center pointer-events-none">
          <!-- Left Arrow -->
          <button
              class="bg-white bg-opacity-10 hover:bg-opacity-60 ml-2 p-4 rounded-full hover:scale-110 transition-transform duration-200 pointer-events-auto transform"
              @click="prevWebcam">
            <ChevronLeftIcon class="w-6 h-6"/>
          </button>

          <!-- Right Arrow -->
          <button
              class="bg-white bg-opacity-10 hover:bg-opacity-60 mr-2 p-4 rounded-full hover:scale-110 transition-transform duration-200 pointer-events-auto transform"
              @click="nextWebcam">
            <ChevronRightIcon class="w-6 h-6"/>
          </button>
        </div>

        <!-- Fullscreen Button -->
        <button
            v-if="!isVideo(currentWebcam.url)"
            class="right-2 bottom-2 absolute bg-gray-800 bg-opacity-70 hover:bg-opacity-100 p-2 rounded-full text-white hover:scale-110 transition-transform duration-200 transform"
            @click="toggleFullscreen">
          <ArrowsPointingOutIcon class="w-6 h-6"/>
        </button>
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
          <DateTimePicker ref="dateTimePickerRef" :webcamId="currentWebcam.id"
                          class="mt-2 w-full sm:w-auto"
                          @date-time-selected="handleDateTimeSelected" @date-selected="handleDateSelected"/>
          <button
              class="flex justify-center items-center bg-blue-500 hover:bg-blue-700 mt-2 sm:mt-10 mb-0.5 lg:ml-2 px-5 py-2 rounded w-full sm:w-auto max-h-10 font-bold text-white"
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
import {computed, onMounted, ref} from "vue";
import WebcamVideo from "@/components/WebcamVideo.vue";
import DateTimePicker from "@/components/DateTimePicker.vue";
import {isVideo} from "@/utils";
import {ArrowsPointingOutIcon, ChevronLeftIcon, ChevronRightIcon} from "@heroicons/vue/24/outline";
import {API_URL} from '@/config';

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
    const currentIndex = ref(0);
    const webcamContainer = ref(null);
    const dateTimePickerRef = ref(null);
    const selectedDate = ref(null);

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
          } else {
            console.error("Failed to fetch history");
          }
        } catch (error) {
          console.error("Error fetching history:", error);
        }
      }
    };

    const handleDateTimeSelected = ({timestamp}) => {
      const normalizeTimestamp = (ts) => new Date(ts).setSeconds(0, 0);
      const normalizedSelectedTimestamp = normalizeTimestamp(timestamp);
      const selectedItem = history.value.find(item => normalizeTimestamp(item.timestamp) === normalizedSelectedTimestamp);

      if (selectedItem) {
        selectedHistory.value = {
          ...selectedItem,
          url: selectedItem.image || selectedItem.video
        };
      } else {
        setTimeout(handleDateTimeSelected, 500, {timestamp});
      }
      selectedDate.value = normalizedSelectedTimestamp;
    };

    const handleDateSelected = async ({date}) => {
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
    };
  },
};
</script>

<style scoped>
</style>
