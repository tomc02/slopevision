<template>
  <div>
    <WebcamDisplay :placeId="placeId" :placeName="placeName" />
  </div>
</template>

<script>
import WebcamDisplay from "../components/WebcamDisplay.vue";
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
export default {
  name: "PlaceDetail",
  components: { WebcamDisplay },
  setup() {
    const route = useRoute();
    const placeId = ref(route.params.id);
    const placeName = ref("");

    const fetchPlaceDetails = async () => {
      const response = await fetch(`/api/places/${placeId.value}`); // Replace with actual API
      const data = await response.json();
      placeName.value = data.name;
    };

    onMounted(fetchPlaceDetails);

    return {
      placeId,
      placeName,
    };
  },
};
</script>
