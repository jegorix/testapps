<!-- PostCardSkeleton.vue -->
<template>
  <div class="card animate-pulse">
    <!-- Изображение -->
    <div class="h-48 bg-gray-300 rounded-t-xl"></div>
    
    <!-- Содержимое -->
    <div class="card-body">
      <!-- Заголовок -->
      <div class="h-4 bg-gray-300 rounded mb-2"></div>
      <div class="h-4 bg-gray-300 rounded w-3/4 mb-4"></div>
      
      <!-- Описание -->
      <div class="space-y-2 mb-4">
        <div class="h-3 bg-gray-200 rounded"></div>
        <div class="h-3 bg-gray-200 rounded"></div>
        <div class="h-3 bg-gray-200 rounded w-1/2"></div>
      </div>
      
      <!-- Метаданные -->
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <div class="h-3 bg-gray-200 rounded w-16"></div>
          <div class="h-3 bg-gray-200 rounded w-20"></div>
        </div>
        <div class="flex items-center space-x-3">
          <div class="h-3 bg-gray-200 rounded w-8"></div>
          <div class="h-3 bg-gray-200 rounded w-8"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PostCardSkeleton'
}
</script>