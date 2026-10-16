<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { api, formatJam, formatTanggal, formatRupiah } from '../api'
import { useBooking } from '../stores/booking'

const router = useRouter()
const bookingStore = useBooking()

const movies = ref<any[]>([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const response = await api.get('/movies')
    movies.value = response.data
  } catch (e) {
    error.value = 'Gagal memuat daftar film. Pastikan backend sudah berjalan.'
  } finally {
    loading.value = false
  }
})

const selectMovie = (movie: any) => {
  if (!movie.showtime) return
  bookingStore.resetBooking()
  bookingStore.movie = movie
  bookingStore.showtime = movie.showtime
  router.push(`/showtimes/${movie.showtime.id}/seats`)
}
</script>

<template>
  <div class="space-y-6">
    <div class="border-b border-white/10 pb-4">
      <h1 class="text-2xl font-bold border-l-4 border-red-500 pl-3">Daftar Film</h1>
      <p class="text-sm text-gray-400 mt-1 pl-4">Pilih film favorit Anda untuk memilih tempat duduk.</p>
    </div>
    
    <div v-if="loading" class="text-gray-400 animate-pulse py-12 text-center">Memuat film...</div>
    <div v-else-if="error" class="bg-red-500/20 text-red-400 p-4 rounded-xl border border-red-500/50">{{ error }}</div>
    <div v-else-if="!movies.length" class="text-gray-400 text-center py-12">Belum ada film yang tersedia saat ini.</div>
    
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <div 
        v-for="movie in movies" 
        :key="movie.id" 
        class="bg-[#1A1D27] rounded-2xl overflow-hidden border border-white/5 flex flex-col justify-between hover:border-white/20 transition-all duration-300 shadow-lg"
      >
        <div class="aspect-[16/9] overflow-hidden bg-gray-800 relative">
          <img 
            :src="movie.poster_url" 
            :alt="movie.title" 
            class="w-full h-full object-cover" 
          />
          <div class="absolute bottom-2 left-2 bg-black/80 px-2 py-0.5 rounded text-xs font-medium text-gray-300">
            {{ movie.duration_minutes }} Menit
          </div>
        </div>

        <div class="p-5 flex-1 flex flex-col justify-between space-y-4">
          <div>
            <h2 class="font-bold text-lg text-white" :title="movie.title">{{ movie.title }}</h2>
            <p class="text-xs text-gray-400 mt-1">{{ movie.genre }}</p>
          </div>

          <div class="bg-[#0F1117] p-3 rounded-xl border border-white/5 space-y-1 text-xs text-gray-300">
            <span class="text-[11px] text-gray-400 uppercase tracking-wider block font-semibold">Jadwal Penayangan:</span>
            <div v-if="movie.showtime" class="space-y-0.5">
              <p class="text-white font-medium">
                {{ formatTanggal(movie.showtime.start_time) }}, {{ formatJam(movie.showtime.start_time) }} WIB
              </p>
              <p class="text-gray-400">
                {{ movie.showtime.studio }} &bull; <span class="text-red-400 font-semibold">{{ formatRupiah(movie.showtime.price) }}</span>
              </p>
            </div>
            <div v-else class="text-gray-500 italic">Jadwal belum tersedia</div>
          </div>

          <button 
            @click="selectMovie(movie)"
            :disabled="!movie.showtime"
            class="w-full py-2.5 bg-red-600 hover:bg-red-700 disabled:bg-gray-700 text-white rounded-xl font-semibold transition-colors text-sm shadow-md shadow-red-600/20 flex items-center justify-center gap-1.5"
          >
            Pilih Film
          </button>
        </div>
      </div>
    </div>
  </div>
</template>