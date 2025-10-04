<template>
  <button @click="$emit('click')" class="search-button">
    <slot>Search</slot>
  </button>
</template>

<script setup lang="ts">
defineEmits<{
  'click': []
}>()
</script>

<style scoped>
@import '../assets/css/search-button.css';
</style>
