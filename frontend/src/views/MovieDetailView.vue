<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api, formatRupiah, formatTanggal, formatJam } from '../api'
import { useBooking } from '../stores/booking'

const route = useRoute()
const router = useRouter()
const bookingStore = useBooking()

const movie = ref<any>(null)
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const response = await api.get(`/movies/${route.params.id}`)
    movie.value = response.data
  } catch (e) {
    error.value = 'Gagal memuat detail film.'
  } finally {
    loading.value = false
  }
})

const groupedShowtimes = computed(() => {
  if (!movie.value?.showtimes) return {}
  const groups: Record<string, any[]> = {}
  movie.value.showtimes.forEach((st: any) => {
    const dateKey = formatTanggal(st.start_time)
    if (!groups[dateKey]) groups[dateKey] = []
    groups[dateKey].push(st)
  })
  return groups
})

const selectShowtime = (showtime: any) => {
  bookingStore.resetBooking()
  bookingStore.movie = movie.value
  bookingStore.showtime = showtime
  router.push(`/showtimes/${showtime.id}/seats`)
}
</script>

<template>
  <div v-if="loading" class="text-gray-400 animate-pulse">Memuat detail film...</div>
  <div v-else-if="error" class="text-red-400">{{ error }}</div>
  
  <div v-else-if="movie" class="space-y-8">
    <div class="flex flex-col md:flex-row gap-8 bg-[#1A1D27] p-6 rounded-2xl">
      <img :src="movie.poster_url" :alt="movie.title" class="w-full md:w-64 rounded-xl shadow-lg aspect-[2/3] object-cover" />
      <div class="flex-1 space-y-4">
        <h1 class="text-3xl font-bold">{{ movie.title }}</h1>
        <div class="flex flex-wrap gap-3 text-sm">
          <span class="bg-white/10 px-3 py-1 rounded-full">{{ movie.genre }}</span>
          <span class="bg-white/10 px-3 py-1 rounded-full">{{ movie.duration_minutes }} Menit</span>
          <span class="bg-red-500/20 text-red-400 border border-red-500/50 px-3 py-1 rounded-full font-semibold">{{ movie.rating }}</span>
        </div>
        <p class="text-gray-400 leading-relaxed">{{ movie.synopsis }}</p>
      </div>
    </div>

    <div class="space-y-6">
      <h2 class="text-xl font-semibold border-l-4 border-red-500 pl-3">Pilih Jadwal Tayang</h2>
      
      <div v-for="(times, date) in groupedShowtimes" :key="date" class="space-y-3">
        <h3 class="text-gray-400 font-medium">{{ date }}</h3>
        <div class="flex flex-wrap gap-4">
          <button 
            v-for="st in times" 
            :key="st.id"
            @click="selectShowtime(st)"
            class="bg-[#1A1D27] hover:bg-red-600 border border-white/10 hover:border-red-500 transition-colors p-3 rounded-lg text-left"
          >
            <div class="font-semibold text-lg">{{ formatJam(st.start_time) }}</div>
            <div class="text-xs text-gray-400">{{ st.studio }}</div>
            <div class="text-sm text-red-400 font-medium mt-1">{{ formatRupiah(st.price) }}</div>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>