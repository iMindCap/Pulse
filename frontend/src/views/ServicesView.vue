<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { usePulseStore } from '@/stores/pulse'

const store = usePulseStore()

const showAddForm = ref(false)
const newServiceName = ref('')
const newServiceUrl = ref('')
const isSubmitting = ref(false)
const error = ref('')

onMounted(() => {
  store.fetchServices()
})

async function handleAddService() {
  if (!newServiceName.value || !newServiceUrl.value) {
    error.value = 'Name and URL are required'
    return
  }

  isSubmitting.value = true
  error.value = ''

  try {
    await store.addService(newServiceName.value, newServiceUrl.value)
    newServiceName.value = ''
    newServiceUrl.value = ''
    showAddForm.value = false
  } catch (e: any) {
    error.value = e.response?.data?.detail || 'Failed to add service'
  } finally {
    isSubmitting.value = false
  }
}

async function handleRemoveService(id: number) {
  await store.removeService(id)
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <p class="text-text-secondary text-sm">Monitor the uptime of your services.</p>
      <button
        @click="showAddForm = !showAddForm"
        class="flex items-center gap-2 px-4 py-2 bg-accent-blue text-white text-sm font-medium rounded-xl hover:opacity-90 transition-opacity duration-200"
      >
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
        </svg>
        Add Service
      </button>
    </div>

    <!-- Add service form -->
    <div
      v-if="showAddForm"
      class="bg-bg-card rounded-2xl border border-border p-5 space-y-4"
    >
      <h3 class="text-text-primary font-medium">New Service</h3>

      <div class="space-y-3">
        <div>
          <label class="text-text-secondary text-xs font-medium block mb-1.5">Name</label>
          <input
            v-model="newServiceName"
            type="text"
            placeholder="My Service"
            class="w-full bg-bg-primary border border-border rounded-xl px-4 py-2.5 text-text-primary text-sm placeholder-text-tertiary focus:outline-none focus:border-accent-blue transition-colors duration-200"
          />
        </div>
        <div>
          <label class="text-text-secondary text-xs font-medium block mb-1.5">URL</label>
          <input
            v-model="newServiceUrl"
            type="text"
            placeholder="http://192.168.1.50:8080"
            class="w-full bg-bg-primary border border-border rounded-xl px-4 py-2.5 text-text-primary text-sm placeholder-text-tertiary focus:outline-none focus:border-accent-blue transition-colors duration-200"
          />
        </div>
      </div>

      <p v-if="error" class="text-accent-red text-xs">{{ error }}</p>

      <div class="flex items-center gap-3 pt-1">
        <button
          @click="handleAddService"
          :disabled="isSubmitting"
          class="px-4 py-2 bg-accent-blue text-white text-sm font-medium rounded-xl hover:opacity-90 transition-opacity duration-200 disabled:opacity-50"
        >
          {{ isSubmitting ? 'Adding...' : 'Add' }}
        </button>
        <button
          @click="showAddForm = false"
          class="px-4 py-2 text-text-secondary text-sm font-medium rounded-xl hover:bg-bg-hover transition-colors duration-200"
        >
          Cancel
        </button>
      </div>
    </div>

    <!-- Services list -->
    <div class="space-y-3">
      <div
        v-for="service in store.services"
        :key="service.id"
        class="bg-bg-card rounded-2xl border border-border p-5 hover:border-border-light transition-all duration-300"
      >
        <div class="flex items-center gap-4">
          <!-- Status -->
          <div
            class="flex items-center justify-center w-10 h-10 rounded-xl shrink-0"
            :class="service.status === 'up' ? 'bg-accent-green/10' : 'bg-accent-red/10'"
          >
            <span
              class="w-3 h-3 rounded-full"
              :class="service.status === 'up' ? 'bg-accent-green' : 'bg-accent-red'"
            ></span>
          </div>

          <!-- Info -->
          <div class="flex-1 min-w-0">
            <h3 class="text-text-primary font-medium">{{ service.name }}</h3>
            <p class="text-text-tertiary text-xs truncate">{{ service.url }}</p>
          </div>

          <!-- Metrics -->
          <div class="text-right shrink-0">
            <p v-if="service.response_time_ms" class="text-text-secondary text-sm font-medium">
              {{ Math.round(service.response_time_ms) }}ms
            </p>
            <p
              class="text-xs font-medium"
              :class="service.status === 'up' ? 'text-accent-green' : 'text-accent-red'"
            >
              {{ service.status === 'up' ? 'Online' : 'Offline' }}
            </p>
          </div>

          <!-- Delete button -->
          <button
            @click="handleRemoveService(service.id)"
            class="p-2 text-text-tertiary hover:text-accent-red rounded-lg hover:bg-bg-hover transition-all duration-200"
          >
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
              <path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Empty state -->
    <div v-if="!store.services.length && !showAddForm" class="flex flex-col items-center justify-center py-16">
      <svg class="w-12 h-12 text-text-tertiary mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
        <path stroke-linecap="round" stroke-linejoin="round" d="M12 21a9.004 9.004 0 0 0 8.716-6.747M12 21a9.004 9.004 0 0 1-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 0 1 7.843 4.582M12 3a8.997 8.997 0 0 0-7.843 4.582m15.686 0A11.953 11.953 0 0 1 12 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0 1 21 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0 1 12 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 0 1 3 12c0-1.605.42-3.113 1.157-4.418" />
      </svg>
      <p class="text-text-tertiary text-sm">No services configured yet</p>
      <button
        @click="showAddForm = true"
        class="text-accent-blue text-sm font-medium hover:underline mt-2"
      >
        Add your first service →
      </button>
    </div>
  </div>
</template>