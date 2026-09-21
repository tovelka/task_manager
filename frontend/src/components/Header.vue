<template>
  <header class="header">
    <div class="header-content">
      <h1>Task Manager</h1>
      <nav v-if="user">
        <router-link to="/">Главная</router-link>
        <router-link to="/events">События</router-link>
        <span>Привет, {{ user.username }}!</span>
        <button @click="logout">Выйти</button>
      </nav>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const logout = async () => {
  await authStore.logout()
  await router.push('/login')
}
</script>

<style scoped>
.header {
  background-color: #343a40;
  color: white;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.header-content h1 {
  margin: 0;
  font-size: 1.5rem;
}

.header-content nav {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-content a {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.header-content a:hover {
  background-color: rgba(255,255,255,0.1);
}

.header-content button {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.header-content button:hover {
  background-color: #c82333;
}
</style>