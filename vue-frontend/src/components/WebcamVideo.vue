<template>
  <div>
    <template v-if="isIframeUrl">
      <iframe
        :src="computedUrl"
        allow="autoplay; fullscreen"
        allowfullscreen
        class="w-full aspect-video"
        frameborder="0"
      ></iframe>
    </template>

    <template v-else-if="isVideoUrl">
      <video
        :src="computedUrl"
        autoplay
        :controls="controls"
        loop
        muted
        class="w-full object-cover aspect-video"
      ></video>
    </template>

    <template v-else>
      <img
        :src="computedUrl"
        :alt="altText"
        class="w-full object-cover aspect-video"
      />
    </template>
  </div>
</template>

<script>
import { API_URL } from '@/config';
export default {
  props: {
    url: {
      type: String,
      required: true
    },
    altText: {
      type: String,
      default: ''
    },
    controls: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      isVideoUrl: false,
      isIframeUrl: false
    };
  },
  computed: {
    computedUrl() {
      if (this.url.includes('meteo.hzs.sk')) {
        return `${API_URL}/api/proxy-image/?url=${encodeURIComponent(this.url)}`;
      }
      return this.url;
    }
  },
  methods: {
    isVideo(url) {
      const videoExtensions = /\.(mp4|webm|ogg)(\?.*)?$/i;
      return videoExtensions.test(url) || url.includes('rtsp.me');
    },
    isIframe(url) {
      const iframePatterns = /(embed|iframe|video\.itcom)/i;
      return iframePatterns.test(url);
    },
    updateDisplayType(url) {
      this.isVideoUrl = this.isVideo(url);
      this.isIframeUrl = this.isIframe(url);
    }
  },
  watch: {
    url: {
      immediate: true,
      handler(newUrl) {
        this.updateDisplayType(newUrl);
      }
    }
  }
};
</script>
