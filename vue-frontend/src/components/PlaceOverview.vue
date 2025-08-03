<template>
	<div
		class="">
		<div class="mx-auto px-4 sm:px-6 lg:px-8 py-8 container">
			<div class="mb-8">
				<div class="mb-0 text-center">
					<h1
						class="bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600 mb-4 font-bold text-transparent text-4xl">
						Discover Places
					</h1>

				</div>

				<!-- Controls Bar -->
				<div
					class="bg-white/80 dark:bg-gray-800/80 shadow-xl backdrop-blur-md px-6 py-4 border border-gray-200 dark:border-gray-700 rounded-2xl">
					<div class="flex lg:flex-row flex-col justify-between items-center gap-4">
						<!-- Stats and Filter Toggle -->
						<div class="flex items-center gap-6">
							<div class="text-center">
								<div class="font-bold text-indigo-600 dark:text-indigo-400 text-2xl">
									{{ filteredPlaces.length }}
								</div>
								<div class="text-gray-500 dark:text-gray-400 text-sm">Places</div>
							</div>

							<div class="bg-gray-300 dark:bg-gray-600 w-px h-8"></div>

							<button @click="showFilters = !showFilters" :class="{
								'bg-indigo-100 dark:bg-indigo-900/30 text-indigo-600 dark:text-indigo-400': showFilters,
								'text-gray-600 dark:text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400 hover:bg-gray-50 dark:hover:bg-gray-700/50': !showFilters
							}" class="flex items-center gap-3 px-4 py-2 rounded-xl font-medium transition-all duration-200">
								<FunnelIcon class="w-5 h-5" />
								<span>Filters</span>
								<div v-if="activeFiltersCount > 0"
									class="flex justify-center items-center bg-orange-500 rounded-full w-6 h-6 font-bold text-white text-xs animate-pulse">
									{{ activeFiltersCount }}
								</div>
							</button>
							<div v-if="activeFiltersCount > 0">
							<button @click="resetFilters"
								class="hover:bg-red-50 dark:hover:bg-red-900/20 px-6 py-2 rounded-xl font-medium text-gray-600 hover:text-red-600 dark:hover:text-red-400 dark:text-gray-400 transition-all duration-200">
								🔄 Reset Filters
							</button>
							</div>
						</div>

						<!-- View Controls -->
						<div class="flex items-center gap-3">
													<!-- Sort Options Row -->
						<div class="border-gray-200 dark:border-gray-700">
							<div class="flex sm:flex-row flex-col justify-between items-start sm:items-center gap-4">
								<div class="w-full sm:w-auto">
									<select v-model="sortOption" class="filter-select sm:w-auto">
										<option value="name-asc">📝 Name (A-Z)</option>
										<option value="name-desc">📝 Name (Z-A)</option>
										<option value="country-asc">🌍 Country (A-Z)</option>
										<option value="range-asc">🏔️ Range (A-Z)</option>
									</select>
								</div>
							</div>
						</div>
							<div class="flex bg-gray-100 dark:bg-gray-700 p-1 rounded-xl">
								<button @click="viewMode = 'grid'" :class="{
									'bg-white dark:bg-gray-600 text-indigo-600 dark:text-indigo-400 shadow-sm': viewMode === 'grid',
									'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300': viewMode !== 'grid'
								}" class="p-2 rounded-lg transition-all duration-200">
									<Squares2X2Icon class="w-5 h-5" />
								</button>
								<button @click="viewMode = 'list'" :class="{
									'bg-white dark:bg-gray-600 text-indigo-600 dark:text-indigo-400 shadow-sm': viewMode === 'list',
									'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300': viewMode !== 'list'
								}" class="p-2 rounded-lg transition-all duration-200">
									<ListBulletIcon class="w-5 h-5" />
								</button>
							</div>
						</div>
					</div>
				</div>
			</div>

			<!-- Filter Panel -->
			<transition enter-active-class="transition ease-out duration-300"
				enter-from-class="transform opacity-0 scale-95" enter-to-class="transform opacity-100 scale-100"
				leave-active-class="transition ease-in duration-200" leave-from-class="transform opacity-100 scale-100"
				leave-to-class="transform opacity-0 scale-95">
				<div v-if="showFilters" class="mb-8">
					<div
						class="bg-white/90 dark:bg-gray-800/90 shadow-xl backdrop-blur-md p-6 border border-gray-200 dark:border-gray-700 rounded-2xl">
						<div class="gap-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5">
							<!-- Search -->
							<div class="xl:col-span-2">
								<label class="block mb-2 font-semibold text-gray-700 dark:text-gray-300 text-sm">
									Search Places
								</label>
								<div class="relative">
									<input v-model="searchQuery"
										class="bg-gray-50 dark:bg-gray-700 px-4 py-2 pl-10 border border-gray-200 dark:border-gray-600 focus:border-transparent rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 w-full text-gray-900 dark:text-gray-100 transition-all duration-200 placeholder-gray-500 dark:placeholder-gray-400"
										placeholder="Search by name, location, or description..." type="text" />
									<svg class="top-1/2 left-3 absolute w-5 h-5 text-gray-400 -translate-y-1/2 transform"
										fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
											d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
									</svg>
								</div>
							</div>

							<!-- Favorites -->
							<div>
								<label class="block mb-2 font-semibold text-gray-700 dark:text-gray-300 text-sm">
									Favorites
								</label>
								<select v-model="favoritesFilter" class="filter-select">
									<option :value="null">All places</option>
									<option value="favorites">💖 Only favorites</option>
									<option value="non-favorites">Discover new</option>
								</select>
							</div>

							<!-- Country -->
							<div>
								<label class="block mb-2 font-semibold text-gray-700 dark:text-gray-300 text-sm">
									Country
								</label>
								<select v-model="selectedCountry" class="filter-select"
									@change="selectedMountainRange = null">
									<option :value="null">🌍 All countries</option>
									<option v-for="country in availableCountries" :key="country" :value="country">
										{{ country }}
									</option>
								</select>
							</div>

							<!-- Mountain Range -->
							<div>
								<label class="block mb-2 font-semibold text-gray-700 dark:text-gray-300 text-sm">
									Mountain Range
								</label>
								<select v-model="selectedMountainRange" class="filter-select"
									:disabled="!selectedCountry">
									<option :value="null">🏔️ All ranges</option>
									<option v-for="range in availableMountainRanges" :key="range" :value="range">
										{{ range }}
									</option>
								</select>
							</div>
						</div>
					</div>
				</div>
			</transition>

			<!-- No Results State -->
			<div v-if="filteredPlaces.length === 0" class="flex flex-col justify-center items-center py-20">
				<div v-if="loading" class="flex flex-col items-center text-center">
					<div class="relative">
						<div
							class="border-4 border-indigo-200 dark:border-indigo-800 rounded-full w-16 h-16 animate-spin">
						</div>
						<div
							class="top-0 left-0 absolute border-4 border-t-indigo-600 border-transparent rounded-full w-16 h-16 animate-spin">
						</div>
					</div>
					<p class="mt-4 text-gray-600 dark:text-gray-400 text-lg">Loading places...</p>
				</div>
				<div v-else class="max-w-md text-center">
					<div
						class="flex justify-center items-center bg-gradient-to-br from-gray-100 dark:from-gray-700 to-gray-200 dark:to-gray-800 mx-auto mb-6 rounded-full w-24 h-24">
						<svg class="w-12 h-12 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor"
							viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
								d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
						</svg>
					</div>
					<h3 class="mb-2 font-semibold text-gray-700 dark:text-gray-300 text-xl">No places found</h3>
					<p class="mb-6 text-gray-500 dark:text-gray-400">Try adjusting your filters or search terms to
						discover more places.</p>
					<button @click="resetFilters"
						class="bg-gradient-to-r from-indigo-500 hover:from-indigo-600 to-purple-600 hover:to-purple-700 shadow-lg hover:shadow-xl px-6 py-3 rounded-xl font-medium text-white hover:scale-105 transition-all duration-200 transform">
						🔄 Reset All Filters
					</button>
				</div>
			</div>


			<!-- Grid View -->
			<div v-if="viewMode === 'grid' && filteredPlaces.length > 0"
				class="gap-6 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-3">
				<router-link v-for="place in filteredPlaces" :key="place.id"
					:to="{ name: 'PlaceDetail', params: { id: place.id } }"
					class="group bg-white dark:bg-gray-800 shadow-lg hover:shadow-2xl border border-gray-200 dark:border-gray-700 rounded-2xl overflow-hidden hover:scale-[1.02] transition-all duration-300 transform">
					<!-- Webcam Container -->
					<div
						class="relative bg-gradient-to-br from-gray-200 dark:from-gray-700 to-gray-300 dark:to-gray-800 aspect-video overflow-hidden">
						<WebcamVideo :altText="place.name" :url="place.first_webcam_url" style="pointer-events: none"
							class="w-full h-full object-cover transition-transform duration-500" />

						<!-- Location Badge -->
						<div class="top-3 left-3 absolute">
							<div
								class="bg-black/70 backdrop-blur-sm px-3 py-1 rounded-full font-medium text-white text-xs">
								{{ place.country }}
							</div>
						</div>

						<!-- Favorite Button -->
						<button
							class="top-3 right-3 absolute flex justify-center items-center bg-white/90 dark:bg-gray-800/90 opacity-0 group-hover:opacity-100 shadow-lg backdrop-blur-sm rounded-full w-10 h-10 hover:scale-110 transition-all duration-200"
							@click.stop.prevent="toggleFavorite(place.id)"
							:aria-label="isFavorite(place.id) ? 'Remove from favorites' : 'Add to favorites'">
							<HeartIcon :class="[
								'w-5 h-5 transition-colors duration-200',
								isFavorite(place.id)
									? 'text-red-500 fill-current'
									: 'text-gray-400 dark:text-gray-500 hover:text-red-500'
							]" />
						</button>

						<!-- Mountain Range Overlay -->
						<div v-if="place.mounain_range"
							class="right-0 bottom-0 left-0 absolute bg-gradient-to-t from-black/80 via-black/40 to-transparent p-4">
							<p class="font-medium text-white text-sm truncate">
								🏔️ {{ place.mounain_range }}
							</p>
						</div>
					</div>

					<!-- Content Area -->
					<div class="p-5">
						<div class="mb-3">
							<h3
								class="mb-1 font-bold text-gray-900 dark:group-hover:text-indigo-400 dark:text-white group-hover:text-indigo-600 text-lg transition-colors duration-200">
								{{ place.name }}
							</h3>
							<p v-if="place.nearest_city"
								class="flex items-center text-gray-500 dark:text-gray-400 text-sm">
								📍 Near {{ place.nearest_city }}
							</p>
						</div>

						<p class="text-gray-600 dark:text-gray-300 text-sm line-clamp-2 leading-relaxed">
							{{ place.description || "Discover this amazing destination with live webcam views." }}
						</p>

						<!-- Action Footer -->
						<div class="mt-4 pt-4 border-gray-100 dark:border-gray-700 border-t">
							<div class="flex justify-between items-center">
								<span class="flex items-center text-gray-500 dark:text-gray-400 text-xs">
									📹 Live webcam
								</span>
								<div
									class="font-medium text-indigo-600 dark:text-indigo-400 text-sm transition-transform group-hover:translate-x-1 duration-200">
									View details →
								</div>
							</div>
						</div>
					</div>
				</router-link>
			</div>

			<!-- List View -->
			<div v-if="viewMode === 'list' && filteredPlaces.length > 0" class="space-y-4">
				<div v-for="place in filteredPlaces" :key="place.id"
					class="group bg-white dark:bg-gray-800 shadow-lg hover:shadow-xl border border-gray-200 dark:border-gray-700 rounded-2xl overflow-hidden transition-all duration-300">
					<router-link :to="{ name: 'PlaceDetail', params: { id: place.id } }"
						class="flex sm:flex-row flex-col">
						<!-- Webcam Thumbnail -->
						<div
							class="relative bg-gradient-to-br from-gray-200 dark:from-gray-700 to-gray-300 dark:to-gray-800 w-full sm:w-80 aspect-video overflow-hidden">
							<WebcamVideo :altText="place.name" :url="place.first_webcam_url"
								style="pointer-events: none"
								class="w-full h-full object-cover transition-transform duration-500" />

							<!-- Country Badge -->
							<div class="top-3 left-3 absolute">
								<div
									class="bg-black/70 backdrop-blur-sm px-3 py-1 rounded-full font-medium text-white text-xs">
									{{ place.country }}
								</div>
							</div>
						</div>

						<!-- Content Area -->
						<div class="flex-1 p-6">
							<div class="flex justify-between items-start h-full">
								<div class="flex-1">
									<div class="mb-3">
										<h3
											class="mb-2 font-bold text-gray-900 dark:group-hover:text-indigo-400 dark:text-white group-hover:text-indigo-600 text-xl transition-colors duration-200">
											{{ place.name }}
										</h3>
										<div
											class="flex flex-wrap items-center gap-3 text-gray-500 dark:text-gray-400 text-sm">
											<span v-if="place.nearest_city" class="flex items-center">
												📍 Near {{ place.nearest_city }}
											</span>
											<span v-if="place.mounain_range" class="flex items-center">
												🏔️ {{ place.mounain_range }}
											</span>
										</div>
									</div>

									<p class="mb-4 text-gray-600 dark:text-gray-300 line-clamp-3 leading-relaxed">
										{{ place.description || "Discover this amazing destination with live webcam views and stunning mountain scenery." }}
									</p>

									<!-- Action Row -->
									<div class="flex justify-between items-center">
										<div class="flex items-center gap-4 text-gray-500 dark:text-gray-400 text-sm">
											<span class="flex items-center">
												📹 Live webcam available
											</span>
										</div>
										<div
											class="font-medium text-indigo-600 dark:text-indigo-400 transition-transform group-hover:translate-x-1 duration-200">
											View details →
										</div>
									</div>
								</div>

								<!-- Favorite Button -->
								<button @click.stop.prevent="toggleFavorite(place.id)"
									class="hover:bg-gray-100 dark:hover:bg-gray-700 ml-4 p-3 rounded-full hover:scale-110 transition-all duration-200"
									:aria-label="isFavorite(place.id) ? 'Remove from favorites' : 'Add to favorites'">
									<HeartIcon :class="[
										'w-6 h-6 transition-colors duration-200',
										isFavorite(place.id)
											? 'text-red-500 fill-current'
											: 'text-gray-400 dark:text-gray-500 hover:text-red-500'
									]" />
								</button>
							</div>
						</div>
					</router-link>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import { computed, onMounted, ref, watch } from "vue";
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
		const loading = ref(false);
		const FILTERS_KEY = 'placeOverview_filters';

		const saveSettings = () => {
			const settings = {
				searchQuery: searchQuery.value,
				favoritesFilter: favoritesFilter.value,
				selectedCountry: selectedCountry.value,
				selectedMountainRange: selectedMountainRange.value,
				sortOption: sortOption.value,
				viewMode: viewMode.value,
				showFilters: showFilters.value
			};
			localStorage.setItem(FILTERS_KEY, JSON.stringify(settings));
		};

		const loadSettings = () => {
			const savedSettings = localStorage.getItem(FILTERS_KEY);
			if (savedSettings) {
				const settings = JSON.parse(savedSettings);
				searchQuery.value = settings.searchQuery || "";
				favoritesFilter.value = settings.favoritesFilter || null;
				selectedCountry.value = settings.selectedCountry || null;
				selectedMountainRange.value = settings.selectedMountainRange || null;
				sortOption.value = settings.sortOption || 'name-asc';
				viewMode.value = settings.viewMode || 'grid';
				showFilters.value = false;
			}
		};

		watch([searchQuery, favoritesFilter, selectedCountry, selectedMountainRange, sortOption, viewMode], saveSettings);

		// watch for ui/dataSaver changes
		watch(() => store.getters['ui/dataSaver'], (newValue) => {
			if (newValue) {
				places.value.forEach(place => {
					place.first_webcam_url = place.latest_webcam_history || place.first_webcam_url;
				});
			} else {
				places.value.forEach(place => {
					place.first_webcam_url = place.live_url;
				});
			}
		});

		const fetchPlaces = async () => {
			try {
				loading.value = true;
				const response = await fetch(`${API_URL}/api/places/`, { method: "GET" });
				const data = await response.json();

				store.dispatch('auth/rehydrateState').then(() => {
					const user = store.getters['auth/currentUser'] || 'User';
					favorites.value = new Set(user.favorite_places?.map(id => id) || []);
				});

				data.forEach(place => {
					place.live_url = place.first_webcam_url;
					if (store.getters['ui/dataSaver']) {
						place.first_webcam_url = place.latest_webcam_history || place.first_webcam_url;
					}
				});

				places.value = data;
				loading.value = false;
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
			saveSettings(); // Also clear from local storage
		};

		onMounted(async () => {
			await fetchPlaces();
			loadSettings();
		});

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
			resetFilters,
			loading,
		};
	},
};
</script>

<style scoped>
.filter-select {
	width: 100%;
	padding: 0.5rem 1rem;
	background-color: rgb(249 250 251);
	border: 1px solid rgb(209 213 219);
	border-radius: 0.75rem;
	outline: none;
	transition: all 0.2s;
	color: rgb(17 24 39);
}

.dark .filter-select {
	background-color: rgb(55 65 81);
	border-color: rgb(75 85 99);
	color: rgb(243 244 246);
}

.filter-select:focus {
	box-shadow: 0 0 0 2px rgb(99 102 241);
	border-color: transparent;
}

.filter-select:disabled {
	opacity: 0.5;
	cursor: not-allowed;
}

/* Custom animations */
@keyframes float {

	0%,
	100% {
		transform: translateY(0px);
	}

	50% {
		transform: translateY(-10px);
	}
}

.float-animation {
	animation: float 3s ease-in-out infinite;
}

/* Transitions */
.transition-all {
	transition-property: all;
	transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
	transition-duration: 300ms;
}

/* Line clamp utility */
.line-clamp-2 {
	overflow: hidden;
	display: -webkit-box;
	-webkit-box-orient: vertical;
	-webkit-line-clamp: 2;
	line-clamp: 2;
}

.line-clamp-3 {
	overflow: hidden;
	display: -webkit-box;
	-webkit-box-orient: vertical;
	-webkit-line-clamp: 3;
	line-clamp: 3;
}

/* Hover effects */
.hover-lift:hover {
	transform: translateY(-4px);
}

/* Backdrop blur fallback */
.backdrop-blur-md {
	backdrop-filter: blur(12px);
}

@supports not (backdrop-filter: blur(12px)) {
	.backdrop-blur-md {
		background-color: rgba(255, 255, 255, 0.9);
	}

	.dark .backdrop-blur-md {
		background-color: rgba(17, 24, 39, 0.9);
	}
}
</style>