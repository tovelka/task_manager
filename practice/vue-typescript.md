# Использование TypeScript с Vue 3

## Введение в TypeScript и Vue 3

TypeScript добавляет статическую типизацию в JavaScript, что помогает выявлять ошибки на этапе разработки и улучшает качество кода. Vue 3 имеет отличную поддержку TypeScript.

## Настройка проекта с TypeScript

### Установка зависимостей

```bash
# Если используете Vite
npm create vue@latest my-project -- --typescript

# Или для существующего проекта
npm install --save-dev typescript @vue/cli-plugin-typescript
```

### Конфигурация tsconfig.json

```json
{
  "compilerOptions": {
    "target": "esnext",
    "module": "esnext",
    "moduleResolution": "node",
    "strict": true,
    "jsx": "preserve",
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "types": ["vite/client"],
    "lib": ["esnext", "dom"]
  },
  "include": ["src/**/*", "src/**/*.vue"],
  "exclude": ["node_modules"]
}
```

## Типизация компонентов

### Базовый компонент с типами

```vue
<template>
  <div>
    <h1>{{ title }}</h1>
    <p>{{ message }}</p>
    <button @click="handleClick">Кликни меня</button>
  </div>
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits } from 'vue'

// Типизация props
interface Props {
  title: string
  count?: number
}

const props = defineProps<Props>()

// Типизация emit
interface Emits {
  (e: 'click', value: string): void
  (e: 'update:count', value: number): void
}

const emit = defineEmits<Emits>()

// Типизация реактивных данных
const message = ref<string>('Привет, мир!')
const handleClick = () => {
  emit('click', 'Кнопка нажата')
}
</script>
```

### С использованием defineProps с типами

```vue
<script setup lang="ts">
// Простая типизация
const props = defineProps({
  name: String,
  age: Number,
  isActive: Boolean
})

// С указанием типов
const props = defineProps<{
  title: string
  count?: number
  items: string[]
  callback?: (value: string) => void
}>()

// Использование с типом
const { title, count = 0 } = props
</script>
```

## Типизация вычисляемых свойств и методов

```vue
<script setup lang="ts">
import { ref, computed } from 'vue'

const firstName = ref<string>('Иван')
const lastName = ref<string>('Иванов')

// Типизация вычисляемого свойства
const fullName = computed<string>(() => {
  return `${firstName.value} ${lastName.value}`
})

// Типизация метода
const handleUpdate = (value: string): void => {
  console.log(value)
}

// Типизация асинхронной функции
const fetchData = async (): Promise<string[]> => {
  const response = await fetch('/api/data')
  const data = await response.json()
  return data.items
}
</script>
```

## Типизация Composition API

### Типизация ref и reactive

```typescript
import { ref, reactive } from 'vue'

// Типизация ref
const count = ref<number>(0)
const message = ref<string>('Привет')
const user = ref<{ name: string; age: number } | null>(null)

// Типизация reactive
const state = reactive({
  count: 0,
  items: [] as string[],
  loading: false
})

// Использование с интерфейсами
interface User {
  id: number
  name: string
  email: string
}

const user = ref<User | null>(null)
```

### Типизация composable функций

```typescript
// composables/useUser.ts
import { ref, computed } from 'vue'

interface User {
  id: number
  name: string
  email: string
}

interface UserStore {
  user: User | null
  loading: boolean
  error: string | null
  fetchUser: (id: number) => Promise<void>
}

export function useUser(): UserStore {
  const user = ref<User | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)
  
  const fetchUser = async (id: number): Promise<void> => {
    loading.value = true
    error.value = null
    
    try {
      const response = await fetch(`/api/users/${id}`)
      user.value = await response.json()
    } catch (err) {
      error.value = err.message
    } finally {
      loading.value = false
    }
  }
  
  return {
    user,
    loading,
    error,
    fetchUser
  }
}
```

## Типизация событий и эмитов

```vue
<script setup lang="ts">
import { defineProps, defineEmits } from 'vue'

// С типизированными эмитами
const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
  (e: 'save', data: { id: number; name: string }): void
  (e: 'delete', id: number): void
}>()

// Использование в шаблоне
const handleSave = () => {
  emit('save', { id: 1, name: 'Пример' })
}
</script>

<template>
  <button @click="handleSave">Сохранить</button>
</template>
```

## Типизация с Composition API и Options API

### Комбинирование подходов

```vue
<script setup lang="ts">
import { ref, computed } from 'vue'

// Используем Composition API
const count = ref(0)
const doubled = computed(() => count.value * 2)

// Возвращаем объект для использования в Options API
const api = {
  count,
  doubled
}
</script>
```

## Работа с типами из библиотек

### Использование типов из внешних библиотек

```typescript
// Для работы с Axios
import axios, { AxiosResponse } from 'axios'

interface User {
  id: number
  name: string
}

const fetchUser = async (id: number): Promise<AxiosResponse<User>> => {
  return await axios.get(`/api/users/${id}`)
}
```

## Типизация маршрутов и роутера

```typescript
// router/index.ts
import { createRouter, createWebHistory } from 'vue-router'

interface RouteConfig {
  path: string
  name: string
  component: () => Promise<any>
}

const routes: RouteConfig[] = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})
```

## Типизация Vuex/Store

```typescript
// store/index.ts
import { defineStore } from 'pinia'

interface State {
  count: number
  user: User | null
}

export const useMainStore = defineStore('main', {
  state: (): State => ({
    count: 0,
    user: null
  }),
  
  getters: {
    isLoggedIn: (state) => state.user !== null,
    userName: (state) => state.user?.name || ''
  },
  
  actions: {
    increment() {
      this.count++
    }
  }
})
```

## Практические советы

1. **Используйте интерфейсы для структур данных**
2. **Типизируйте все props и emits**
3. **Используйте строгую типизацию (strict: true)**
4. **Не бойтесь использовать any, когда это необходимо**
5. **Пишите типы для сложных функций и методов**
6. **Используйте utility types из TypeScript**

## Полезные utility types

```typescript
// Partial - делает все свойства необязательными
interface User {
  name: string
  age: number
}

const partialUser: Partial<User> = { name: 'Иван' }

// Pick - выбирает определенные свойства
const userWithOnlyName: Pick<User, 'name'> = { name: 'Иван' }

// Omit - исключает определенные свойства
const userWithoutAge: Omit<User, 'age'> = { name: 'Иван' }

// Readonly - делает объект неизменяемым
const readonlyUser: Readonly<User> = { name: 'Иван', age: 30 }
```
