<template>
  <div>
    <template v-if="isIframeUrl">
      <iframe
        :src="url"
        allow="autoplay; fullscreen"
        allowfullscreen
        class="w-full aspect-video"
        frameborder="0"
      ></iframe>
    </template>

    <template v-else-if="isVideoUrl">
      <video
        :src="url"
        autoplay
        :controls="controls"
        loop
        muted
        class="w-full object-cover aspect-video"
      ></video>
    </template>

    <template v-else>
      <img
        :src="url"
        :alt="altText"
        class="w-full object-cover aspect-video"
      />
    </template>
  </div>
</template>

<script>
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
