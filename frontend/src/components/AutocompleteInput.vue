<template>
  <div class="autocomplete-input">
    <label :for="id" class="input-label">{{ label }}</label>
    <input
      :id="id"
      v-model="inputValue"
      type="text"
      :placeholder="placeholder"
      @input="handleInput"
      @focus="handleFocus"
      @blur="handleBlur"
    />
    <div v-if="shouldShowSuggestions" class="suggestions-list">
      <div
        v-for="option in filteredOptions"
        :key="option"
        class="suggestion-item"
        @mousedown="selectOption(option)"
      >
        {{ option }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const props = defineProps<{
  id: string
  label: string
  placeholder: string
  options: (string | number)[]
  modelValue: string | number | undefined
  minChars?: number
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string | number | undefined]
}>()

const inputValue = ref(props.modelValue?.toString() || '')
const showSuggestions = ref(false)
const minCharacters = props.minChars || 3

const filteredOptions = computed(() => {
  if (!inputValue.value) return []

  return props.options.filter(option =>
    option.toString().toLowerCase().includes(inputValue.value.toLowerCase())
  )
})

const shouldShowSuggestions = computed(() => {
  return showSuggestions.value &&
         inputValue.value.length >= minCharacters &&
         filteredOptions.value.length > 0
})

const handleInput = () => {
  if (!inputValue.value) {
    emit('update:modelValue', undefined)
    showSuggestions.value = false
  } else if (inputValue.value.length >= minCharacters) {
    showSuggestions.value = true
  }
}

const handleFocus = () => {
  if (inputValue.value.length >= minCharacters) {
    showSuggestions.value = true
  }
}

const selectOption = (option: string | number) => {
  inputValue.value = option.toString()
  emit('update:modelValue', option)
  showSuggestions.value = false
}

// Validar que el valor ingresado existe en las opciones
const validateInput = () => {
  if (inputValue.value) {
    const exactMatch = props.options.find(
      option => option.toString().toLowerCase() === inputValue.value.toLowerCase()
    )
    if (!exactMatch) {
      emit('update:modelValue', undefined)
    }
  }
}

const handleBlur = () => {
  setTimeout(() => {
    showSuggestions.value = false
    validateInput()
  }, 200)
}
</script>

<style scoped>
@import '../assets/css/autocomplete-input.css';
</style>
