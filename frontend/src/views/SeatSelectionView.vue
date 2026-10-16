<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api, formatRupiah, formatJam, formatTanggal } from '../api'
import { useBooking } from '../stores/booking'
import SeatGrid from '../components/SeatGrid.vue'

const route = useRoute()
const router = useRouter()
const store = useBooking()

const seats = ref<any[]>([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  if (!store.showtime) {
    router.push('/')
    return
  }

  try {
    const { data } = await api.get(`/showtimes/${route.params.id}/seats`)
    seats.value = data
  } catch (e) {
    error.value = 'Gagal memuat peta kursi. Coba muat ulang halaman.'
  } finally {
    loading.value = false
  }
})

const lanjutPembayaran = () => {
  if (store.selectedSeats.length > 0) {
    router.push('/payment')
  }
}
</script>

<template>
  <div v-if="loading" class="text-gray-400 animate-pulse text-center mt-10">Memuat peta kursi...</div>
  <div v-else-if="error" class="bg-red-500/20 text-red-400 p-4 rounded-lg text-center">{{ error }}</div>
  
  <div v-else class="grid lg:grid-cols-3 gap-8">
    <div class="lg:col-span-2 bg-[#1A1D27] p-6 rounded-2xl border border-white/5">
      <div class="mb-6">
        <h1 class="text-2xl font-bold">{{ store.movie?.title }}</h1>
        <p class="text-gray-400">{{ store.showtime?.studio }} &bull; {{ formatTanggal(store.showtime?.start_time) }} &bull; {{ formatJam(store.showtime?.start_time) }}</p>
      </div>
      
      <SeatGrid 
        :seats="seats" 
        :selectedIds="store.selectedSeatIds" 
        @toggle="store.toggleSeat" 
      />
    </div>

    <div class="bg-[#1A1D27] p-6 rounded-2xl border border-white/5 h-fit sticky top-24">
      <h2 class="text-xl font-semibold mb-4 border-b border-white/10 pb-4">Ringkasan</h2>
      
      <div class="space-y-4 mb-6">
        <div class="flex justify-between text-gray-400">
          <span>Harga per tiket</span>
          <span class="text-white">{{ formatRupiah(store.showtime?.price || 0) }}</span>
        </div>
        
        <div class="flex justify-between text-gray-400">
          <span>Kursi dipilih (Maks 6)</span>
          <div class="text-right">
            <span v-if="store.selectedSeats.length === 0" class="text-sm">Belum ada</span>
            <div v-else class="flex flex-wrap justify-end gap-1">
              <span v-for="s in store.selectedSeats" :key="s.id" class="bg-red-600 text-white text-xs px-2 py-1 rounded">
                {{ s.row }}{{ s.number }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div class="border-t border-white/10 pt-4 mb-6">
        <div class="flex justify-between items-end">
          <span class="text-gray-400">Total Pembayaran</span>
          <span class="text-2xl font-bold text-red-500">{{ formatRupiah(store.totalPrice) }}</span>
        </div>
      </div>

      <button 
        @click="lanjutPembayaran"
        :disabled="store.selectedSeats.length === 0"
        class="w-full py-3 rounded-lg font-semibold transition-all duration-300"
        :class="store.selectedSeats.length > 0 ? 'bg-red-600 hover:bg-red-700 text-white' : 'bg-gray-700 text-gray-500 cursor-not-allowed'"
      >
        Lanjut ke Pembayaran
      </button>
    </div>
  </div>
</template>