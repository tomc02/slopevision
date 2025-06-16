<template>
  <div>
    <PlaceOverview :showOnlyFavorites="false" />
  </div>
</template>

<script>
import PlaceOverview from "@/components/PlaceOverview.vue";

export default {
  name: "LiveWebcams",
  components: {
    PlaceOverview,
  },
};
</script>
