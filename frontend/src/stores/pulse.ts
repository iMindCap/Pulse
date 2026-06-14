import { ref } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

export const usePulseStore = defineStore('pulse', () => {
  // State
  const systemMetrics = ref<any>(null)
  const dockerInfo = ref<any>(null)
  const containers = ref<any[]>([])
  const services = ref<any[]>([])
  const isLoading = ref(true)
  const lastUpdated = ref<Date | null>(null)

  // Fetch system metrics
  async function fetchSystemMetrics() {
    try {
      const { data } = await axios.get('/api/system')
      systemMetrics.value = data
      lastUpdated.value = new Date()
    } catch (error) {
      console.error('Failed to fetch system metrics:', error)
    }
  }

  // Fetch Docker info
  async function fetchDockerInfo() {
    try {
      const { data } = await axios.get('/api/docker')
      dockerInfo.value = data
    } catch (error) {
      console.error('Failed to fetch Docker info:', error)
    }
  }

  // Fetch containers
  async function fetchContainers() {
    try {
      const { data } = await axios.get('/api/containers')
      containers.value = data.containers
    } catch (error) {
      console.error('Failed to fetch containers:', error)
    }
  }

  // Fetch services
  async function fetchServices() {
    try {
      const { data } = await axios.get('/api/services')
      services.value = data.services
    } catch (error) {
      console.error('Failed to fetch services:', error)
    }
  }

  // Add a new service
  async function addService(name: string, url: string) {
    try {
      await axios.post('/api/services', { name, url })
      await fetchServices()
    } catch (error) {
      console.error('Failed to add service:', error)
      throw error
    }
  }

  // Remove a service
  async function removeService(id: number) {
    try {
      await axios.delete(`/api/services/${id}`)
      await fetchServices()
    } catch (error) {
      console.error('Failed to remove service:', error)
      throw error
    }
  }

  // Fetch all data at once
  async function fetchAll() {
    isLoading.value = true
    await Promise.all([
      fetchSystemMetrics(),
      fetchDockerInfo(),
      fetchContainers(),
      fetchServices(),
    ])
    isLoading.value = false
  }

  return {
    systemMetrics,
    dockerInfo,
    containers,
    services,
    isLoading,
    lastUpdated,
    fetchSystemMetrics,
    fetchDockerInfo,
    fetchContainers,
    fetchServices,
    fetchAll,
    addService,
    removeService,
  }
})