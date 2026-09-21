<template>
  <div class="register">
    <h1>Регистрация</h1>
    <form @submit.prevent="register" class="register-form">
      <div>
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="formData.email" required />
      </div>

      <div>
        <label for="username">Имя пользователя:</label>
        <input type="text" id="username" v-model="formData.username" required />
      </div>

      <div>
        <label for="password">Пароль:</label>
        <input type="password" id="password" v-model="formData.password" required />
      </div>

      <div>
        <label for="confirmPassword">Подтвердите пароль:</label>
        <input type="password" id="confirmPassword" v-model="confirmPassword" required />
      </div>

      <button type="submit" :disabled="loading">Зарегистрироваться</button>
    </form>

    <div v-if="error" class="error">{{ error }}</div>
    <div v-if="success" class="success">Регистрация прошла успешно! Пожалуйста, войдите в систему.</div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import type { RegisterRequest } from '@/types'

const authStore = useAuthStore()
const loading = ref(false)
const error = ref<string | null>(null)
const success = ref(false)

const formData = ref<RegisterRequest>({
  email: '',
  password: '',
  username: '',
})

const confirmPassword = ref('')

const register = async () => {
  if (formData.value.password !== confirmPassword.value) {
    error.value = 'Пароли не совпадают'
    return
  }

  loading.value = true
  error.value = null

  try {
    await authStore.register(formData.value)
    success.value = true
  } catch (err) {
    error.value = 'Ошибка регистрации. Пожалуйста, попробуйте еще раз.'
    console.error('Registration error:', err)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register {
  max-width: 500px;
  margin: 2rem auto;
  padding: 2rem;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.register h1 {
  text-align: center;
  color: #333;
  margin-bottom: 1.5rem;
}

.register-form div {
  margin-bottom: 1rem;
}

.register-form label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
  color: #555;
}

.register-form input[type="email"],
.register-form input[type="password"] {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

.checkbox-group {
  margin-bottom: 1rem;
}

.checkbox-group label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: normal;
  color: #555;
}

.checkbox-group input[type="checkbox"] {
  width: auto;
}

.register-form button {
  width: 100%;
  padding: 0.75rem;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.register-form button:hover:not(:disabled) {
  background-color: #218838;
}

.register-form button:disabled {
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

.success {
  margin-top: 1rem;
  padding: 0.75rem;
  background-color: #d4edda;
  color: #155724;
  border-radius: 4px;
  text-align: center;
}
</style>

