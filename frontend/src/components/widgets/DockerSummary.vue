<script setup lang="ts">
defineProps<{
  info: any
  containers: any[]
}>()

function statusColor(status: string): string {
  switch (status) {
    case 'running': return 'bg-accent-green'
    case 'exited': return 'bg-accent-red'
    case 'paused': return 'bg-accent-yellow'
    default: return 'bg-text-tertiary'
  }
}
</script>

<template>
  <div class="bg-bg-card rounded-2xl border border-border overflow-hidden">
    <!-- Docker not available -->
    <div v-if="info && !info.available" class="p-5">
      <div class="flex items-center gap-3 text-text-tertiary">
        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z" />
        </svg>
        <span class="text-sm">Docker is not available</span>
      </div>
    </div>

    <!-- Docker available -->
    <template v-else>
      <!-- Stats bar -->
      <div class="flex items-center gap-6 px-5 py-4 border-b border-border">
        <div class="flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-accent-green"></span>
          <span class="text-text-primary text-sm font-medium">
            {{ info?.containers_running ?? 0 }}
          </span>
          <span class="text-text-tertiary text-xs">running</span>
        </div>
        <div class="flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-accent-red"></span>
          <span class="text-text-primary text-sm font-medium">
            {{ info?.containers_stopped ?? 0 }}
          </span>
          <span class="text-text-tertiary text-xs">stopped</span>
        </div>
        <div class="ml-auto text-text-tertiary text-xs">
          {{ info?.docker_version ?? '' }}
        </div>
      </div>

      <!-- Container list -->
      <div class="divide-y divide-border">
        <div
          v-for="container in containers.slice(0, 5)"
          :key="container.id"
          class="flex items-center gap-3 px-5 py-3 hover:bg-bg-hover transition-colors duration-200"
        >
          <span class="w-2 h-2 rounded-full shrink-0" :class="statusColor(container.status)"></span>
          <div class="flex-1 min-w-0">
            <p class="text-text-primary text-sm font-medium truncate">
              {{ container.name }}
            </p>
            <p class="text-text-tertiary text-xs truncate">
              {{ container.image }}
            </p>
          </div>
          <div v-if="container.stats" class="text-right shrink-0">
            <p class="text-text-secondary text-xs">
              {{ container.stats.cpu_percent }}% CPU
            </p>
            <p class="text-text-tertiary text-xs">
              {{ container.stats.memory_usage_mb }} MB
            </p>
          </div>
          <div v-else class="shrink-0">
            <span class="text-text-tertiary text-xs capitalize">{{ container.status }}</span>
          </div>
        </div>

        <!-- Empty state -->
        <div v-if="!containers.length" class="px-5 py-8 text-center">
          <p class="text-text-tertiary text-sm">No containers found</p>
        </div>
      </div>

      <!-- Show more -->
      <div v-if="containers.length > 5" class="px-5 py-3 border-t border-border">
        <RouterLink
          to="/containers"
          class="text-accent-blue text-xs font-medium hover:underline"
        >
          View all {{ containers.length }} containers →
        </RouterLink>
      </div>
    </template>
  </div>
</template>