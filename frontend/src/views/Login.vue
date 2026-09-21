<template>
  <div class="login">
    <h1>Вход</h1>
    <form @submit.prevent="login" class="login-form">
      <div>
        <label for="username">Имя пользователя:</label>
        <input type="text" id="username" v-model="formData.username" required />
      </div>

      <div>
        <label for="password">Пароль:</label>
        <input type="password" id="password" v-model="formData.password" required />
      </div>
      <button type="submit" :disabled="loading">Войти</button>
    </form>

    <div v-if="error" class="error">{{ error }}</div>

    <p class="register-link">
      Нет аккаунта? <router-link to="/register">Зарегистрироваться</router-link>
    </p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()
const loading = ref(false)
const error = ref<string | null>(null)

const formData = ref({
  username: '',
  password: ''
})

    const login = async () => {
  loading.value = true
  error.value = null

      try {
    await authStore.login(formData.value) // Pass the whole object
    await router.push('/home') // Changed to match your route
  } catch (err) {
    error.value = 'Ошибка входа. Пожалуйста, проверьте данные.'
    console.error('Login error:', err)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login {
  max-width: 400px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.login h1 {
  text-align: center;
  color: #333;
  margin-bottom: 1.5rem;
}

.login-form div {
  margin-bottom: 1rem;
}

.login-form label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
  color: #555;
}

.login-form input[id="username"],
.login-form input[type="password"] {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

.login-form button {
  width: 100%;
  padding: 0.75rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.login-form button:hover:not(:disabled) {
  background-color: #0056b3;
}

.login-form button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.error {
  margin-top: 1rem;
  padding: 0.75rem;
  background-color: #f8d7da;
  color: #721c24;
  border-radius: 4px;
  text-align: center;
}

.register-link {
  margin-top: 1rem;
  text-align: center;
}

.register-link a {
  color: #007bff;
  text-decoration: none;
}

.register-link a:hover {
  text-decoration: underline;
}
</style>