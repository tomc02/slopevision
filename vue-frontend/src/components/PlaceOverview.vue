<template>
	<div class="py-8 min-h-fit">
		<div class="mx-auto px-4 container">
			<!-- Page Title and Controls -->
			<div class="flex md:flex-row flex-col justify-between items-center gap-4 mb-8">
				<h1 class="font-bold text-3xl">
					Places Overview
					<span v-if="activeFiltersCount > 0" class="font-normal text-gray-500 dark:text-gray-400 text-sm">
						({{ filteredPlaces.length }} results)
					</span>
				</h1>

				<div class="flex items-center gap-2">
					<button @click="showFilters = !showFilters"
						class="flex items-center gap-2 bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:hover:bg-gray-700 px-4 py-2 rounded-lg transition">
						<FunnelIcon class="w-5 h-5" />
						<span>Filters</span>
						<span v-if="activeFiltersCount > 0"
							class="flex justify-center items-center bg-indigo-500 rounded-full w-5 h-5 text-white text-xs">
							{{ activeFiltersCount }}
						</span>
					</button>

					<button @click="toggleViewMode"
						class="hover:bg-gray-200 dark:hover:bg-gray-700 p-2 rounded-lg transition">
						<Squares2X2Icon v-if="viewMode === 'grid'" class="w-5 h-5" />
						<ListBulletIcon v-else class="w-5 h-5" />
					</button>
				</div>
			</div>

			<!-- Filter Panel -->
			<transition name="slide-down">
				<div v-if="showFilters" class="bg-gray-50 dark:bg-gray-800 shadow-sm mb-6 p-4 rounded-lg">
					<div class="gap-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4">
						<!-- Search -->
						<div class="md:col-span-2 lg:col-span-4">
							<label class="block mb-1 font-medium text-sm">Search</label>
							<input v-model="searchQuery"
								class="dark:bg-gray-800 p-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 w-full dark:text-gray-100"
								placeholder="Search places..." type="text" />
						</div>

						<!-- Favorites -->
						<div>
							<label class="block mb-1 font-medium text-sm">Favorites</label>
							<select v-model="favoritesFilter" class="filter-select">
								<option :value="null">All places</option>
								<option value="favorites">Only favorites</option>
								<option value="non-favorites">Non-favorites</option>
							</select>
						</div>

						<!-- Country -->
						<div>
							<label class="block mb-1 font-medium text-sm">Country</label>
							<select v-model="selectedCountry" class="filter-select"
								@change="selectedMountainRange = null">
								<option :value="null">All countries</option>
								<option v-for="country in availableCountries" :key="country" :value="country">
									{{ country }}
								</option>
							</select>
						</div>

						<!-- Mountain Range -->
						<div>
							<label class="block mb-1 font-medium text-sm">Mountain Range</label>
							<select v-model="selectedMountainRange" class="filter-select" :disabled="!selectedCountry">
								<option :value="null">All ranges</option>
								<option v-for="range in availableMountainRanges" :key="range" :value="range">
									{{ range }}
								</option>
							</select>
						</div>

						<!-- Sort Options -->
						<div>
							<label class="block mb-1 font-medium text-sm">Sort by</label>
							<select v-model="sortOption" class="filter-select">
								<option value="name-asc">Name (A-Z)</option>
								<option value="name-desc">Name (Z-A)</option>
								<option value="country-asc">Country (A-Z)</option>
								<option value="range-asc">Range (A-Z)</option>
							</select>
						</div>
					</div>

					<div class="flex justify-end mt-4">
						<button @click="resetFilters"
							class="px-4 py-2 text-gray-600 hover:text-gray-800 dark:hover:text-gray-100 dark:text-gray-300 text-sm transition">
							Reset all filters
						</button>
					</div>
				</div>
			</transition>

			<!-- No Results Message -->
			<div v-if="filteredPlaces.length === 0" class="py-12 text-center">
				<p class="text-gray-500 dark:text-gray-400">No places match your filters.</p>
				<button @click="resetFilters"
					class="mt-2 px-4 py-2 text-indigo-600 hover:text-indigo-800 dark:hover:text-indigo-300 dark:text-indigo-400 transition">
					Reset filters
				</button>
			</div>

			<!-- Grid View -->
			<div v-if="viewMode === 'grid' && filteredPlaces.length > 0"
				class="gap-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-3">
				<router-link v-for="place in filteredPlaces" :key="place.id"
					:to="{ name: 'PlaceDetail', params: { id: place.id } }"
					class="group relative bg-item-light-bg dark:bg-item-dark-bg shadow-lg rounded-lg overflow-hidden hover:scale-[1.02] transition-transform transform">
					<!-- Webcam with loading state -->
					<div class="relative bg-gray-200 dark:bg-gray-700 aspect-video overflow-hidden">
						<WebcamVideo :altText="place.name" :url="place.first_webcam" style="pointer-events: none" />
						<div v-if="place.country || place.mounain_range"
							class="right-0 bottom-0 left-0 absolute bg-gradient-to-t from-black/70 to-transparent p-2">
							<p class="text-white text-xs truncate">
								{{ place.mounain_range }}{{ place.country ? `, ${place.country}` : '' }}
							</p>
						</div>
					</div>

					<!-- Place Details -->
					<div class="p-4">
						<div class="flex justify-between items-start">
							<h2 class="font-semibold text-primary-light dark:text-primary-dark text-xl">
								{{ place.name }}
								<span v-if="place.nearest_city"
									class="block font-normal text-gray-500 dark:text-gray-400 text-sm">
									Near {{ place.nearest_city }}
								</span>
							</h2>
							<span class="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded text-xs">
								{{ place.country }}
							</span>
						</div>
						<p class="mt-2 text-secondary-light dark:text-secondary-dark text-sm line-clamp-3">
							{{ place.description || "No description available." }}
						</p>
					</div>

					<!-- Favorite Button -->
					<button
						class="top-4 right-4 absolute flex justify-center items-center bg-white/90 dark:bg-gray-800/90 opacity-0 group-hover:opacity-100 shadow-md border border-gray-200 dark:border-gray-700 rounded-full w-8 h-8 transition-opacity"
						@click.stop.prevent="toggleFavorite(place.id)"
						:aria-label="isFavorite(place.id) ? 'Remove from favorites' : 'Add to favorites'">
						<HeartIcon :class="[
							'w-5 h-5',
							isFavorite(place.id) ? 'text-red-500 fill-current' : 'text-gray-400 dark:text-gray-500 fill-none stroke-2'
						]" />
					</button>
				</router-link>
			</div>

			<!-- List View -->
			<div v-if="viewMode === 'list' && filteredPlaces.length > 0" class="space-y-2">
				<div v-for="place in filteredPlaces" :key="place.id"
					class="bg-item-light-bg dark:bg-item-dark-bg hover:shadow-md rounded-lg overflow-hidden transition-shadow">
					<router-link :to="{ name: 'PlaceDetail', params: { id: place.id } }" class="flex">
						<!-- Webcam thumbnail -->
						<div class="relative bg-gray-200 dark:bg-gray-700 w-1/3 min-w-[120px] aspect-video">
							<WebcamVideo :altText="place.name" :url="place.first_webcam" style="pointer-events: none" />
						</div>

						<!-- Place details -->
						<div class="flex flex-col flex-1 p-4">
							<div class="flex justify-between items-start">
								<div>
									<h2 class="font-semibold text-primary-light dark:text-primary-dark text-lg">
										{{ place.name }}
										<span v-if="place.nearest_city"
											class="block font-normal text-gray-500 dark:text-gray-400 text-sm">
											Near {{ place.nearest_city }}
										</span>
									</h2>
									<p class="mt-1 text-secondary-light dark:text-secondary-dark text-sm line-clamp-2">
										{{ place.description || "No description available." }}
									</p>
								</div>
								<div class="flex items-center gap-2">
									<span
										class="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded text-xs whitespace-nowrap">
										{{ place.country }}
									</span>
									<button @click.stop.prevent="toggleFavorite(place.id)"
										class="hover:bg-gray-200 dark:hover:bg-gray-700 p-1 rounded-full transition"
										:aria-label="isFavorite(place.id) ? 'Remove from favorites' : 'Add to favorites'">
										<HeartIcon :class="[
											'w-5 h-5',
											isFavorite(place.id) ? 'text-red-500 fill-current' : 'text-gray-400 dark:text-gray-500 fill-none stroke-2'
										]" />
									</button>
								</div>
							</div>

							<div class="flex flex-wrap gap-2 mt-auto pt-2">
								<span v-if="place.mounain_range"
									class="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded text-xs">
									{{ place.mounain_range }}
								</span>
							</div>
						</div>
					</router-link>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import { computed, onMounted, ref } from "vue";
import WebcamVideo from "@/components/WebcamVideo.vue";
import {
	HeartIcon,
	FunnelIcon,
	Squares2X2Icon,
	ListBulletIcon
} from '@heroicons/vue/24/outline';
import { API_URL } from '@/config';
import api from "@/services/api";
import store from '../store';

export default {
	name: "PlaceOverview",
	components: {
		WebcamVideo,
		HeartIcon,
		FunnelIcon,
		Squares2X2Icon,
		ListBulletIcon
	},
	setup() {
		const places = ref([]);
		const searchQuery = ref("");
		const favorites = ref(new Set());
		const showFilters = ref(false);
		const viewMode = ref('grid'); // 'grid' or 'list'

		// Filter states
		const favoritesFilter = ref(null);
		const selectedCountry = ref(null);
		const selectedMountainRange = ref(null);
		const sortOption = ref('name-asc');

		const fetchPlaces = async () => {
			try {
				const response = await fetch(`${API_URL}/api/places/`, { method: "GET" });
				const data = await response.json();

				store.dispatch('auth/rehydrateState').then(() => {
					const user = store.getters['auth/currentUser'] || 'User';
					favorites.value = new Set(user.favorite_places?.map(id => id) || []);
				});


				places.value = data;
				console.log("Fetched places:", places.value);
			} catch (error) {
				console.error("Error fetching places:", error);
			}
		};

		// Computed properties for filter options
		const availableCountries = computed(() => {
			const countries = new Set();
			places.value.forEach(place => {
				if (place.country) countries.add(place.country);
			});
			return Array.from(countries).sort();
		});

		const availableMountainRanges = computed(() => {
			const ranges = new Set();
			places.value.forEach(place => {
				if (place.mounain_range && (!selectedCountry.value || place.country === selectedCountry.value)) {
					ranges.add(place.mounain_range);
				}
			});
			return Array.from(ranges).sort();
		});

		// Active filters count for badge
		const activeFiltersCount = computed(() => {
			let count = 0;
			if (searchQuery.value) count++;
			if (favoritesFilter.value) count++;
			if (selectedCountry.value) count++;
			if (selectedMountainRange.value) count++;
			if (sortOption.value !== 'name-asc') count++;
			return count;
		});

		// Main filtered places computation
		const filteredPlaces = computed(() => {
			let result = [...places.value];

			// Apply search filter
			if (searchQuery.value) {
				const query = searchQuery.value.toLowerCase();
				result = result.filter(place =>
					place.name.toLowerCase().includes(query) ||
					(place.description && place.description.toLowerCase().includes(query)) ||
					(place.nearest_city && place.nearest_city.toLowerCase().includes(query)) ||
					(place.mounain_range && place.mounain_range.toLowerCase().includes(query)) ||
					(place.country && place.country.toLowerCase().includes(query))
				);
			}

			// Apply favorites filter
			if (favoritesFilter.value === 'favorites') {
				result = result.filter(place => isFavorite(place.id));
			} else if (favoritesFilter.value === 'non-favorites') {
				result = result.filter(place => !isFavorite(place.id));
			}

			// Apply country filter
			if (selectedCountry.value) {
				result = result.filter(place => place.country === selectedCountry.value);
			}

			// Apply mountain range filter
			if (selectedMountainRange.value) {
				result = result.filter(place => place.mounain_range === selectedMountainRange.value);
			}

			// Apply sorting
			switch (sortOption.value) {
				case 'name-asc':
					result.sort((a, b) => a.name.localeCompare(b.name));
					break;
				case 'name-desc':
					result.sort((a, b) => b.name.localeCompare(a.name));
					break;
				case 'country-asc':
					result.sort((a, b) => (a.country || '').localeCompare(b.country || ''));
					break;
				case 'range-asc':
					result.sort((a, b) => (a.mounain_range || '').localeCompare(b.mounain_range || ''));
					break;
			}

			return result;
		});

		const toggleFavorite = async (placeId) => {
			const wasFavorite = favorites.value.has(placeId);
			const endpoint = wasFavorite
				? `/api/auth/user/remove-favorites/${placeId}/`
				: `/api/auth/user/add-favorites/${placeId}/`;

			try {
				await api.post(endpoint);
				if (wasFavorite) {
					favorites.value.delete(placeId);
				} else {
					favorites.value.add(placeId);
				}
			} catch (err) {
				console.error(`Error toggling favorite for place ${placeId}:`, err);
			}
		};

		const isFavorite = (placeId) => favorites.value.has(placeId);

		const toggleViewMode = () => {
			viewMode.value = viewMode.value === 'grid' ? 'list' : 'grid';
		};

		const resetFilters = () => {
			searchQuery.value = "";
			favoritesFilter.value = null;
			selectedCountry.value = null;
			selectedMountainRange.value = null;
			sortOption.value = 'name-asc';
		};

		onMounted(fetchPlaces);

		return {
			places,
			searchQuery,
			filteredPlaces,
			toggleFavorite,
			isFavorite,
			showFilters,
			viewMode,
			toggleViewMode,
			favoritesFilter,
			selectedCountry,
			selectedMountainRange,
			availableCountries,
			availableMountainRanges,
			sortOption,
			activeFiltersCount,
			resetFilters
		};
	},
};
</script>

<style scoped>
.filter-select {
	@apply dark:bg-gray-800 p-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 w-full dark:text-gray-100;
}

.slide-down-enter-active,
.slide-down-leave-active {
	transition: all 0.3s ease;
}

.slide-down-enter-from,
.slide-down-leave-to {
	opacity: 0;
	transform: translateY(-10px);
}

button {
	transition: transform 0.2s ease-in-out;
}

button:hover {
	transform: scale(1.05);
}
</style>