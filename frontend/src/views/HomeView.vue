<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { api, formatJam, formatRupiah } from '../api'
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

const selectShowtime = (movie: any, showtime: any) => {
  bookingStore.resetBooking()
  bookingStore.movie = movie
  bookingStore.showtime = showtime
  router.push(`/showtimes/${showtime.id}/seats`)
}
</script>

<template>
  <div class="space-y-6">
    <div class="border-b border-white/10 pb-4">
      <h1 class="text-2xl font-bold border-l-4 border-red-500 pl-3">Pilih Film Favorit</h1>
      <p class="text-sm text-gray-400 mt-1 pl-4">Pilih film dan jadwal untuk langsung memesan kursi.</p>
    </div>
    
    <div v-if="loading" class="text-gray-400 animate-pulse py-12 text-center">Memuat film...</div>
    <div v-else-if="error" class="bg-red-500/20 text-red-400 p-4 rounded-xl border border-red-500/50">{{ error }}</div>
    <div v-else-if="!movies.length" class="text-gray-400 text-center py-12">Belum ada film yang tersedia saat ini.</div>
    
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <div 
        v-for="movie in movies" 
        :key="movie.id" 
        class="bg-[#1A1D27] rounded-2xl overflow-hidden border border-white/5 flex flex-col hover:border-white/20 transition-all duration-300 shadow-lg"
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
          </div>

          <!-- Pilihan Jadwal Tayang Langsung -->
          <div class="space-y-2">
            <span class="text-xs text-gray-400 uppercase tracking-wider block font-medium">Jadwal Tayang:</span>
            
            <div v-if="movie.showtimes?.length" class="flex flex-wrap gap-2">
              <button 
                v-for="st in movie.showtimes" 
                :key="st.id"
                @click="selectShowtime(movie, st)"
                class="bg-[#0F1117] hover:bg-red-600 border border-white/10 hover:border-red-500 px-3 py-2 rounded-xl text-left transition-colors group/btn"
              >
                <div class="font-bold text-sm text-white group-hover/btn:text-white">{{ formatJam(st.start_time) }}</div>
                <div class="text-[11px] text-gray-400 group-hover/btn:text-white/80">{{ st.studio }} &bull; {{ formatRupiah(st.price) }}</div>
              </button>
            </div>
            
            <div v-else class="text-xs text-gray-500 italic">
              Tidak ada jadwal tayang aktif.
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>