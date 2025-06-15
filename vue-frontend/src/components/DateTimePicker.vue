<template>
  <div class="relative w-full">
    <label class="block mb-1.5 font-semibold text-secondary-light dark:text-secondary-dark" for="datetime-picker">
      Choose Webcam History Time
    </label>
    <div class="flex items-center space-x-2">
      <!-- Previous Date Button -->
      <button
          class="bg-item-secondary-light hover:bg-gray-200 dark:hover:bg-gray-600 dark:bg-item-secondary-dark p-2 border border-secondary-dark dark:border-secondary-light rounded-md text-primary-light dark:text-primary-dark"
          @click="changeDate(-1)"
      >
        <ChevronLeftIcon class="w-4 h-6"/>
      </button>

      <!-- Flatpickr Date Picker -->
      <input
          id="datetime-picker"
          ref="flatpickr"
          v-model="selectedDate"
          class="bg-item-light-bg dark:bg-item-dark-bg p-2 border border-secondary-dark dark:border-secondary-light rounded-md focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 w-32 text-primary-light dark:text-primary-dark"
          placeholder="Select Date"
          type="text"
      />

      <!-- Next Date Button -->
      <button
          class="bg-item-secondary-light hover:bg-gray-200 dark:hover:bg-gray-600 dark:bg-item-secondary-dark p-2 border border-secondary-dark dark:border-secondary-light rounded-md text-primary-light dark:text-primary-dark"
          @click="changeDate(1)"
      >
        <ChevronRightIcon class="w-4 h-6"/>
      </button>

      <!-- Time picker select -->
      <select v-model="selectedTime"
              :disabled="!Object.keys(availableTimes).length"
              class="bg-item-light-bg dark:bg-item-dark-bg p-2 border border-gray-300 dark:border-gray-600 rounded-md focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 w-32 text-primary-light dark:text-primary-dark">
        <option v-for="(timestamp, time) in availableTimes" :key="time" :value="time">
          {{ time }}
        </option>
        <option v-if="!Object.keys(availableTimes).length" disabled>No available times</option>
      </select>
    </div>

    <!-- Error message display -->
    <p v-if="errorMessage" class="mt-2 text-red-500 dark:text-red-400 text-sm">{{ errorMessage }}</p>
  </div>
</template>

<script>
import flatpickr from 'flatpickr'; // Import Flatpickr
import 'flatpickr/dist/flatpickr.min.css'; // Import Flatpickr styles
import 'flatpickr/dist/themes/dark.css';
import {ChevronLeftIcon, ChevronRightIcon} from "@heroicons/vue/24/outline";
import { API_URL } from '@/config';

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
        const response = await fetch(`${API_URL}/api/webcams/${this.webcamId}/history?date=${date}&times=true`);
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
