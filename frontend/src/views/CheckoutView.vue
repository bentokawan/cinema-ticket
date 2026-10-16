<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { api, formatRupiah, formatJam, formatTanggal } from '../api'
import { useBooking } from '../stores/booking'

const router = useRouter()
const store = useBooking()

const form = ref({
  name: '',
  email: '',
  phone: ''
})

const loading = ref(false)
const error = ref('')

onMounted(() => {
  if (!store.showtime || store.selectedSeats.length === 0) {
    router.push('/')
  }
})

const submitOrder = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const payload = {
      showtime_id: store.showtime.id,
      seat_ids: store.selectedSeatIds,
      customer_name: form.value.name,
      customer_email: form.value.email,
      customer_phone: form.value.phone
    }
    
    const { data } = await api.post('/orders/', payload)
    
    router.push(`/order/${data.id}`)
    
  } catch (e: any) {
    if (e.response?.status === 409) {
      error.value = 'Mohon maaf, kursi sudah diambil orang lain. Mengarahkan kembali ke peta kursi...'
      setTimeout(() => {
        router.push(`/showtimes/${store.showtime.id}/seats`)
      }, 3000)
    } else if (e.response?.status === 422) {
      error.value = 'Data tidak valid. Periksa kembali format email dan pastikan semua kolom terisi.'
    } else {
      error.value = 'Terjadi kesalahan sistem. Silakan coba lagi.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div v-if="store.movie" class="max-w-4xl mx-auto">
    <h1 class="text-3xl font-bold mb-8 border-l-4 border-red-500 pl-3">Checkout Tiket</h1>
    
    <div class="grid lg:grid-cols-2 gap-8">
      <div class="bg-[#1A1D27] p-6 rounded-2xl border border-white/5 h-fit">
        <h2 class="text-xl font-semibold mb-6">Data Pemesan</h2>
        
        <div v-if="error" class="mb-4 bg-red-500/20 text-red-400 p-3 rounded-lg text-sm border border-red-500/50">
          {{ error }}
        </div>

        <form @submit.prevent="submitOrder" class="space-y-4">
          <div>
            <label class="block text-sm text-gray-400 mb-1">Nama Lengkap</label>
            <input 
              v-model="form.name" 
              type="text" 
              required
              class="w-full bg-[#0F1117] border border-white/10 rounded-lg p-3 text-white focus:outline-none focus:border-red-500 transition-colors"
              placeholder="Contoh: Budi Santoso"
            >
          </div>
          
          <div>
            <label class="block text-sm text-gray-400 mb-1">Email Aktif</label>
            <input 
              v-model="form.email" 
              type="email" 
              required
              class="w-full bg-[#0F1117] border border-white/10 rounded-lg p-3 text-white focus:outline-none focus:border-red-500 transition-colors"
              placeholder="budi@email.com"
            >
          </div>
          
          <div>
            <label class="block text-sm text-gray-400 mb-1">Nomor Handphone</label>
            <input 
              v-model="form.phone" 
              type="tel" 
              required
              minlength="6"
              maxlength="15"
              class="w-full bg-[#0F1117] border border-white/10 rounded-lg p-3 text-white focus:outline-none focus:border-red-500 transition-colors"
              placeholder="081234567890"
            >
          </div>

          <button 
            type="submit" 
            :disabled="loading"
            class="w-full mt-6 py-3 rounded-lg font-semibold transition-all duration-300 flex justify-center items-center gap-2"
            :class="loading ? 'bg-red-800 text-gray-300 cursor-wait' : 'bg-red-600 hover:bg-red-700 text-white'"
          >
            <svg v-if="loading" class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
            {{ loading ? 'Memproses...' : 'Konfirmasi Pesanan' }}
          </button>
        </form>
      </div>

      <div class="space-y-6">
        <div class="bg-[#1A1D27] p-6 rounded-2xl border border-white/5">
          <h2 class="text-xl font-semibold mb-4 border-b border-white/10 pb-4">Detail Tayang</h2>
          <div class="flex gap-4 mb-4">
            <img :src="store.movie.poster_url" class="w-20 rounded-lg object-cover aspect-[2/3]">
            <div>
              <h3 class="font-bold text-lg">{{ store.movie.title }}</h3>
              <p class="text-sm text-gray-400 mt-1">{{ store.showtime.studio }}</p>
              <p class="text-sm text-gray-400">{{ formatTanggal(store.showtime.start_time) }}, {{ formatJam(store.showtime.start_time) }}</p>
            </div>
          </div>
        </div>

        <div class="bg-[#1A1D27] p-6 rounded-2xl border border-white/5">
          <h2 class="text-xl font-semibold mb-4 border-b border-white/10 pb-4">Kursi & Biaya</h2>
          <div class="space-y-3 text-sm text-gray-400 mb-4">
            <div class="flex justify-between">
              <span>Jumlah Tiket</span>
              <span class="text-white">{{ store.selectedSeats.length }} Tiket</span>
            </div>
            <div class="flex justify-between">
              <span>Nomor Kursi</span>
              <span class="text-white font-medium">
                {{ store.selectedSeats.map(s => `${s.row}${s.number}`).join(', ') }}
              </span>
            </div>
            <div class="flex justify-between">
              <span>Harga Satuan</span>
              <span class="text-white">{{ formatRupiah(store.showtime.price) }}</span>
            </div>
          </div>
          <div class="border-t border-white/10 pt-4 flex justify-between items-end">
            <span class="text-gray-400">Total Harga</span>
            <span class="text-2xl font-bold text-red-500">{{ formatRupiah(store.totalPrice) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>