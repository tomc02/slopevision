<template>
  <div class="relative w-full">
    <label class="block text-secondary-light dark:text-secondary-dark font-semibold mb-1.5" for="datetime-picker">
      Choose Webcam History Time
    </label>
    <div class="flex items-center space-x-2">
      <!-- Previous Date Button -->
      <button
          class="border border-secondary-dark dark:border-secondary-light rounded-md p-2 text-primary-light dark:text-primary-dark bg-item-secondary-light dark:bg-item-secondary-dark hover:bg-gray-200 dark:hover:bg-gray-600"
          @click="changeDate(-1)"
      >
        <ChevronLeftIcon class="w-4 h-6"/>
      </button>

      <!-- Flatpickr Date Picker -->
      <input
          id="datetime-picker"
          ref="flatpickr"
          v-model="selectedDate"
          class="border border-secondary-dark dark:border-secondary-light rounded-md p-2 text-primary-light dark:text-primary-dark bg-item-light-bg dark:bg-item-dark-bg w-32 focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400"
          placeholder="Select Date"
          type="text"
      />

      <!-- Next Date Button -->
      <button
          class="border border-secondary-dark dark:border-secondary-light rounded-md p-2 text-primary-light dark:text-primary-dark bg-item-secondary-light dark:bg-item-secondary-dark hover:bg-gray-200 dark:hover:bg-gray-600"
          @click="changeDate(1)"
      >
        <ChevronRightIcon class="w-4 h-6"/>
      </button>

      <!-- Time picker select -->
      <select v-model="selectedTime"
              :disabled="!Object.keys(availableTimes).length"
              class="border border-gray-300 dark:border-gray-600 rounded-md p-2 text-primary-light dark:text-primary-dark bg-item-light-bg dark:bg-item-dark-bg w-32 focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400">
        <option v-for="(timestamp, time) in availableTimes" :key="time" :value="time">
          {{ time }}
        </option>
        <option v-if="!Object.keys(availableTimes).length" disabled>No available times</option>
      </select>
    </div>

    <!-- Error message display -->
    <p v-if="errorMessage" class="text-red-500 dark:text-red-400 text-sm mt-2">{{ errorMessage }}</p>
  </div>
</template>

<script>
import flatpickr from 'flatpickr'; // Import Flatpickr
import 'flatpickr/dist/flatpickr.min.css'; // Import Flatpickr styles
import 'flatpickr/dist/themes/dark.css';
import {ChevronLeftIcon, ChevronRightIcon} from "@heroicons/vue/24/outline";

export default {
  components: {ChevronLeftIcon, ChevronRightIcon},
  props: {
    webcamId: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      selectedDate: '', // Automatically set in the mounted hook
      selectedTime: '',
      availableTimes: {}, // This will now store times and their timestamps from the API
      errorMessage: '',
    };
  },
  methods: {
    async fetchAvailableTimes(date) {
      this.availableTimes = {};
      try {
        const response = await fetch(`/api/webcams/${this.webcamId}/history?date=${date}&times=true`);
        const data = await response.json();
        if (Object.keys(data).length) {
          this.availableTimes = data;
          this.errorMessage = '';
        } else {
          this.availableTimes = {};
          this.errorMessage = 'No available times for the selected date.';
        }
      } catch (error) {
        this.errorMessage = 'Error fetching available times.';
      }
    },
    onDateChange(selectedDates) {
      if (selectedDates.length) {
        this.selectedDate = selectedDates[0].toISOString().split('T')[0]; // Update selectedDate
        this.fetchAvailableTimes(this.selectedDate);
        this.selectedTime = ''; // Reset selected time when date changes
        if (this.selectedDate) {
          this.$emit('date-selected', {date: this.selectedDate});
        }
      }
    },
    onTimeSelected() {
      if (this.selectedDate && this.selectedTime) {
        const timestamp = this.availableTimes[this.selectedTime];
        if (timestamp) {
          this.$emit('date-time-selected', {timestamp});
        }
      }
    },
    reset() {
      this.selectedDate = '';
      this.selectedTime = '';
      this.availableTimes = {};
      this.errorMessage = '';
    },
    getTodayDate() {
      const today = new Date();
      return today.toISOString().split('T')[0]; // Format: YYYY-MM-DD
    },
    setToday() {
      this.selectedDate = this.getTodayDate();
      this.fetchAvailableTimes(this.selectedDate);
      this.selectedTime = ''; // Reset selected time when date changes
      if (this.selectedDate) {
        this.$emit('date-selected', {date: this.selectedDate});
      }
    },
    changeDate(days) {
      if (this.selectedDate) {
        const currentDate = new Date(this.selectedDate);
        currentDate.setDate(currentDate.getDate() + days);
        this.selectedDate = currentDate.toISOString().split('T')[0];
        this.fetchAvailableTimes(this.selectedDate);
        this.selectedTime = '';
        if (this.selectedDate) {
          this.$emit('date-selected', {date: this.selectedDate});
        }
      }
    },
  },
  mounted() {
    this.setToday();
    // Initialize Flatpickr with dark theme
    flatpickr(this.$refs.flatpickr, {
      dateFormat: 'Y-m-d',
      onChange: this.onDateChange, // Update selectedDate when a new date is picked
      mode: 'single', // Only allow one date to be selected
      theme: 'dark', // This will apply the dark theme from Flatpickr
    });
  },
  watch: {
    webcamId(newId, oldId) {
      if (newId !== oldId) {
        this.reset(); // Clear the current state
        this.setToday(); // Reload with the new webcam ID
      }
    },
    selectedDate(newValue) {
      if (newValue) {
        this.fetchAvailableTimes(newValue);
      }
    },
    selectedTime(newValue) {
      if (newValue) {
        this.onTimeSelected();
      }
    },
  },
};
</script>

<style scoped>
</style>
