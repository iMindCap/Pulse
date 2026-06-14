<script setup lang="ts">
import { onMounted } from 'vue'
import { usePulseStore } from '@/stores/pulse'

const store = usePulseStore()

onMounted(() => {
  store.fetchContainers()
})
</script>

<template>
  <div class="space-y-6">
    <p class="text-text-secondary text-sm">All Docker containers on this host.</p>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div
        v-for="container in store.containers"
        :key="container.id"
        class="bg-bg-card rounded-2xl border border-border p-5 hover:border-border-light transition-all duration-300"
      >
        <!-- Header -->
        <div class="flex items-center gap-3 mb-4">
          <span
            class="w-2.5 h-2.5 rounded-full shrink-0"
            :class="container.status === 'running' ? 'bg-accent-green' : 'bg-accent-red'"
          ></span>
          <h3 class="text-text-primary font-medium truncate">{{ container.name }}</h3>
        </div>

        <!-- Details -->
        <div class="space-y-2">
          <div class="flex justify-between">
            <span class="text-text-tertiary text-xs">Image</span>
            <span class="text-text-secondary text-xs truncate ml-4 max-w-[60%] text-right">{{ container.image }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-text-tertiary text-xs">Status</span>
            <span class="text-text-secondary text-xs capitalize">{{ container.status }}</span>
          </div>
          <template v-if="container.stats">
            <div class="flex justify-between">
              <span class="text-text-tertiary text-xs">CPU</span>
              <span class="text-text-secondary text-xs">{{ container.stats.cpu_percent }}%</span>
            </div>
            <div class="flex justify-between">
              <span class="text-text-tertiary text-xs">Memory</span>
              <span class="text-text-secondary text-xs">{{ container.stats.memory_usage_mb }} MB</span>
            </div>
            <div class="flex justify-between">
              <span class="text-text-tertiary text-xs">Network ↓</span>
              <span class="text-text-secondary text-xs">{{ container.stats.network_rx_mb }} MB</span>
            </div>
          </template>
          <div v-if="container.ports.length" class="flex justify-between">
            <span class="text-text-tertiary text-xs">Ports</span>
            <span class="text-text-secondary text-xs">
              {{ container.ports.map((p: any) => p.container).join(', ') }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty state -->
    <div v-if="!store.containers.length" class="flex flex-col items-center justify-center py-16">
      <svg class="w-12 h-12 text-text-tertiary mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
        <path stroke-linecap="round" stroke-linejoin="round" d="m21 7.5-9-5.25L3 7.5m18 0-9 5.25m9-5.25v9l-9 5.25M3 7.5l9 5.25M3 7.5v9l9 5.25m0-9v9" />
      </svg>
      <p class="text-text-tertiary text-sm">No containers found</p>
      <p class="text-text-tertiary text-xs mt-1">Make sure Docker is running on this host</p>
    </div>
  </div>
</template>