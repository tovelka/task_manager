# Создание и использование composable функций в Vue 3

## Что такое Composable функции?

Composable функции - это функции, которые используют реактивные возможности Vue для объединения логики компонентов. Они позволяют переиспользовать логику между компонентами.

## Создание composable функций

### Базовая composable функция

```javascript
// composables/useCounter.js
import { ref, computed } from 'vue'

export function useCounter(initialValue = 0) {
  const count = ref(initialValue)
  
  const increment = () => {
    count.value++
  }
  
  const decrement = () => {
    count.value--
  }
  
  const reset = () => {
    count.value = initialValue
  }
  
  return {
    count,
    increment,
    decrement,
    reset
  }
}
```

### Composable с вычисляемыми свойствами

```javascript
// composables/useUser.js
import { ref, computed } from 'vue'

export function useUser() {
  const user = ref(null)
  
  const isLoggedIn = computed(() => {
    return user.value !== null
  })
  
  const userName = computed(() => {
    return user.value ? user.value.name : 'Гость'
  })
  
  const setUser = (userData) => {
    user.value = userData
  }
  
  const clearUser = () => {
    user.value = null
  }
  
  return {
    user,
    isLoggedIn,
    userName,
    setUser,
    clearUser
  }
}
```

### Composable с эффектами

```javascript
// composables/useLocalStorage.js
import { ref, watch } from 'vue'

export function useLocalStorage(key, defaultValue) {
  const value = ref(defaultValue)
  
  // Чтение из localStorage при инициализации
  const storedValue = localStorage.getItem(key)
  if (storedValue) {
    value.value = JSON.parse(storedValue)
  }
  
  // Сохранение в localStorage при изменении
  watch(value, (newValue) => {
    localStorage.setItem(key, JSON.stringify(newValue))
  }, { deep: true })
  
  return value
}
```

## Использование composable функций в компонентах

### Базовое использование

```vue
<template>
  <div>
    <p>Счётчик: {{ count }}</p>
    <button @click="increment">+</button>
    <button @click="decrement">-</button>
    <button @click="reset">Сброс</button>
  </div>
</template>

<script setup>
import { useCounter } from '@/composables/useCounter'

const { count, increment, decrement, reset } = useCounter(0)
</script>
```

### Использование с API

```vue
<template>
  <div v-if="loading">Загрузка...</div>
  <div v-else-if="error">Ошибка: {{ error }}</div>
  <div v-else>
    <h2>{{ user?.name }}</h2>
    <p>{{ user?.email }}</p>
  </div>
</template>

<script setup>
import { useUser } from '@/composables/useUser'

const { user, loading, error } = useUser()
</script>
```

## Продвинутые composable функции

### Composable с async/await

```javascript
// composables/useFetch.js
import { ref, computed } from 'vue'

export function useFetch(url) {
  const data = ref(null)
  const loading = ref(false)
  const error = ref(null)
  
  const fetchData = async () => {
    loading.value = true
    error.value = null
    
    try {
      const response = await fetch(url)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      data.value = await response.json()
    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }
  
  return {
    data,
    loading,
    error,
    fetchData
  }
}
```

### Composable с watch и computed

```javascript
// composables/useDebounce.js
import { ref, watch } from 'vue'

export function useDebounce(value, delay = 300) {
  const debouncedValue = ref(value)
  
  watch(value, (newValue) => {
    const handler = setTimeout(() => {
      debouncedValue.value = newValue
    }, delay)
    
    return () => clearTimeout(handler)
  })
  
  return debouncedValue
}
```

## Правила и рекомендации

1. **Именование**: Используйте префикс `use` для composable функций
2. **Возврат**: Возвращайте объект с реактивными свойствами и методами
3. **Изоляция**: Composable функции должны быть независимыми
4. **Типизация**: При использовании TypeScript добавляйте типы
5. **Документация**: Документируйте composable функции

## Пример полного компонента с composable

```vue
<template>
  <div>
    <h2>Пользователь: {{ userName }}</h2>
    <p v-if="isLoggedIn">Вы вошли как пользователь</p>
    <p v-else>Вы не авторизованы</p>
    
    <button @click="login">Войти</button>
    <button @click="logout">Выйти</button>
  </div>
</template>

<script setup>
import { useUser } from '@/composables/useUser'

const { user, isLoggedIn, userName, setUser, clearUser } = useUser()

const login = () => {
  setUser({ name: 'Иван', email: 'ivan@example.com' })
}

const logout = () => {
  clearUser()
}
</script>
```
