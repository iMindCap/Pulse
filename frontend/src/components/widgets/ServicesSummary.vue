<script setup lang="ts">
defineProps<{
  services: any[]
}>()
</script>

<template>
  <div class="bg-bg-card rounded-2xl border border-border overflow-hidden">
    <!-- Service list -->
    <div class="divide-y divide-border">
      <div
        v-for="service in services"
        :key="service.id"
        class="flex items-center gap-3 px-5 py-3 hover:bg-bg-hover transition-colors duration-200"
      >
        <!-- Status indicator -->
        <span
          class="w-2 h-2 rounded-full shrink-0"
          :class="service.status === 'up' ? 'bg-accent-green' : 'bg-accent-red'"
        ></span>

        <!-- Service info -->
        <div class="flex-1 min-w-0">
          <p class="text-text-primary text-sm font-medium truncate">
            {{ service.name }}
          </p>
          <p class="text-text-tertiary text-xs truncate">
            {{ service.url }}
          </p>
        </div>

        <!-- Response time -->
        <div class="text-right shrink-0">
          <p v-if="service.response_time_ms" class="text-text-secondary text-xs">
            {{ Math.round(service.response_time_ms) }}ms
          </p>
          <p
            class="text-xs font-medium"
            :class="service.status === 'up' ? 'text-accent-green' : 'text-accent-red'"
          >
            {{ service.status === 'up' ? 'Online' : 'Offline' }}
          </p>
        </div>
      </div>

      <!-- Empty state -->
      <div v-if="!services.length" class="px-5 py-8 text-center">
        <div class="flex flex-col items-center gap-2">
          <svg class="w-8 h-8 text-text-tertiary" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 21a9.004 9.004 0 0 0 8.716-6.747M12 21a9.004 9.004 0 0 1-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 0 1 7.843 4.582M12 3a8.997 8.997 0 0 0-7.843 4.582m15.686 0A11.953 11.953 0 0 1 12 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0 1 21 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0 1 12 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 0 1 3 12c0-1.605.42-3.113 1.157-4.418" />
          </svg>
          <p class="text-text-tertiary text-sm">No services configured</p>
          <RouterLink
            to="/services"
            class="text-accent-blue text-xs font-medium hover:underline mt-1"
          >
            Add a service →
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>