<template>
  <router-link
    v-if="category.slug"
    :to="{ name: 'CategoryPosts', params: { slug: category.slug } }"
    class="card hover:shadow-lg transition-all duration-300 group cursor-pointer"
  >
    <div class="card-body text-center py-6">
      <!-- Иконка категории -->
      <div class="w-12 h-12 bg-accent-100 rounded-lg flex items-center justify-center mx-auto mb-4 group-hover:bg-accent-200 transition-colors">
        <component
          :is="getCategoryIcon(category.name)"
          class="w-6 h-6 text-accent-600"
        />
      </div>
      
      <!-- Название категории -->
      <h3 class="text-lg font-semibold text-gray-900 mb-2 group-hover:text-accent-600 transition-colors">
        {{ category.name }}
      </h3>
      
      <!-- Описание -->
      <p v-if="category.description" class="text-gray-600 text-sm mb-3 line-clamp-2">
        {{ category.description }}
      </p>
      
      <!-- Количество постов -->
      <div class="flex items-center justify-center text-sm text-gray-500">
        <DocumentTextIcon class="w-4 h-4 mr-1" />
        <span>{{ category.posts_count }} {{ pluralize(category.posts_count, 'пост', 'поста', 'постов') }}</span>
      </div>
    </div>
  </router-link>
  
  <!-- Fallback для категорий без slug -->
  <div
    v-else
    class="card cursor-not-allowed opacity-50"
  >
    <div class="card-body text-center py-6">
      <div class="w-12 h-12 bg-gray-200 rounded-lg flex items-center justify-center mx-auto mb-4">
        <component
          :is="getCategoryIcon(category.name)"
          class="w-6 h-6 text-gray-400"
        />
      </div>
      
      <h3 class="text-lg font-semibold text-gray-600 mb-2">
        {{ category.name }}
      </h3>
      
      <p v-if="category.description" class="text-gray-500 text-sm mb-3 line-clamp-2">
        {{ category.description }}
      </p>
      
      <div class="flex items-center justify-center text-sm text-gray-400">
        <DocumentTextIcon class="w-4 h-4 mr-1" />
        <span>{{ category.posts_count }} {{ pluralize(category.posts_count, 'пост', 'поста', 'постов') }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import {
  DocumentTextIcon,
  ComputerDesktopIcon,
  BeakerIcon,
  HeartIcon,
  BookOpenIcon,
  GlobeAltIcon,
  CameraIcon,
  MusicalNoteIcon,
  TrophyIcon,
  BriefcaseIcon,
  HomeIcon,
  ShoppingBagIcon,
  AcademicCapIcon,
  FilmIcon,
  TagIcon
} from '@heroicons/vue/24/outline'

export default {
  name: 'CategoryCard',
  components: {
    DocumentTextIcon,
    ComputerDesktopIcon,
    BeakerIcon,
    HeartIcon,
    BookOpenIcon,
    GlobeAltIcon,
    CameraIcon,
    MusicalNoteIcon,
    TrophyIcon,
    BriefcaseIcon,
    HomeIcon,
    ShoppingBagIcon,
    AcademicCapIcon,
    FilmIcon,
    TagIcon
  },
  props: {
    category: {
      type: Object,
      required: true,
      validator(category) {
        return category && typeof category === 'object' && category.name
      }
    }
  },
  setup() {
    const getCategoryIcon = (categoryName) => {
      if (!categoryName) return 'TagIcon'
      
      const name = categoryName.toLowerCase()
      
      if (name.includes('технолог') || name.includes('tech')) return 'ComputerDesktopIcon'
      if (name.includes('наука') || name.includes('science')) return 'BeakerIcon'
      if (name.includes('здоровье') || name.includes('health')) return 'HeartIcon'
      if (name.includes('образование') || name.includes('education')) return 'AcademicCapIcon'
      if (name.includes('путешеств') || name.includes('travel')) return 'GlobeAltIcon'
      if (name.includes('фото') || name.includes('photo')) return 'CameraIcon'
      if (name.includes('музыка') || name.includes('music')) return 'MusicalNoteIcon'
      if (name.includes('спорт') || name.includes('sport')) return 'TrophyIcon'
      if (name.includes('бизнес') || name.includes('business')) return 'BriefcaseIcon'
      if (name.includes('дом') || name.includes('home')) return 'HomeIcon'
      if (name.includes('покупк') || name.includes('shop')) return 'ShoppingBagIcon'
      if (name.includes('книг') || name.includes('book')) return 'BookOpenIcon'
      if (name.includes('фильм') || name.includes('movie') || name.includes('кино')) return 'FilmIcon'
      
      return 'TagIcon'
    }
    
    const pluralize = (count, one, few, many) => {
      if (typeof count !== 'number') return many
      
      const mod10 = count % 10
      const mod100 = count % 100
      
      if (mod100 >= 11 && mod100 <= 19) {
        return many
      }
      if (mod10 === 1) {
        return one
      }
      if (mod10 >= 2 && mod10 <= 4) {
        return few
      }
      return many
    }
    
    return {
      getCategoryIcon,
      pluralize
    }
  }
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>