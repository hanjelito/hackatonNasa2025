<template>
  <div class="search-input">
    <input
      :value="modelValue"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
      type="text"
      :placeholder="placeholder"
      @keyup.enter="$emit('search')"
    />
  </div>
</template>

<script setup lang="ts">
defineProps<{
  modelValue: string
  placeholder?: string
}>()

defineEmits<{
  'update:modelValue': [value: string]
  'search': []
}>()
</script>

<style scoped>
@import '../assets/css/search-input.css';
</style>
