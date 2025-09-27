import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { commentsAPI } from '@/services/api'

export const useCommentsStore = defineStore('comments', () => {
  // Состояние
  const comments = ref([])
  const postComments = ref([])
  const myComments = ref([])
  const currentComment = ref(null)
  const commentReplies = ref({}) // Объект для хранения ответов по ID комментария
  
  // Состояния загрузки
  const isLoading = ref(false)
  const isLoadingReplies = ref({}) // Объект для отслеживания загрузки ответов
  const isSubmitting = ref(false)

  // Вычисляемые свойства
  const topLevelComments = computed(() => 
    postComments.value.filter(comment => !comment.parent)
  )
  
  const repliesCount = computed(() => 
    postComments.value.filter(comment => comment.parent).length
  )
  
  const totalCommentsCount = computed(() => postComments.value.length)

  // Действия для комментариев
  const fetchComments = async (params = {}) => {
    isLoading.value = true
    try {
      const response = await commentsAPI.getAll(params)
      comments.value = response.data.results || []
      return response.data
    } catch (error) {
      console.error('Ошибка загрузки комментариев:', error)
      comments.value = []
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const fetchPostComments = async (postId) => {
    isLoading.value = true
    try {
      const response = await commentsAPI.getPostComments(postId)
      const data = response.data
      
      postComments.value = data.comments || []
      
      // Сортируем комментарии: сначала основные, потом ответы
      postComments.value.sort((a, b) => {
        if (!a.parent && !b.parent) {
          return new Date(b.created_at) - new Date(a.created_at)
        }
        if (!a.parent && b.parent) return -1
        if (a.parent && !b.parent) return 1
        return new Date(a.created_at) - new Date(b.created_at)
      })
      
      return data
    } catch (error) {
      console.error('Ошибка загрузки комментариев поста:', error)
      postComments.value = []
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const fetchCommentById = async (commentId) => {
    isLoading.value = true
    try {
      const response = await commentsAPI.getById(commentId)
      currentComment.value = response.data
      return response.data
    } catch (error) {
      console.error('Ошибка загрузки комментария:', error)
      currentComment.value = null
      throw error
    } finally {
      isLoading.value = false
    }
  }

  const fetchCommentReplies = async (commentId) => {
    if (isLoadingReplies.value[commentId]) return
    
    isLoadingReplies.value[commentId] = true
    try {
      const response = await commentsAPI.getCommentReplies(commentId)
      const data = response.data
      
      commentReplies.value[commentId] = data.replies || []
      return data
    } catch (error) {
      console.error('Ошибка загрузки ответов на комментарий:', error)
      commentReplies.value[commentId] = []
      throw error
    } finally {
      isLoadingReplies.value[commentId] = false
    }
  }

  const createComment = async (commentData) => {
    isSubmitting.value = true
    try {
      const response = await commentsAPI.create(commentData)
      const newComment = response.data
      
      // Если это комментарий к посту (загружены комментарии поста)
      if (postComments.value.length > 0 || commentData.post) {
        if (newComment.parent) {
          // Это ответ на комментарий
          postComments.value.push(newComment)
          
          // Обновляем счетчик ответов у родительского комментария
          const parentComment = postComments.value.find(c => c.id === newComment.parent)
          if (parentComment) {
            parentComment.replies_count = (parentComment.replies_count || 0) + 1
          }
          
          // Добавляем в кэш ответов
          if (commentReplies.value[newComment.parent]) {
            commentReplies.value[newComment.parent].push(newComment)
          }
        } else {
          // Это основной комментарий
          postComments.value.unshift(newComment)
        }
      }
      
      // Добавляем в общий список
      comments.value.unshift(newComment)
      
      return newComment
    } catch (error) {
      console.error('Ошибка создания комментария:', error)
      throw error
    } finally {
      isSubmitting.value = false
    }
  }

  const updateComment = async (commentId, commentData) => {
    isSubmitting.value = true
    try {
      const response = await commentsAPI.update(commentId, commentData)
      const updatedComment = response.data
      
      // Обновляем в списке комментариев поста
      const postIndex = postComments.value.findIndex(c => c.id === commentId)
      if (postIndex !== -1) {
        postComments.value[postIndex] = updatedComment
      }
      
      // Обновляем в общем списке
      const index = comments.value.findIndex(c => c.id === commentId)
      if (index !== -1) {
        comments.value[index] = updatedComment
      }
      
      // Обновляем в кэше ответов
      Object.keys(commentReplies.value).forEach(parentId => {
        const replyIndex = commentReplies.value[parentId].findIndex(c => c.id === commentId)
        if (replyIndex !== -1) {
          commentReplies.value[parentId][replyIndex] = updatedComment
        }
      })
      
      // Обновляем текущий комментарий
      if (currentComment.value && currentComment.value.id === commentId) {
        currentComment.value = updatedComment
      }
      
      return updatedComment
    } catch (error) {
      console.error('Ошибка обновления комментария:', error)
      throw error
    } finally {
      isSubmitting.value = false
    }
  }

  const updateCommentPartial = async (commentId, commentData) => {
    isSubmitting.value = true
    try {
      const response = await commentsAPI.updatePartial(commentId, commentData)
      const updatedComment = response.data
      
      // Аналогично updateComment
      const postIndex = postComments.value.findIndex(c => c.id === commentId)
      if (postIndex !== -1) {
        postComments.value[postIndex] = updatedComment
      }
      
      const index = comments.value.findIndex(c => c.id === commentId)
      if (index !== -1) {
        comments.value[index] = updatedComment
      }
      
      Object.keys(commentReplies.value).forEach(parentId => {
        const replyIndex = commentReplies.value[parentId].findIndex(c => c.id === commentId)
        if (replyIndex !== -1) {
          commentReplies.value[parentId][replyIndex] = updatedComment
        }
      })
      
      if (currentComment.value && currentComment.value.id === commentId) {
        currentComment.value = updatedComment
      }
      
      return updatedComment
    } catch (error) {
      console.error('Ошибка обновления комментария:', error)
      throw error
    } finally {
      isSubmitting.value = false
    }
  }

  const deleteComment = async (commentId) => {
    isSubmitting.value = true
    try {
      await commentsAPI.delete(commentId)
      
      // Помечаем комментарий как неактивный (мягкое удаление)
      const updateCommentStatus = (commentsList) => {
        const index = commentsList.findIndex(c => c.id === commentId)
        if (index !== -1) {
          commentsList[index].is_active = false
          commentsList[index].content = '[Комментарий удален]'
        }
      }
      
      updateCommentStatus(postComments.value)
      updateCommentStatus(comments.value)
      updateCommentStatus(myComments.value)
      
      // Обновляем в кэше ответов
      Object.keys(commentReplies.value).forEach(parentId => {
        updateCommentStatus(commentReplies.value[parentId])
      })
      
      // Очищаем текущий комментарий
      if (currentComment.value && currentComment.value.id === commentId) {
        currentComment.value = null
      }
      
      return true
    } catch (error) {
      console.error('Ошибка удаления комментария:', error)
      throw error
    } finally {
      isSubmitting.value = false
    }
  }

  const fetchMyComments = async (params = {}) => {
    isLoading.value = true
    try {
      const response = await commentsAPI.getMyComments(params)
      myComments.value = response.data.results || []
      return response.data
    } catch (error) {
      console.error('Ошибка загрузки моих комментариев:', error)
      myComments.value = []
      throw error
    } finally {
      isLoading.value = false
    }
  }

  // Утилиты
  const getCommentsByParent = (parentId) => {
    return postComments.value.filter(comment => comment.parent === parentId)
  }

  const getCommentById = (commentId) => {
    return postComments.value.find(comment => comment.id === commentId) ||
           comments.value.find(comment => comment.id === commentId) ||
           null
  }

  const getRepliesForComment = (commentId) => {
    return commentReplies.value[commentId] || []
  }

  const isReplyLoading = (commentId) => {
    return !!isLoadingReplies.value[commentId]
  }

  // Подсчет комментариев и ответов
  const getCommentDepth = (comment) => {
    let depth = 0
    let current = comment
    
    while (current.parent) {
      depth++
      current = getCommentById(current.parent)
      if (!current) break
    }
    
    return depth
  }

  const getCommentThread = (commentId) => {
    const thread = []
    const comment = getCommentById(commentId)
    
    if (comment) {
      thread.push(comment)
      
      // Получаем все ответы на этот комментарий
      const replies = getCommentsByParent(commentId)
      thread.push(...replies)
      
      // Рекурсивно получаем ответы на ответы
      replies.forEach(reply => {
        const subThread = getCommentThread(reply.id)
        thread.push(...subThread.slice(1)) // Исключаем сам reply, он уже добавлен
      })
    }
    
    return thread
  }

  // Очистка состояния
  const clearComments = () => {
    comments.value = []
  }

  const clearPostComments = () => {
    postComments.value = []
    commentReplies.value = {}
  }

  const clearCurrentComment = () => {
    currentComment.value = null
  }

  const clearMyComments = () => {
    myComments.value = []
  }

  // Кэширование и оптимизация
  const preloadReplies = async (commentIds) => {
    const promises = commentIds
      .filter(id => !commentReplies.value[id] && !isLoadingReplies.value[id])
      .map(id => fetchCommentReplies(id))
    
    await Promise.allSettled(promises)
  }

  const invalidateCommentCache = (commentId) => {
    delete commentReplies.value[commentId]
  }

  return {
    // Состояние
    comments,
    postComments,
    myComments,
    currentComment,
    commentReplies,
    isLoading,
    isLoadingReplies,
    isSubmitting,
    
    // Вычисляемые свойства
    topLevelComments,
    repliesCount,
    totalCommentsCount,
    
    // Основные действия
    fetchComments,
    fetchPostComments,
    fetchCommentById,
    fetchCommentReplies,
    createComment,
    updateComment,
    updateCommentPartial,
    deleteComment,
    fetchMyComments,
    
    // Утилиты
    getCommentsByParent,
    getCommentById,
    getRepliesForComment,
    isReplyLoading,
    getCommentDepth,
    getCommentThread,
    
    // Очистка состояния
    clearComments,
    clearPostComments,
    clearCurrentComment,
    clearMyComments,
    
    // Кэширование и оптимизация
    preloadReplies,
    invalidateCommentCache
  }
})