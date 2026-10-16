<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  seats: any[]
  selectedIds: number[]
}>()

const emit = defineEmits(['toggle'])

const rows = computed(() => {
  const map: Record<string, any[]> = {}
  for (const s of props.seats) {
    const list = map[s.row] || []
    list.push(s)
    map[s.row] = list
  }
  return Object.entries(map)
})

const seatClass = (s: any) => {
  if (s.status === 'taken') return 'bg-gray-700 cursor-not-allowed text-gray-500'
  if (props.selectedIds.includes(s.id)) return 'bg-red-600 text-white border border-red-500 shadow-[0_0_10px_rgba(220,38,38,0.5)]'
  return 'bg-gray-300 text-gray-900 hover:bg-white'
}
</script>

<template>
  <div class="space-y-4 max-w-2xl mx-auto overflow-x-auto pb-4">

    <div class="mx-auto mb-10 w-3/4 rounded-t-xl bg-gradient-to-b from-gray-500 to-transparent pt-1 text-center text-xs tracking-[0.3em] opacity-80 h-8 shadow-[0_-10px_20px_rgba(255,255,255,0.1)]">
      LAYAR
    </div>

    <div v-for="[row, list] in rows" :key="row" class="flex items-center justify-center gap-2 min-w-max">
      <span class="w-6 text-sm font-semibold text-gray-400 text-center">{{ row }}</span>
      <button
        v-for="s in list"
        :key="s.id"
        :disabled="s.status === 'taken'"
        :class="seatClass(s)"
        class="h-9 w-9 rounded-t-lg rounded-b-sm text-xs font-bold transition-all duration-200"
        @click="emit('toggle', s)"
      >
        {{ s.number }}
      </button>
      <span class="w-6 text-sm font-semibold text-gray-400 text-center">{{ row }}</span>
    </div>

    <div class="flex justify-center gap-6 pt-8 text-sm text-gray-400">
      <span class="flex items-center gap-2"><i class="h-4 w-4 rounded bg-gray-300"></i>Tersedia</span>
      <span class="flex items-center gap-2"><i class="h-4 w-4 rounded bg-red-600 border border-red-500"></i>Dipilih</span>
      <span class="flex items-center gap-2"><i class="h-4 w-4 rounded bg-gray-700"></i>Terisi</span>
    </div>
  </div>
</template>