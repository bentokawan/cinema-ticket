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

const selectedMethod = ref<'transfer' | 'ewallet' | 'card'>('transfer')
const loading = ref(false)
const error = ref('')
const successOrder = ref<any>(null)

onMounted(() => {
  if (!store.showtime || store.selectedSeats.length === 0) {
    router.push('/')
  }
})

const submitPayment = async () => {
  loading.value = true
  error.value = ''

  try {
    // 1. Buat pesanan (hold kursi)
    const orderPayload = {
      showtime_id: store.showtime.id,
      seat_ids: store.selectedSeatIds,
      customer_name: form.value.name,
      customer_email: form.value.email,
      customer_phone: form.value.phone
    }
    const createRes = await api.post('/orders/', orderPayload)
    const orderId = createRes.data.id

    // 2. Eksekusi pembayaran
    await api.post(`/orders/${orderId}/pay`, {
      method: selectedMethod.value
    })

    // 3. Ambil data order final
    const finalRes = await api.get(`/orders/${orderId}`)
    successOrder.value = finalRes.data

    // Reset store
    store.resetBooking()
  } catch (e: any) {
    if (e.response?.status === 409) {
      error.value = 'Kursi telah dipilih oleh pengguna lain. Silakan pilih kursi lain.'
    } else if (e.response?.status === 422) {
      error.value = 'Mohon periksa kembali kelengkapan data pemesan.'
    } else {
      error.value = e.response?.data?.detail || 'Terjadi kesalahan saat memproses pembayaran.'
    }
  } finally {
    loading.value = false
  }
}

const handleReset = () => {
  store.resetBooking()
  router.push('/')
}
</script>

<template>
  <div class="max-w-3xl mx-auto py-6">
    <!-- Success State: Tampilan Ringkas Bukti Pemesanan -->
    <div v-if="successOrder" class="bg-[#1A1D27] p-8 rounded-2xl border border-white/10 space-y-6 text-center">
      <div class="w-16 h-16 bg-green-500/20 text-green-400 rounded-full flex items-center justify-center mx-auto border border-green-500/30">
        <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path>
        </svg>
      </div>

      <div class="space-y-1">
        <h1 class="text-2xl font-bold text-white">Pembayaran Berhasil</h1>
        <p class="text-sm text-gray-400">Tiket bioskop Anda telah terkonfirmasi.</p>
      </div>

      <div class="bg-[#0F1117] p-6 rounded-xl border border-white/5 text-left space-y-4 max-w-md mx-auto">
        <div class="flex justify-between items-center border-b border-white/10 pb-3">
          <span class="text-xs text-gray-400 uppercase tracking-wider">Kode Booking</span>
          <span class="text-xl font-mono font-bold text-red-500">{{ successOrder.booking_code }}</span>
        </div>

        <div class="text-sm space-y-2 text-gray-300">
          <div class="flex justify-between">
            <span class="text-gray-400">Film</span>
            <span class="font-medium text-white">{{ successOrder.movie }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-400">Studio & Jadwal</span>
            <span class="text-white">{{ successOrder.studio }} &bull; {{ formatTanggal(successOrder.start_time) }}, {{ formatJam(successOrder.start_time) }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-400">Nomor Kursi</span>
            <span class="font-semibold text-red-400">{{ successOrder.seats?.join(', ') }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-400">Pemesan</span>
            <span class="text-white">{{ successOrder.customer_name }}</span>
          </div>
          <div class="flex justify-between border-t border-white/10 pt-2 font-semibold">
            <span class="text-gray-300">Total Pembayaran</span>
            <span class="text-red-400">{{ formatRupiah(successOrder.total_price) }}</span>
          </div>
        </div>
      </div>

      <button 
        @click="handleReset"
        class="px-8 py-3 bg-red-600 hover:bg-red-700 text-white rounded-xl font-semibold transition-colors text-sm"
      >
        Pesan Tiket Lain
      </button>
    </div>

    <!-- Payment Flow State -->
    <div v-else-if="store.movie" class="space-y-6">
      <div class="flex items-center gap-2 border-b border-white/10 pb-4">
        <button 
          @click="router.back()" 
          class="text-xs text-gray-400 hover:text-white flex items-center gap-1"
        >
          &larr; Ubah Kursi
        </button>
        <h1 class="text-2xl font-bold ml-2">Pembayaran Tiket</h1>
      </div>

      <div v-if="error" class="bg-red-500/20 text-red-400 p-4 rounded-xl text-sm border border-red-500/50">
        {{ error }}
      </div>

      <form @submit.prevent="submitPayment" class="grid md:grid-cols-5 gap-6">
        <!-- Form Pemesan & Metode Bayar (3 Kolom) -->
        <div class="md:col-span-3 space-y-6">
          <!-- Data Pemesan -->
          <div class="bg-[#1A1D27] p-6 rounded-2xl border border-white/5 space-y-4">
            <h2 class="text-base font-semibold text-white">Data Pemesan</h2>
            
            <div class="space-y-3">
              <div>
                <label class="block text-xs text-gray-400 mb-1">Nama Lengkap</label>
                <input 
                  v-model="form.name"
                  type="text" 
                  required 
                  placeholder="Contoh: Budi Santoso"
                  class="w-full bg-[#0F1117] border border-white/10 rounded-lg p-2.5 text-sm text-white focus:outline-none focus:border-red-500 transition-colors"
                />
              </div>

              <div>
                <label class="block text-xs text-gray-400 mb-1">Email</label>
                <input 
                  v-model="form.email"
                  type="email" 
                  required 
                  placeholder="budi@example.com"
                  class="w-full bg-[#0F1117] border border-white/10 rounded-lg p-2.5 text-sm text-white focus:outline-none focus:border-red-500 transition-colors"
                />
              </div>

              <div>
                <label class="block text-xs text-gray-400 mb-1">Nomor Handphone</label>
                <input 
                  v-model="form.phone"
                  type="tel" 
                  required 
                  minlength="8"
                  maxlength="14"
                  placeholder="081234567890"
                  class="w-full bg-[#0F1117] border border-white/10 rounded-lg p-2.5 text-sm text-white focus:outline-none focus:border-red-500 transition-colors"
                />
              </div>
            </div>
          </div>

          <!-- Pilihan Metode Pembayaran -->
          <div class="bg-[#1A1D27] p-6 rounded-2xl border border-white/5 space-y-3">
            <h2 class="text-base font-semibold text-white">Metode Pembayaran</h2>

            <div class="space-y-2">
              <label 
                class="flex items-center justify-between p-3 rounded-xl border cursor-pointer transition-all"
                :class="selectedMethod === 'transfer' ? 'bg-red-600/10 border-red-500 text-white' : 'bg-[#0F1117] border-white/10 text-gray-300 hover:border-white/20'"
              >
                <div class="flex items-center gap-3">
                  <input type="radio" value="transfer" v-model="selectedMethod" class="text-red-500 focus:ring-red-500" />
                  <span class="text-sm font-medium">Transfer Bank (Virtual Account)</span>
                </div>
                <span class="text-xs text-gray-400">BCA, Mandiri, BNI, BRI</span>
              </label>

              <label 
                class="flex items-center justify-between p-3 rounded-xl border cursor-pointer transition-all"
                :class="selectedMethod === 'ewallet' ? 'bg-red-600/10 border-red-500 text-white' : 'bg-[#0F1117] border-white/10 text-gray-300 hover:border-white/20'"
              >
                <div class="flex items-center gap-3">
                  <input type="radio" value="ewallet" v-model="selectedMethod" class="text-red-500 focus:ring-red-500" />
                  <span class="text-sm font-medium">E-Wallet / QRIS</span>
                </div>
                <span class="text-xs text-gray-400">GoPay, OVO, DANA</span>
              </label>

              <label 
                class="flex items-center justify-between p-3 rounded-xl border cursor-pointer transition-all"
                :class="selectedMethod === 'card' ? 'bg-red-600/10 border-red-500 text-white' : 'bg-[#0F1117] border-white/10 text-gray-300 hover:border-white/20'"
              >
                <div class="flex items-center gap-3">
                  <input type="radio" value="card" v-model="selectedMethod" class="text-red-500 focus:ring-red-500" />
                  <span class="text-sm font-medium">Kartu Kredit / Debit</span>
                </div>
                <span class="text-xs text-gray-400">Visa, Mastercard</span>
              </label>
            </div>
          </div>
        </div>

        <!-- Ringkasan & Tombol Bayar (2 Kolom) -->
        <div class="md:col-span-2 space-y-4">
          <div class="bg-[#1A1D27] p-5 rounded-2xl border border-white/5 space-y-4 sticky top-24">
            <h3 class="font-semibold text-base border-b border-white/10 pb-3">Ringkasan Tiket</h3>
            
            <div class="space-y-1">
              <h4 class="font-bold text-white text-base">{{ store.movie.title }}</h4>
              <p class="text-xs text-gray-400">{{ store.showtime.studio }}</p>
              <p class="text-xs text-gray-400">{{ formatTanggal(store.showtime.start_time) }}, {{ formatJam(store.showtime.start_time) }}</p>
            </div>

            <div class="border-t border-white/10 pt-3 space-y-2 text-xs text-gray-300">
              <div class="flex justify-between">
                <span class="text-gray-400">Kursi Dipilih</span>
                <span class="font-bold text-red-400">
                  {{ store.selectedSeats.map(s => `${s.row}${s.number}`).join(', ') }}
                </span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-400">Jumlah Tiket</span>
                <span>{{ store.selectedSeats.length }} Tiket</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-400">Harga Satuan</span>
                <span>{{ formatRupiah(store.showtime.price) }}</span>
              </div>
            </div>

            <div class="border-t border-white/10 pt-3 flex justify-between items-end">
              <span class="text-xs text-gray-400">Total Tagihan</span>
              <span class="text-xl font-bold text-red-500">{{ formatRupiah(store.totalPrice) }}</span>
            </div>

            <button 
              type="submit"
              :disabled="loading"
              class="w-full mt-2 py-3 bg-red-600 hover:bg-red-700 disabled:bg-gray-700 text-white rounded-xl font-semibold transition-colors flex items-center justify-center gap-2 text-sm shadow-lg shadow-red-600/20"
            >
              <svg v-if="loading" class="animate-spin h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span>{{ loading ? 'Memproses...' : 'Bayar Sekarang' }}</span>
            </button>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>
