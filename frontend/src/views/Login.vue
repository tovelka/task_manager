<template>
  <div class="login">
    <h1>Вход</h1>
    <form @submit.prevent="login">
      <div>
        <label for="username">Имя пользователя</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div>
        <label for="password">Пароль</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit">Войти</button>
    </form>
    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import type { UserResponse, LoginRequest, RegisterRequest } from '@/types'
import { useAuthStore } from '../stores/auth';

const createLoginRequest = (username: string, password: string): LoginRequest => ({
  username,
  password
});

export default defineComponent({
  name: 'Login',
  setup() {
    const username = ref('');
    const password = ref('');
    const error = ref<string | null>(null);
    const authStore = useAuthStore();

    const login = async () => {
      try {
        const request = createLoginRequest(username.value, password.value);
        await authStore.login(request);
        username.value = '';
        password.value = '';
        error.value = null;
      } catch (err: unknown) {
        if (err instanceof Error) {
          error.value = err.message;
        } else {
          error.value = 'Произошла неизвестная ошибка';
        }
      }
    };

    return {
      username,
      password,
      error,
      login
    };
  }
});
</script>

<style scoped>
.login {
  max-width: 300px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.error {
  color: red;
}
</style>