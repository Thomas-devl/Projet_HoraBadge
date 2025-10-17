import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useMainStore = defineStore('main', () => {
  // State
  const count = ref(0)
  const user = ref(null)

  // Actions
  function increment() {
    count.value++
  }

  function setUser(userData) {
    user.value = userData
  }

  // Getters
  const doubleCount = computed(() => count.value * 2)

  return {
    count,
    user,
    increment,
    setUser,
    doubleCount
  }
})
