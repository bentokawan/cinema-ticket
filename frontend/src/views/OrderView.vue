<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api, formatRupiah, formatJam, formatTanggal } from '../api'

const route = useRoute()
const router = useRouter()

const order = ref<any>(null)
const loading = ref(true)
const error = ref('')
const timeLeft = ref(0)
let timer: any = null

onMounted(async () => {
  try {
    const { data } = await api.get(`/orders/${route.params.id}`)
    order.value = data
    timeLeft.value = data.expires_in || 0

    if (order.value.status === 'pending' && timeLeft.value > 0) {
      timer = setInterval(() => {
        if (timeLeft.value > 0) {
          timeLeft.value--
        } else {
          clearInterval(timer)
          order.value.status = 'expired'
        }
      }, 1000)
    }
  } catch (e) {
    error.value = 'Gagal memuat detail pesanan. Order tidak ditemukan.'
  } finally {
    loading.value = false
  }
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})

const formattedCountdown = computed(() => {
  const minutes = Math.floor(timeLeft.value / 60)
  const seconds = timeLeft.value % 60
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`
})

const cancelOrder = async () => {
  if (!confirm('Apakah Anda yakin ingin membatalkan pesanan ini?')) return
  try {
    await api.delete(`/orders/${route.params.id}`)
    alert('Pesanan berhasil dibatalkan.')
    router.push('/')
  } catch (e) {
    alert('Gagal membatalkan pesanan.')
  }
}

const proceedToPayment = () => {
  router.push(`/payment/${route.params.id}`)
}
</script>

<template>
  <div class="max-w-xl mx-auto py-6">
    <div v-if="loading" class="text-gray-400 text-center animate-pulse">Memuat ringkasan pesanan...</div>
    <div v-else-if="error" class="bg-red-500/20 text-red-400 p-4 rounded-xl text-center border border-red-500/50">{{ error }}</div>

    <div v-else-if="order" class="bg-[#1A1D27] p-8 rounded-2xl border border-white/5 space-y-6">

      <div class="flex justify-between items-center border-b border-white/10 pb-6">
        <div>
          <span class="text-xs text-gray-400 uppercase tracking-wider">Kode Booking</span>
          <h1 class="text-2xl font-mono font-bold text-red-500">{{ order.booking_code }}</h1>
        </div>
        <div class="text-right">
          <span class="text-xs text-gray-400 uppercase tracking-wider">Status</span>
          <div>
            <span v-if="order.status === 'pending'" class="bg-yellow-500/20 text-yellow-400 text-xs px-3 py-1 rounded-full font-semibold border border-yellow-500/30">Menunggu Pembayaran</span>
            <span v-else-if="order.status === 'paid'" class="bg-green-500/20 text-green-400 text-xs px-3 py-1 rounded-full font-semibold border border-green-500/30">Sudah Dibayar</span>
            <span v-else class="bg-red-500/20 text-red-400 text-xs px-3 py-1 rounded-full font-semibold border border-red-500/30 capitalize">{{ order.status }}</span>
          </div>
        </div>
      </div>

      <div v-if="order.status === 'pending'" class="bg-yellow-500/10 border border-yellow-500/30 p-4 rounded-xl flex justify-between items-center">
        <div>
          <p class="text-sm font-medium text-yellow-400">Selesaikan Pembayaran Dalam</p>
          <p class="text-xs text-gray-400">Kursi Anda di-hold sementara waktu.</p>
        </div>
        <div class="text-2xl font-mono font-bold text-yellow-400">
          {{ formattedCountdown }}
        </div>
      </div>

      <div class="space-y-4 text-sm">
        <div class="flex justify-between py-2 border-b border-white/5">
          <span class="text-gray-400">Film</span>
          <span class="font-medium text-white">{{ order.movie }}</span>
        </div>
        <div class="flex justify-between py-2 border-b border-white/5">
          <span class="text-gray-400">Studio & Jadwal</span>
          <span class="font-medium text-white">{{ order.studio }} &bull; {{ formatTanggal(order.start_time) }} &bull; {{ formatJam(order.start_time) }}</span>
        </div>
        <div class="flex justify-between py-2 border-b border-white/5">
          <span class="text-gray-400">Kursi Dipilih</span>
          <span class="font-medium text-white">{{ order.seats.join(', ') }}</span>
        </div>
        <div class="flex justify-between py-2 border-b border-white/5">
          <span class="text-gray-400">Pemesan</span>
          <span class="font-medium text-white">{{ order.customer_name }} ({{ order.customer_email }})</span>
        </div>
        <div class="flex justify-between py-2 text-base font-semibold">
          <span class="text-gray-300">Total Tagihan</span>
          <span class="text-red-500 text-xl">{{ formatRupiah(order.total_price) }}</span>
        </div>
      </div>

      <div v-if="order.status === 'pending'" class="flex gap-4 pt-4">
        <button 
          @click="cancelOrder"
          class="w-1/3 bg-white/10 hover:bg-white/20 text-white py-3 rounded-xl font-semibold transition-colors text-sm"
        >
          Batalkan
        </button>
        <button 
          @click="proceedToPayment"
          class="w-2/3 bg-red-600 hover:bg-red-700 text-white py-3 rounded-xl font-semibold transition-colors text-sm shadow-lg shadow-red-600/20"
        >
          Pilih Metode Pembayaran
        </button>
      </div>

      <div v-else class="pt-4">
        <button 
          @click="router.push(`/success/${order.id}`)"
          class="w-full bg-green-600 hover:bg-green-700 text-white py-3 rounded-xl font-semibold transition-colors text-sm"
        >
          Lihat E-Ticket
        </button>
      </div>
    </div>
  </div>
</template>