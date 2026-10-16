<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api, formatRupiah, formatJam, formatTanggal } from '../api'

const route = useRoute()
const router = useRouter()

const order = ref<any>(null)
const loading = ref(true)
const paying = ref(false)
const error = ref('')
const timeLeft = ref(0)
let timer: any = null

const selectedCategory = ref<'transfer' | 'ewallet' | 'card'>('transfer')
const selectedProvider = ref('BCA')

const paymentOptions = {
  transfer: [
    { id: 'BCA', name: 'BCA Virtual Account', icon: '🏦', va: '88012839201928' },
    { id: 'Mandiri', name: 'Mandiri Virtual Account', icon: '🏛️', va: '89102839102938' },
    { id: 'BNI', name: 'BNI Virtual Account', icon: '💳', va: '98201928301928' },
    { id: 'BRI', name: 'BRI Virtual Account', icon: '🏧', va: '10293847561029' }
  ],
  ewallet: [
    { id: 'GoPay', name: 'GoPay / GoPay Later', icon: '🟢', desc: 'Scan QRIS atau bayar via aplikasi Gojek' },
    { id: 'OVO', name: 'OVO Cash', icon: '🟣', desc: 'Konfirmasi via notifikasi aplikasi OVO' },
    { id: 'DANA', name: 'DANA Dompet Digital', icon: '🔵', desc: 'Bayar instan dengan saldo DANA' },
    { id: 'ShopeePay', name: 'ShopeePay', icon: '🟠', desc: 'Gunakan koin & promo ShopeePay' }
  ],
  card: [
    { id: 'Visa', name: 'Kartu Kredit / Debit Visa', icon: '💳' },
    { id: 'Mastercard', name: 'Mastercard Worldwide', icon: '💳' },
    { id: 'JCB', name: 'JCB Card', icon: '💳' }
  ]
}

const cardForm = ref({
  number: '',
  expiry: '',
  cvv: '',
  holder: ''
})

onMounted(async () => {
  try {
    const { data } = await api.get(`/orders/${route.params.id}`)
    order.value = data
    timeLeft.value = data.expires_in || 0

    if (order.value.status === 'paid') {
      router.replace(`/success/${order.value.id}`)
      return
    }

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
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Gagal memuat informasi pesanan.'
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

const handlePay = async () => {
  paying.value = true
  error.value = ''

  try {
    await api.post(`/orders/${route.params.id}/pay`, {
      method: selectedCategory.value
    })
    
    // Redirect ke halaman sukses e-ticket
    router.push(`/success/${route.params.id}`)
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Gagal memproses pembayaran. Silakan coba lagi.'
  } finally {
    paying.value = false
  }
}
</script>

<template>
  <div class="max-w-4xl mx-auto py-6">
    <div v-if="loading" class="text-gray-400 text-center animate-pulse py-16">
      Memuat rincian pembayaran...
    </div>

    <div v-else-if="error && !order" class="bg-red-500/20 text-red-400 p-6 rounded-2xl border border-red-500/50 text-center">
      <p class="font-medium text-lg">{{ error }}</p>
      <button 
        @click="router.push('/')" 
        class="mt-4 px-6 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg font-medium transition-colors"
      >
        Kembali ke Beranda
      </button>
    </div>

    <div v-else-if="order" class="space-y-6">
      <!-- Header -->
      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 border-b border-white/10 pb-6">
        <div>
          <button @click="router.push(`/order/${order.id}`)" class="text-xs text-gray-400 hover:text-white flex items-center gap-1 mb-2">
            &larr; Kembali ke Ringkasan
          </button>
          <h1 class="text-3xl font-bold border-l-4 border-red-500 pl-3">Pembayaran Tiket</h1>
        </div>
        <div class="bg-yellow-500/10 border border-yellow-500/30 px-4 py-2 rounded-xl flex items-center gap-3">
          <span class="text-xs text-yellow-400 font-medium">Batas Waktu:</span>
          <span class="font-mono font-bold text-yellow-400 text-lg">{{ formattedCountdown }}</span>
        </div>
      </div>

      <!-- Warning if expired -->
      <div v-if="order.status === 'expired' || timeLeft <= 0" class="bg-red-500/20 border border-red-500/50 p-6 rounded-2xl text-center space-y-3">
        <h3 class="text-lg font-bold text-red-400">Waktu Pembayaran Habis</h3>
        <p class="text-sm text-gray-300">Hold kursi telah kadaluarsa dan pesanan ini dibatalkan secara otomatis.</p>
        <button 
          @click="router.push('/')" 
          class="px-6 py-2.5 bg-red-600 hover:bg-red-700 text-white rounded-lg font-medium transition-colors text-sm"
        >
          Pilih Jadwal Lain
        </button>
      </div>

      <!-- Main Payment Flow -->
      <div v-else class="grid lg:grid-cols-3 gap-8">
        <!-- Payment Methods Column -->
        <div class="lg:col-span-2 space-y-6">
          <div v-if="error" class="bg-red-500/20 text-red-400 p-4 rounded-xl text-sm border border-red-500/50">
            {{ error }}
          </div>

          <!-- Category Selection -->
          <div class="bg-[#1A1D27] p-6 rounded-2xl border border-white/5 space-y-4">
            <h2 class="text-lg font-semibold text-white">Pilih Metode Pembayaran</h2>
            <div class="grid grid-cols-3 gap-3">
              <button 
                type="button"
                @click="selectedCategory = 'transfer'; selectedProvider = 'BCA'"
                class="p-4 rounded-xl text-center border transition-all flex flex-col items-center gap-2"
                :class="selectedCategory === 'transfer' ? 'bg-red-600/10 border-red-500 text-white shadow-lg shadow-red-500/10' : 'bg-[#0F1117] border-white/10 text-gray-400 hover:border-white/30'"
              >
                <span class="text-2xl">🏦</span>
                <span class="text-xs sm:text-sm font-semibold">Virtual Account</span>
              </button>

              <button 
                type="button"
                @click="selectedCategory = 'ewallet'; selectedProvider = 'GoPay'"
                class="p-4 rounded-xl text-center border transition-all flex flex-col items-center gap-2"
                :class="selectedCategory === 'ewallet' ? 'bg-red-600/10 border-red-500 text-white shadow-lg shadow-red-500/10' : 'bg-[#0F1117] border-white/10 text-gray-400 hover:border-white/30'"
              >
                <span class="text-2xl">📱</span>
                <span class="text-xs sm:text-sm font-semibold">E-Wallet / QRIS</span>
              </button>

              <button 
                type="button"
                @click="selectedCategory = 'card'; selectedProvider = 'Visa'"
                class="p-4 rounded-xl text-center border transition-all flex flex-col items-center gap-2"
                :class="selectedCategory === 'card' ? 'bg-red-600/10 border-red-500 text-white shadow-lg shadow-red-500/10' : 'bg-[#0F1117] border-white/10 text-gray-400 hover:border-white/30'"
              >
                <span class="text-2xl">💳</span>
                <span class="text-xs sm:text-sm font-semibold">Kartu Kredit</span>
              </button>
            </div>
          </div>

          <!-- Options Detail by Category -->
          <div class="bg-[#1A1D27] p-6 rounded-2xl border border-white/5 space-y-4">
            <!-- Transfer / Virtual Account -->
            <div v-if="selectedCategory === 'transfer'" class="space-y-3">
              <h3 class="text-sm font-medium text-gray-400">Pilih Bank</h3>
              <div class="space-y-2">
                <label 
                  v-for="opt in paymentOptions.transfer" 
                  :key="opt.id"
                  class="flex items-center justify-between p-3.5 rounded-xl border cursor-pointer transition-all"
                  :class="selectedProvider === opt.id ? 'bg-white/5 border-red-500 text-white' : 'bg-[#0F1117] border-white/5 text-gray-300 hover:border-white/20'"
                >
                  <div class="flex items-center gap-3">
                    <input 
                      type="radio" 
                      name="provider" 
                      :value="opt.id" 
                      v-model="selectedProvider"
                      class="text-red-500 focus:ring-red-500"
                    />
                    <span class="text-xl">{{ opt.icon }}</span>
                    <div>
                      <span class="font-medium text-sm">{{ opt.name }}</span>
                    </div>
                  </div>
                  <span class="text-xs font-mono bg-white/5 px-2.5 py-1 rounded text-gray-400">Otomatis</span>
                </label>
              </div>

              <!-- VA preview info -->
              <div class="mt-4 p-4 rounded-xl bg-[#0F1117] border border-white/10 space-y-1">
                <p class="text-xs text-gray-400">Nomor Virtual Account Simulasi:</p>
                <p class="text-base font-mono font-bold text-red-400">
                  {{ paymentOptions.transfer.find(t => t.id === selectedProvider)?.va }}
                </p>
                <p class="text-[11px] text-gray-500">Pembayaran akan otomatis diverifikasi tanpa perlu upload bukti transfer.</p>
              </div>
            </div>

            <!-- E-Wallet -->
            <div v-else-if="selectedCategory === 'ewallet'" class="space-y-3">
              <h3 class="text-sm font-medium text-gray-400">Pilih Penyedia E-Wallet</h3>
              <div class="space-y-2">
                <label 
                  v-for="opt in paymentOptions.ewallet" 
                  :key="opt.id"
                  class="flex items-center justify-between p-3.5 rounded-xl border cursor-pointer transition-all"
                  :class="selectedProvider === opt.id ? 'bg-white/5 border-red-500 text-white' : 'bg-[#0F1117] border-white/5 text-gray-300 hover:border-white/20'"
                >
                  <div class="flex items-center gap-3">
                    <input 
                      type="radio" 
                      name="provider" 
                      :value="opt.id" 
                      v-model="selectedProvider"
                      class="text-red-500 focus:ring-red-500"
                    />
                    <span class="text-xl">{{ opt.icon }}</span>
                    <div>
                      <p class="font-medium text-sm">{{ opt.name }}</p>
                      <p class="text-xs text-gray-400">{{ opt.desc }}</p>
                    </div>
                  </div>
                </label>
              </div>

              <!-- QRIS Preview -->
              <div class="mt-4 p-4 rounded-xl bg-[#0F1117] border border-white/10 flex items-center gap-4">
                <div class="bg-white p-2 rounded-lg w-20 h-20 flex items-center justify-center">
                  <div class="grid grid-cols-4 gap-0.5 w-full h-full p-1 bg-black rounded">
                    <div v-for="i in 16" :key="i" :class="(i % 2 === 0 || i % 5 === 0) ? 'bg-white' : 'bg-transparent'"></div>
                  </div>
                </div>
                <div class="text-xs space-y-1">
                  <span class="font-bold text-white text-sm">QRIS Standard Terpadu</span>
                  <p class="text-gray-400">Mendukung GoPay, OVO, DANA, ShopeePay, LinkAja, dan Mobile Banking.</p>
                </div>
              </div>
            </div>

            <!-- Credit Card -->
            <div v-else-if="selectedCategory === 'card'" class="space-y-4">
              <h3 class="text-sm font-medium text-gray-400">Detail Kartu Kredit / Debit</h3>
              <div class="space-y-3">
                <div>
                  <label class="block text-xs text-gray-400 mb-1">Nomor Kartu (16 Digit)</label>
                  <input 
                    v-model="cardForm.number" 
                    type="text" 
                    maxlength="19"
                    placeholder="4000 1234 5678 9010" 
                    class="w-full bg-[#0F1117] border border-white/10 rounded-lg p-3 text-white focus:outline-none focus:border-red-500 font-mono text-sm"
                  />
                </div>
                <div class="grid grid-cols-2 gap-3">
                  <div>
                    <label class="block text-xs text-gray-400 mb-1">Masa Berlaku (MM/YY)</label>
                    <input 
                      v-model="cardForm.expiry" 
                      type="text" 
                      maxlength="5"
                      placeholder="12/28" 
                      class="w-full bg-[#0F1117] border border-white/10 rounded-lg p-3 text-white focus:outline-none focus:border-red-500 font-mono text-sm"
                    />
                  </div>
                  <div>
                    <label class="block text-xs text-gray-400 mb-1">CVV (3 Digit)</label>
                    <input 
                      v-model="cardForm.cvv" 
                      type="password" 
                      maxlength="3"
                      placeholder="123" 
                      class="w-full bg-[#0F1117] border border-white/10 rounded-lg p-3 text-white focus:outline-none focus:border-red-500 font-mono text-sm"
                    />
                  </div>
                </div>
                <div>
                  <label class="block text-xs text-gray-400 mb-1">Nama Pemilik Kartu</label>
                  <input 
                    v-model="cardForm.holder" 
                    type="text" 
                    placeholder="Nama sesuai kartu" 
                    class="w-full bg-[#0F1117] border border-white/10 rounded-lg p-3 text-white focus:outline-none focus:border-red-500 text-sm"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Order Summary Column -->
        <div class="space-y-6">
          <div class="bg-[#1A1D27] p-6 rounded-2xl border border-white/5 space-y-4 sticky top-24">
            <h2 class="text-lg font-semibold border-b border-white/10 pb-3">Ringkasan Tagihan</h2>
            
            <div class="flex gap-3 items-center">
              <img 
                v-if="order.poster_url" 
                :src="order.poster_url" 
                class="w-14 rounded-lg object-cover aspect-[2/3] border border-white/10"
              />
              <div class="overflow-hidden">
                <h3 class="font-bold text-sm text-white truncate" :title="order.movie">{{ order.movie }}</h3>
                <p class="text-xs text-gray-400">{{ order.studio }}</p>
                <p class="text-xs text-gray-400">{{ formatTanggal(order.start_time) }} &bull; {{ formatJam(order.start_time) }}</p>
              </div>
            </div>

            <div class="border-t border-white/10 pt-3 space-y-2 text-xs text-gray-400">
              <div class="flex justify-between">
                <span>Kode Booking</span>
                <span class="font-mono text-white font-semibold">{{ order.booking_code }}</span>
              </div>
              <div class="flex justify-between">
                <span>Kursi ({{ order.seats?.length }} Tiket)</span>
                <span class="text-white font-medium">{{ order.seats?.join(', ') }}</span>
              </div>
              <div class="flex justify-between">
                <span>Metode Terpilih</span>
                <span class="text-white capitalize">{{ selectedCategory }} ({{ selectedProvider }})</span>
              </div>
            </div>

            <div class="border-t border-white/10 pt-4">
              <div class="flex justify-between items-baseline mb-4">
                <span class="text-xs text-gray-400">Total Pembayaran</span>
                <span class="text-2xl font-bold text-red-500">{{ formatRupiah(order.total_price) }}</span>
              </div>

              <button 
                @click="handlePay"
                :disabled="paying || timeLeft <= 0"
                class="w-full py-3.5 rounded-xl font-bold text-sm transition-all duration-300 flex justify-center items-center gap-2 shadow-lg"
                :class="paying || timeLeft <= 0 
                  ? 'bg-gray-700 text-gray-500 cursor-not-allowed shadow-none' 
                  : 'bg-red-600 hover:bg-red-700 text-white shadow-red-600/30 active:scale-[0.98]'"
              >
                <svg v-if="paying" class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                <span>{{ paying ? 'Memproses Transaksi...' : `Bayar ${formatRupiah(order.total_price)}` }}</span>
              </button>
            </div>

            <p class="text-[11px] text-gray-500 text-center">
              🔒 Transaksi aman & terenkripsi 256-bit SSL.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
