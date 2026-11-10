/* 轻量全局状态：待选清单、我的标记、收藏、主题、提示 */
import { reactive, watch } from "vue"

const LS_KEY = "hongchen_state_v1"

function load() {
  try {
    return JSON.parse(localStorage.getItem(LS_KEY)) || {}
  } catch {
    return {}
  }
}
const saved = load()

export const state = reactive({
  selectedIds: saved.selectedIds || [],
  markedIds: saved.markedIds || [],
  favoriteIds: saved.favoriteIds || [],
  theme: saved.theme || "light",
  toasts: [],
})

watch(
  () => [
    state.selectedIds,
    state.markedIds,
    state.favoriteIds,
    state.theme,
  ],
  () => {
    localStorage.setItem(
      LS_KEY,
      JSON.stringify({
        selectedIds: state.selectedIds,
        markedIds: state.markedIds,
        favoriteIds: state.favoriteIds,
        theme: state.theme,
      })
    )
  },
  { deep: true }
)

/* 待选清单 */
export function addSelected(id) {
  if (state.selectedIds.includes(id)) return false
  state.selectedIds.push(id)
  return true
}
export function removeSelected(id) {
  const i = state.selectedIds.indexOf(id)
  if (i >= 0) state.selectedIds.splice(i, 1)
}
export function clearSelected() {
  state.selectedIds.splice(0)
}

/* 我的标记 */
export function toggleMarked(id) {
  const i = state.markedIds.indexOf(id)
  if (i >= 0) state.markedIds.splice(i, 1)
  else state.markedIds.push(id)
}

/* 收藏 */
export function toggleFavorite(id) {
  const i = state.favoriteIds.indexOf(id)
  if (i >= 0) state.favoriteIds.splice(i, 1)
  else state.favoriteIds.push(id)
}

/* 轻提示 */
export function showToast(message) {
  const toast = { id: Date.now() + Math.random(), message }
  state.toasts.push(toast)
  setTimeout(() => {
    const i = state.toasts.findIndex((x) => x.id === toast.id)
    if (i >= 0) state.toasts.splice(i, 1)
  }, 2200)
}

export function toggleTheme() {
  state.theme = state.theme === "light" ? "dark" : "light"
}
