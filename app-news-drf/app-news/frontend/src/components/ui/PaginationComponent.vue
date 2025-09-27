<!-- PaginationComponent.vue -->
<template>
  <nav class="flex items-center justify-between border-t border-gray-200 px-4 py-3 sm:px-6" aria-label="Pagination">
    <div class="hidden sm:block">
      <p class="text-sm text-gray-700">
        Страница
        <span class="font-medium">{{ currentPage }}</span>
        из
        <span class="font-medium">{{ totalPages }}</span>
      </p>
    </div>
    <div class="flex flex-1 justify-between sm:justify-end">
      <button
        @click="$emit('page-change', currentPage - 1)"
        :disabled="!hasPrevious"
        class="btn-outline btn-sm mr-3"
        :class="{ 'opacity-50 cursor-not-allowed': !hasPrevious }"
      >
        Назад
      </button>
      
      <!-- Номера страниц -->
      <div class="hidden sm:flex items-center space-x-1">
        <button
          v-for="page in visiblePages"
          :key="page"
          @click="$emit('page-change', page)"
          :class="[
            'px-3 py-1 text-sm font-medium rounded-lg transition-colors',
            page === currentPage
              ? 'bg-accent-600 text-white'
              : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100'
          ]"
        >
          {{ page }}
        </button>
      </div>
      
      <button
        @click="$emit('page-change', currentPage + 1)"
        :disabled="!hasNext"
        class="btn-outline btn-sm ml-3"
        :class="{ 'opacity-50 cursor-not-allowed': !hasNext }"
      >
        Вперед
      </button>
    </div>
  </nav>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'PaginationComponent',
  props: {
    currentPage: {
      type: Number,
      required: true
    },
    totalPages: {
      type: Number,
      required: true
    },
    hasNext: {
      type: Boolean,
      default: false
    },
    hasPrevious: {
      type: Boolean,
      default: false
    }
  },
  emits: ['page-change'],
  setup(props) {
    const visiblePages = computed(() => {
      const pages = []
      const start = Math.max(1, props.currentPage - 2)
      const end = Math.min(props.totalPages, props.currentPage + 2)
      
      for (let i = start; i <= end; i++) {
        pages.push(i)
      }
      
      return pages
    })
    
    return {
      visiblePages
    }
  }
}
</script>