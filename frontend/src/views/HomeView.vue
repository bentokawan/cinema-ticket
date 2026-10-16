<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { api } from '../api'
import { RouterLink } from 'vue-router'

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
</script>

<template>
  <div class="space-y-6">
    <h1 class="text-2xl font-bold border-l-4 border-red-500 pl-3">Sedang Tayang</h1>
    
    <div v-if="loading" class="text-gray-400 animate-pulse">Memuat daftar film...</div>
    <div v-else-if="error" class="bg-red-500/20 text-red-400 p-4 rounded-lg border border-red-500/50">{{ error }}</div>
    <div v-else-if="!movies.length" class="text-gray-400">Belum ada film yang tersedia saat ini.</div>
    
    <div v-else class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      <RouterLink 
        v-for="movie in movies" 
        :key="movie.id" 
        :to="`/movies/${movie.id}`"
        class="group bg-[#1A1D27] overflow-hidden hover:ring-2 hover:ring-red-500 transition-all duration-300"
      >
        <div class="aspect-[2/3] overflow-hidden bg-gray-800 relative">
          <img :src="movie.poster_url" :alt="movie.title" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
         
        </div>
        <div class="p-4">
          <h2 class="font-semibold text-lg truncate" :title="movie.title">{{ movie.title }}</h2>
          <p class="text-sm text-gray-400 mt-1 truncate">{{ movie.genre }}</p>
          <p class="text-xs text-gray-500 mt-2">{{ movie.duration_minutes }} Menit</p>
        </div>
      </RouterLink>
    </div>
  </div>
</template>