<template>
  <div class="multiselect-filter" ref="containerRef">
    <div class="multiselect-container">
      <div class="selected-items" @click.stop="toggleDropdown">
        <span v-if="selectedValues.length === 0" class="placeholder">
          Select {{ label.toLowerCase() }}...
        </span>
        <span v-else class="selected-count">
          {{ selectedValues.length }} {{ label.toLowerCase() }} selected
        </span>
        <span class="dropdown-arrow">▼</span>
      </div>

      <div v-if="isOpen" class="dropdown-menu">
        <div
          v-for="option in options"
          :key="option"
          class="dropdown-item"
          @click.stop="toggleOption(option)"
        >
          <input
            type="checkbox"
            :checked="isSelected(option)"
            @click.stop
          />
          <span>{{ option }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps<{
  id: string
  label: string
  options: (string | number)[]
  modelValue: (string | number)[]
}>()

const emit = defineEmits<{
  'update:modelValue': [value: (string | number)[]]
}>()

const isOpen = ref(false)
const containerRef = ref<HTMLElement | null>(null)

const selectedValues = computed(() => props.modelValue || [])

const toggleDropdown = () => {
  if (!isOpen.value) {
    // Emit custom event to close other dropdowns
    document.dispatchEvent(new CustomEvent('multiselect-open', { detail: { id: props.id } }))
  }
  isOpen.value = !isOpen.value
}

const closeDropdown = () => {
  isOpen.value = false
}

const isSelected = (option: string | number) => {
  return selectedValues.value.includes(option)
}

const toggleOption = (option: string | number) => {
  const current = [...selectedValues.value]
  const index = current.indexOf(option)

  if (index > -1) {
    current.splice(index, 1)
  } else {
    current.push(option)
  }

  emit('update:modelValue', current)
}

const handleClickOutside = (event: MouseEvent) => {
  if (containerRef.value && !containerRef.value.contains(event.target as Node)) {
    closeDropdown()
  }
}

const handleMultiselectOpen = (event: Event) => {
  const customEvent = event as CustomEvent
  if (customEvent.detail.id !== props.id) {
    closeDropdown()
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  document.addEventListener('multiselect-open', handleMultiselectOpen as EventListener)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  document.removeEventListener('multiselect-open', handleMultiselectOpen as EventListener)
})
</script>

<style scoped>
.multiselect-filter {
  margin-bottom: 1.25rem;
}

.multiselect-container {
  position: relative;
}

.selected-items {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  border: 2px solid #2a2a2a;
  border-radius: 6px;
  background: #2a2a2a;
  color: #d1d1d1;
  cursor: pointer;
  transition: all 0.2s;
}

.selected-items:hover {
  border-color: #288bff;
  background: #1a1a1a;
}

.placeholder {
  color: #959599;
}

.selected-count {
  color: #288bff;
  font-weight: 600;
}

.dropdown-arrow {
  font-size: 0.75rem;
  color: #959599;
  transition: transform 0.2s;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  margin-top: 0.5rem;
  max-height: 240px;
  overflow-y: auto;
  background: #1a1a1a;
  border: 1px solid #2a2a2a;
  border-radius: 6px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
  z-index: 10;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  color: #d1d1d1;
  cursor: pointer;
  transition: background-color 0.2s;
}

.dropdown-item:hover {
  background-color: rgba(40, 139, 255, 0.1);
}

.dropdown-item input[type="checkbox"] {
  cursor: pointer;
  accent-color: #288bff;
  width: 1.125rem;
  height: 1.125rem;
}
</style>
