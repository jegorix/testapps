<!-- src/components/ui/PostDetailSkeleton.vue -->
<template>
  <div class="bg-white rounded-xl shadow-sm border border-gray-200 animate-pulse">
    <!-- Изображение -->
    <div class="h-64 md:h-80 bg-gray-300 rounded-t-xl"></div>
    
    <div class="p-6 md:p-8">
      <!-- Заголовок -->
      <div class="h-8 bg-gray-300 rounded mb-4"></div>
      <div class="h-8 bg-gray-300 rounded w-3/4 mb-6"></div>
      
      <!-- Метаданные -->
      <div class="flex items-center space-x-4 mb-8">
        <div class="w-10 h-10 bg-gray-300 rounded-full"></div>
        <div class="space-y-2">
          <div class="h-4 bg-gray-300 rounded w-24"></div>
          <div class="h-3 bg-gray-200 rounded w-16"></div>
        </div>
      </div>
      
      <!-- Содержимое -->
      <div class="space-y-3 mb-8">
        <div class="h-4 bg-gray-200 rounded"></div>
        <div class="h-4 bg-gray-200 rounded"></div>
        <div class="h-4 bg-gray-200 rounded w-5/6"></div>
        <div class="h-4 bg-gray-200 rounded"></div>
        <div class="h-4 bg-gray-200 rounded w-4/5"></div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PostDetailSkeleton'
}
</script>