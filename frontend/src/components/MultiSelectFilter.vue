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

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.multiselect-filter {
  margin-bottom: 1rem;
}

.multiselect-container {
  position: relative;
}

.selected-items {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
  cursor: pointer;
  transition: border-color 0.2s;
}

.selected-items:hover {
  border-color: #0066cc;
}

.placeholder {
  color: #999;
}

.selected-count {
  color: #0066cc;
  font-weight: 500;
}

.dropdown-arrow {
  font-size: 0.75rem;
  color: #666;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  margin-top: 0.25rem;
  max-height: 200px;
  overflow-y: auto;
  background: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  z-index: 10;
}

.dropdown-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.dropdown-item:hover {
  background-color: #f5f5f5;
}

.dropdown-item input[type="checkbox"] {
  cursor: pointer;
}
</style>
