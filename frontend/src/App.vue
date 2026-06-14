<script setup lang="ts">
import { RouterLink, RouterView, useRoute } from 'vue-router'
import { ref } from 'vue'

const route = useRoute()
const sidebarCollapsed = ref(false)

const navigation = [
  { name: 'Dashboard', path: '/', icon: 'dashboard' },
  { name: 'Containers', path: '/containers', icon: 'containers' },
  { name: 'Services', path: '/services', icon: 'services' },
]
</script>

<template>
  <div class="flex h-screen bg-bg-primary">
    <!-- Sidebar -->
    <aside
      class="flex flex-col border-r border-border bg-bg-secondary transition-all duration-300"
      :class="sidebarCollapsed ? 'w-[68px]' : 'w-[240px]'"
    >
      <!-- Logo -->
      <div class="flex items-center gap-3 px-4 py-5 select-none">
        <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-indigo-600 to-cyan-400 flex items-center justify-center shadow-md shadow-cyan-500/20 transition-transform duration-300 hover:scale-105">
          <svg
            class="w-5 h-5 text-white"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            stroke-width="2"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M3 12h3l3-9 4 18 3-13 1 4h3"
            />
          </svg>
        </div>
        <span
          v-if="!sidebarCollapsed"
          class="text-text-primary font-bold text-xl tracking-tight transition-all duration-200"
        >
          Pulse
        </span>
      </div>

      <!-- Navigation -->
      <nav class="flex-1 px-3 py-4 space-y-1">
        <RouterLink
          v-for="item in navigation"
          :key="item.path"
          :to="item.path"
          class="flex items-center gap-3 px-3 py-2.5 rounded-[10px] transition-all duration-200 group"
          :class="
            route.path === item.path
              ? 'bg-bg-hover text-text-primary'
              : 'text-text-secondary hover:bg-bg-hover hover:text-text-primary'
          "
        >
          <!-- Icons -->
          <svg
            v-if="item.icon === 'dashboard'"
            class="w-5 h-5 shrink-0"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            stroke-width="1.5"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M3.75 6A2.25 2.25 0 0 1 6 3.75h2.25A2.25 2.25 0 0 1 10.5 6v2.25a2.25 2.25 0 0 1-2.25 2.25H6a2.25 2.25 0 0 1-2.25-2.25V6ZM3.75 15.75A2.25 2.25 0 0 1 6 13.5h2.25a2.25 2.25 0 0 1 2.25 2.25V18a2.25 2.25 0 0 1-2.25 2.25H6A2.25 2.25 0 0 1 3.75 18v-2.25ZM13.5 6a2.25 2.25 0 0 1 2.25-2.25H18A2.25 2.25 0 0 1 20.25 6v2.25A2.25 2.25 0 0 1 18 10.5h-2.25a2.25 2.25 0 0 1-2.25-2.25V6ZM13.5 15.75a2.25 2.25 0 0 1 2.25-2.25H18a2.25 2.25 0 0 1 2.25 2.25V18A2.25 2.25 0 0 1 18 20.25h-2.25a2.25 2.25 0 0 1-2.25-2.25v-2.25Z"
            />
          </svg>

          <svg
            v-if="item.icon === 'containers'"
            class="w-5 h-5 shrink-0"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            stroke-width="1.5"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="m21 7.5-9-5.25L3 7.5m18 0-9 5.25m9-5.25v9l-9 5.25M3 7.5l9 5.25M3 7.5v9l9 5.25m0-9v9"
            />
          </svg>

          <svg
            v-if="item.icon === 'services'"
            class="w-5 h-5 shrink-0"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            stroke-width="1.5"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M12 21a9.004 9.004 0 0 0 8.716-6.747M12 21a9.004 9.004 0 0 1-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 0 1 7.843 4.582M12 3a8.997 8.997 0 0 0-7.843 4.582m15.686 0A11.953 11.953 0 0 1 12 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0 1 21 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0 1 12 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 0 1 3 12c0-1.605.42-3.113 1.157-4.418"
            />
          </svg>

          <span v-if="!sidebarCollapsed" class="text-sm font-medium">
            {{ item.name }}
          </span>
        </RouterLink>
      </nav>

      <!-- Collapse button -->
      <div class="px-3 py-4 border-t border-border">
        <button
          @click="sidebarCollapsed = !sidebarCollapsed"
          class="flex items-center justify-center w-full py-2 rounded-[10px] text-text-tertiary hover:text-text-secondary hover:bg-bg-hover transition-all duration-200"
        >
          <svg
            class="w-5 h-5 transition-transform duration-300"
            :class="sidebarCollapsed ? 'rotate-180' : ''"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            stroke-width="1.5"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              d="M15.75 19.5 8.25 12l7.5-7.5"
            />
          </svg>
        </button>
      </div>
    </aside>

    <!-- Main content -->
    <main class="flex-1 overflow-y-auto">
      <!-- Top bar -->
      <header class="sticky top-0 z-10 flex items-center h-16 px-8 border-b border-border bg-bg-primary/80 backdrop-blur-xl">
        <h1 class="text-lg font-semibold text-text-primary">
          {{ navigation.find(n => n.path === route.path)?.name || 'Pulse' }}
        </h1>
      </header>

      <!-- Page content -->
      <div class="p-8">
        <RouterView />
      </div>
    </main>
  </div>
</template>