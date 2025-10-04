<template>
  <header class="nav-header">
    <div class="nav-container">
      <router-link to="/" class="logo-link">
        <img src="../assets/images/nasa-logo.svg" alt="NASA" class="nasa-logo" />
        <span class="app-title">Challenge 2025</span>
      </router-link>

      <nav class="nav-links">
        <router-link to="/" class="nav-link">Home</router-link>
      </nav>
    </div>
  </header>
</template>

<script setup lang="ts">
</script>

<style scoped>
.nav-header {
  background-color: #000000;
  border-bottom: 1px solid #2a2a2a;
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(10px);
}

.nav-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo-link {
  display: flex;
  align-items: center;
  gap: 1rem;
  text-decoration: none;
  transition: opacity 0.2s;
}

.logo-link:hover {
  opacity: 0.8;
}

.nasa-logo {
  height: 50px;
  width: auto;
}

.app-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #d1d1d1;
  letter-spacing: 0.5px;
}

.nav-links {
  display: flex;
  gap: 2rem;
  align-items: center;
}

.nav-link {
  color: #d1d1d1;
  text-decoration: none;
  font-size: 0.95rem;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: all 0.2s;
}

.nav-link:hover {
  color: #288bff;
  background-color: rgba(40, 139, 255, 0.1);
}

.nav-link.router-link-active {
  color: #288bff;
}

@media (max-width: 768px) {
  .nav-container {
    padding: 1rem;
  }

  .nasa-logo {
    height: 40px;
  }

  .app-title {
    font-size: 1rem;
  }

  .nav-links {
    gap: 1rem;
  }

  .nav-link {
    padding: 0.5rem;
    font-size: 0.875rem;
  }
}

@media (max-width: 480px) {
  .app-title {
    display: none;
  }
}
</style>
