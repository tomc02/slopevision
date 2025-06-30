<template>
  <div class="bg-white dark:bg-gray-800 shadow-lg p-4 rounded-xl min-w-[220px] max-w-[280px] font-sans text-sm">
    <div class="mb-1 font-semibold text-gray-800 dark:text-white text-base">
      {{ place.name }}
    </div>
    <div class="mb-2 text-gray-500 dark:text-gray-400 text-sm">
      {{ place.country }}<span v-if="place.mounain_range">, {{ place.mounain_range }}</span>
    </div>

    <div class="mb-3 border border-gray-200 dark:border-gray-700 rounded-lg aspect-video overflow-hidden">
      <WebcamVideo
        :url="place.latest_webcam_history"
        :altText="place.name"
        class="w-full h-full object-cover"
      />
    </div>

    <div class="mb-3 text-gray-600 dark:text-gray-300 leading-snug">
      {{ shortDescription }}
    </div>

    <div class="text-right">
      <a
        :href="'/place/' + place.id"
        class="font-medium text-indigo-600 dark:text-indigo-400 text-sm hover:underline"
      >
        View details →
      </a>
    </div>
  </div>
</template>

<script setup>
import WebcamVideo from '@/components/WebcamVideo.vue'
import { computed } from 'vue'
defineProps({
  place: {
    type: Object,
    required: true,
  },
})
const shortDescription = computed(() => {
   return ''
})
</script>
