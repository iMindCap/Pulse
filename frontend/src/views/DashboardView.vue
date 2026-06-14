<script setup lang="ts">
import { onMounted, onUnmounted, computed } from 'vue'
import { usePulseStore } from '@/stores/pulse'
import MetricCard from '@/components/widgets/MetricCard.vue'
import DockerSummary from '@/components/widgets/DockerSummary.vue'
import ServicesSummary from '@/components/widgets/ServicesSummary.vue'

const store = usePulseStore()

let interval: ReturnType<typeof setInterval>

onMounted(async () => {
  await store.fetchAll()
  interval = setInterval(() => store.fetchAll(), 5000)
})

onUnmounted(() => {
  clearInterval(interval)
})

const uptime = computed(() => {
  if (!store.systemMetrics?.boot_time) return '--'
  const seconds = Date.now() / 1000 - store.systemMetrics.boot_time
  const days = Math.floor(seconds / 86400)
  const hours = Math.floor((seconds % 86400) / 3600)
  const mins = Math.floor((seconds % 3600) / 60)
  if (days > 0) return `${days}d ${hours}h ${mins}m`
  if (hours > 0) return `${hours}h ${mins}m`
  return `${mins}m`
})

const lastUpdatedText = computed(() => {
  if (!store.lastUpdated) return ''
  return store.lastUpdated.toLocaleTimeString()
})
</script>

<template>
  <div class="space-y-8">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <p class="text-text-secondary text-sm">
          System uptime: {{ uptime }}
        </p>
      </div>
      <div class="flex items-center gap-2 text-text-tertiary text-xs">
        <span
          class="w-2 h-2 rounded-full"
          :class="store.isLoading ? 'bg-accent-orange animate-pulse' : 'bg-accent-green'"
        ></span>
        <span v-if="lastUpdatedText">Updated {{ lastUpdatedText }}</span>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="store.isLoading && !store.systemMetrics" class="flex items-center justify-center h-64">
      <div class="flex flex-col items-center gap-3">
        <div class="w-8 h-8 border-2 border-accent-blue border-t-transparent rounded-full animate-spin"></div>
        <span class="text-text-secondary text-sm">Loading metrics...</span>
      </div>
    </div>

    <!-- System Metrics -->
    <template v-else>
      <section>
        <h2 class="text-text-secondary text-xs font-semibold uppercase tracking-wider mb-4">
          System
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <MetricCard
            title="CPU"
            :value="store.systemMetrics?.cpu?.percent ?? 0"
            unit="%"
            :subtitle="`${store.systemMetrics?.cpu?.cores ?? '--'} cores · ${store.systemMetrics?.cpu?.freq_mhz ?? '--'} MHz`"
            color="blue"
          />
          <MetricCard
            title="Memory"
            :value="store.systemMetrics?.memory?.percent ?? 0"
            unit="%"
            :subtitle="`${store.systemMetrics?.memory?.used_gb ?? '--'} / ${store.systemMetrics?.memory?.total_gb ?? '--'} GB`"
            color="purple"
          />
          <MetricCard
            title="Disk"
            :value="store.systemMetrics?.disk?.percent ?? 0"
            unit="%"
            :subtitle="`${store.systemMetrics?.disk?.used_gb ?? '--'} / ${store.systemMetrics?.disk?.total_gb ?? '--'} GB`"
            color="orange"
          />
          <MetricCard
            title="Temperature"
            :value="store.systemMetrics?.temperature?.cpu_celsius ?? 0"
            unit="°C"
            subtitle="CPU"
            color="red"
          />
        </div>
      </section>

      <!-- Docker & Services -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <section>
          <h2 class="text-text-secondary text-xs font-semibold uppercase tracking-wider mb-4">
            Docker
          </h2>
          <DockerSummary
            :info="store.dockerInfo"
            :containers="store.containers"
          />
        </section>

        <section>
          <h2 class="text-text-secondary text-xs font-semibold uppercase tracking-wider mb-4">
            Services
          </h2>
          <ServicesSummary :services="store.services" />
        </section>
      </div>
    </template>
  </div>
</template>