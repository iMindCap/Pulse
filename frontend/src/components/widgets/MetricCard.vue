<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  title: string
  value: number
  unit: string
  subtitle: string
  color: 'blue' | 'purple' | 'orange' | 'red' | 'green'
}>()

const colorMap: Record<string, string> = {
  blue: 'var(--color-accent-blue)',
  purple: 'var(--color-accent-purple)',
  orange: 'var(--color-accent-orange)',
  red: 'var(--color-accent-red)',
  green: 'var(--color-accent-green)',
}

const strokeColor = computed(() => colorMap[props.color] || colorMap.blue)

// Circular progress calculations
const radius = 40
const circumference = 2 * Math.PI * radius
const progress = computed(() => {
  const clampedValue = Math.min(Math.max(props.value, 0), 100)
  return circumference - (clampedValue / 100) * circumference
})

// Dynamic status color based on value
const statusLevel = computed(() => {
  if (props.value >= 90) return 'critical'
  if (props.value >= 75) return 'warning'
  return 'normal'
})
</script>

<template>
  <div class="bg-bg-card rounded-2xl p-5 border border-border hover:border-border-light transition-all duration-300">
    <div class="flex items-center justify-between">
      <!-- Info -->
      <div class="flex flex-col gap-1">
        <span class="text-text-secondary text-xs font-medium uppercase tracking-wider">
          {{ title }}
        </span>
        <div class="flex items-baseline gap-1">
          <span class="text-3xl font-semibold text-text-primary tracking-tight">
            {{ value !== null && value !== undefined ? Math.round(value) : '--' }}
          </span>
          <span class="text-text-tertiary text-sm font-medium">{{ unit }}</span>
        </div>
        <span class="text-text-tertiary text-xs mt-1">{{ subtitle }}</span>
      </div>

      <!-- Circular progress -->
      <div class="relative w-20 h-20">
        <svg class="w-20 h-20 -rotate-90" viewBox="0 0 100 100">
          <!-- Background arc -->
          <circle
            cx="50"
            cy="50"
            :r="radius"
            fill="none"
            stroke="var(--color-border)"
            stroke-width="6"
            stroke-linecap="round"
          />
          <!-- Progress arc -->
          <circle
            cx="50"
            cy="50"
            :r="radius"
            fill="none"
            :stroke="strokeColor"
            stroke-width="6"
            stroke-linecap="round"
            :stroke-dasharray="circumference"
            :stroke-dashoffset="progress"
            class="transition-all duration-700 ease-out"
            :style="{ opacity: statusLevel === 'critical' ? 1 : 0.85 }"
          />
        </svg>
        <!-- Center percentage -->
        <div class="absolute inset-0 flex items-center justify-center">
          <span class="text-xs font-semibold" :style="{ color: strokeColor }">
            {{ value !== null && value !== undefined ? Math.round(value) : '--' }}%
          </span>
        </div>
      </div>
    </div>
  </div>
</template>