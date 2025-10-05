<template>
  <button @click="$emit('click')" class="search-button">
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="search-icon">
      <path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z" />
    </svg>
  </button>
</template>

<script setup lang="ts">
defineEmits<{
  'click': []
}>()
</script>

<style scoped>
.search-button {
  background-color: #0b3d91;
  color: white;
  padding: 0.75rem;
  border-radius: 0.5rem;
  font-weight: 600;
  transition: all 0.2s;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 48px;
  height: 48px;
}

.search-button:hover {
  background-color: #083073;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(11, 61, 145, 0.3);
}

.search-button:active {
  transform: translateY(0);
}

.search-icon {
  width: 20px;
  height: 20px;
}
</style>
