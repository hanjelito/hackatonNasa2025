<template>
  <button @click="$emit('click')" class="filter-tag" :class="tagType">
    {{ label }}: {{ value }}
  </button>
</template>

<script setup lang="ts">
defineProps<{
  label: string
  value: string | number
  tagType: 'year' | 'organism'
}>()

defineEmits<{
  'click': []
}>()
</script>

<style scoped>
@import '../assets/css/filter-tag.css';
</style>
