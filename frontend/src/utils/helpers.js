/**
 * Format date to locale string
 * @param {Date|string} date
 * @returns {string}
 */
export function formatDate(date) {
  return new Date(date).toLocaleDateString()
}

/**
 * Debounce function
 * @param {Function} func
 * @param {number} wait
 * @returns {Function}
 */
export function debounce(func, wait) {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}
