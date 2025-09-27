<!-- src/views/categories/CategoriesView.vue -->
<template>
  <div class="min-h-screen bg-gray-50 py-8">
    <div class="container-content">
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-gray-900 mb-4">Категории</h1>
        <p class="text-gray-600 max-w-2xl mx-auto">
          Исследуйте статьи по различным темам и найдите то, что вас интересует
        </p>
      </div>
      
      <div v-if="postsStore.isLoadingCategories" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <CategoryCardSkeleton v-for="i in 12" :key="i" />
      </div>
      
      <div v-else-if="categories.length > 0" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <CategoryCard
          v-for="category in categories"
          :key="category.id"
          :category="category"
        />
      </div>
      
      <div v-else class="text-center py-16">
        <TagIcon class="w-16 h-16 text-gray-300 mx-auto mb-4" />
        <h3 class="text-lg font-medium text-gray-900 mb-2">Категории не найдены</h3>
        <p class="text-gray-500">Пока нет созданных категорий</p>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, onMounted } from 'vue'
import { usePostsStore } from '@/stores/posts'
import CategoryCard from '@/components/categories/CategoryCard.vue'
import CategoryCardSkeleton from '@/components/ui/CategoryCardSkeleton.vue'
import { TagIcon } from '@heroicons/vue/24/outline'

export default {
  name: 'CategoriesView',
  components: { CategoryCard, CategoryCardSkeleton, TagIcon },
  setup() {
    const postsStore = usePostsStore()
    const categories = computed(() => postsStore.categories)
    
    onMounted(() => {
      postsStore.fetchCategories()
    })
    
    return { postsStore, categories }
  }
}
</script>