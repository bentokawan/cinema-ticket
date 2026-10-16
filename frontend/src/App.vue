<script setup lang="ts"></script>

<template>
  <header class="border-b border-white/10 px-6 py-4 text-lg font-semibold sticky top-0 bg-[#0F1117]/90 backdrop-blur z-50">
    <RouterLink to="/" class="cursor-pointer">
      Cinema<span class="text-red-500">Go</span>
    </RouterLink>
  </header>
  
  <main class="mx-auto max-w-5xl p-6">
    <RouterView />
  </main>
</template>
