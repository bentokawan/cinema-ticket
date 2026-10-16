<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api, formatRupiah, formatJam, formatTanggal } from '../api'

const route = useRoute()
const router = useRouter()

const order = ref<any>(null)
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const { data } = await api.get(`/orders/${route.params.id}`)
    order.value = data
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Gagal memuat e-ticket.'
  } finally {
    loading.value = false
  }
})

const printTicket = () => {
  window.print()
}
</script>

<template>
  <div class="max-w-xl mx-auto py-6 px-4">
    <div v-if="loading" class="text-gray-400 text-center animate-pulse py-20">
      Menerbitkan e-ticket Anda...
    </div>

    <div v-else-if="error" class="bg-red-500/20 text-red-400 p-6 rounded-2xl border border-red-500/50 text-center">
      <p class="font-medium text-lg">{{ error }}</p>
      <button 
        @click="router.push('/')" 
        class="mt-4 px-6 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg font-medium transition-colors"
      >
        Kembali ke Beranda
      </button>
    </div>

    <div v-else-if="order" class="space-y-6">
      <!-- Success Banner -->
      <div class="text-center space-y-2">
        <div class="inline-flex items-center justify-center w-16 h-16 rounded-full bg-green-500/20 text-green-400 mb-2 border border-green-500/30">
          <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path>
          </svg>
        </div>
        <h1 class="text-2xl sm:text-3xl font-extrabold text-white">Pembayaran Berhasil!</h1>
        <p class="text-sm text-gray-400">E-Ticket bioskop resmi Anda telah diterbitkan.</p>
      </div>

      <!-- Cinema E-Ticket Card -->
      <div id="printable-ticket" class="relative bg-[#1A1D27] rounded-3xl overflow-hidden border border-white/10 shadow-2xl">
        <!-- Ticket Top / Header Section -->
        <div class="p-6 sm:p-8 bg-gradient-to-b from-red-600/20 to-transparent border-b border-white/5">
          <div class="flex justify-between items-start gap-4">
            <div>
              <div class="flex items-center gap-2 mb-2">
                <span class="text-xs font-bold tracking-widest uppercase bg-red-600 text-white px-2.5 py-0.5 rounded">
                  E-TICKET
                </span>
                <span class="text-xs text-green-400 font-semibold flex items-center gap-1">
                  ● LUNAS
                </span>
              </div>
              <h2 class="text-2xl font-bold text-white tracking-tight">{{ order.movie }}</h2>
              <p class="text-sm text-gray-300 mt-1 font-medium">{{ order.studio }}</p>
            </div>
            
            <img 
              v-if="order.poster_url" 
              :src="order.poster_url" 
              :alt="order.movie"
              class="w-20 rounded-xl object-cover aspect-[2/3] shadow-lg border border-white/10 shrink-0"
            />
          </div>
        </div>

        <!-- Perforation Divider with Ticket Cutouts -->
        <div class="relative flex items-center justify-center my-0">
          <div class="absolute -left-4 w-8 h-8 rounded-full bg-[#0F1117] border-r border-white/10"></div>
          <div class="w-full border-t-2 border-dashed border-white/20 mx-6"></div>
          <div class="absolute -right-4 w-8 h-8 rounded-full bg-[#0F1117] border-l border-white/10"></div>
        </div>

        <!-- Ticket Body Section -->
        <div class="p-6 sm:p-8 space-y-6">
          <!-- Details Grid -->
          <div class="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span class="text-xs text-gray-400 uppercase tracking-wider block">Tanggal</span>
              <span class="font-semibold text-white">{{ formatTanggal(order.start_time) }}</span>
            </div>
            <div>
              <span class="text-xs text-gray-400 uppercase tracking-wider block">Waktu Tayang</span>
              <span class="font-semibold text-white">{{ formatJam(order.start_time) }} WIB</span>
            </div>
            <div>
              <span class="text-xs text-gray-400 uppercase tracking-wider block">Nomor Kursi</span>
              <div class="flex flex-wrap gap-1 mt-1">
                <span 
                  v-for="seat in order.seats" 
                  :key="seat"
                  class="bg-red-600/20 text-red-400 border border-red-500/30 text-xs px-2.5 py-0.5 rounded font-bold"
                >
                  {{ seat }}
                </span>
              </div>
            </div>
            <div>
              <span class="text-xs text-gray-400 uppercase tracking-wider block">Jumlah Tiket</span>
              <span class="font-semibold text-white">{{ order.seats?.length }} Orang</span>
            </div>
          </div>

          <div class="border-t border-white/5 pt-4 grid grid-cols-2 gap-4 text-xs">
            <div>
              <span class="text-gray-400 block">Nama Pemesan</span>
              <span class="text-white font-medium truncate block">{{ order.customer_name }}</span>
            </div>
            <div>
              <span class="text-gray-400 block">Metode Bayar</span>
              <span class="text-white font-medium capitalize">{{ order.payment_method || 'Transfer' }}</span>
            </div>
          </div>

          <!-- Booking Code & Barcode Box -->
          <div class="bg-[#0F1117] p-5 rounded-2xl border border-white/10 text-center space-y-3">
            <span class="text-xs text-gray-400 uppercase tracking-widest block">KODE BOOKING</span>
            <div class="text-3xl font-mono font-black tracking-widest text-red-500 select-all">
              {{ order.booking_code }}
            </div>
            
            <!-- Simulated Barcode -->
            <div class="pt-2 flex justify-center items-center gap-[3px] h-10 px-6 opacity-80">
              <div v-for="n in 36" :key="n" 
                class="bg-white h-full"
                :style="{ width: (n % 3 === 0 ? '3px' : n % 2 === 0 ? '2px' : '1px') }"
              ></div>
            </div>
            <p class="text-[11px] text-gray-400">
              Tunjukkan barcode atau kode booking ini pada mesin cetak tiket mandiri di bioskop.
            </p>
          </div>

          <!-- Total Payment -->
          <div class="flex justify-between items-center text-sm pt-2">
            <span class="text-gray-400">Total Pembayaran</span>
            <span class="text-xl font-bold text-white">{{ formatRupiah(order.total_price) }}</span>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex flex-col sm:flex-row gap-3 pt-2">
        <button 
          @click="printTicket"
          class="flex-1 py-3 px-4 bg-white/10 hover:bg-white/20 text-white rounded-xl font-semibold transition-colors flex items-center justify-center gap-2 text-sm"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"></path>
          </svg>
          Cetak / Unduh Tiket
        </button>
        <button 
          @click="router.push('/')"
          class="flex-1 py-3 px-4 bg-red-600 hover:bg-red-700 text-white rounded-xl font-semibold transition-colors flex items-center justify-center gap-2 text-sm shadow-lg shadow-red-600/30"
        >
          Kembali ke Beranda
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
@media print {
  body * {
    visibility: hidden;
  }
  #printable-ticket, #printable-ticket * {
    visibility: visible;
  }
  #printable-ticket {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    border: none;
    background: #111 !important;
    color: #fff !important;
  }
}
</style>
