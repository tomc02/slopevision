<template>
  <div>
    <template v-if="isIframeUrl">
      <iframe :src="url" allow="autoplay; fullscreen" allowfullscreen class="w-full aspect-video"
              frameborder="0"></iframe>
    </template>
    <template v-else-if="isVideoUrl">
      <video :src="url" autoplay class="w-full object-cover aspect-video" controls loop muted></video>
    </template>
    <template v-else>
      <img :alt="altText" :src="url" class="w-full object-cover aspect-video"/>
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
      const videoExtensions = /(mp4|webm|ogg)/i; // Remove the anchoring `^` and `$`
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
    url(newUrl) {
      this.updateDisplayType(newUrl);
    }
  },
  mounted() {
    this.updateDisplayType(this.url);
  },
};
</script>
