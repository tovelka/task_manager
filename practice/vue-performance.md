# Оптимизация производительности Vue 3

## Введение в оптимизацию производительности

Производительность Vue 3 была значительно улучшена по сравнению с Vue 2 благодаря новой системе компиляции и более эффективной реактивности. Однако оптимизация всё ещё важна для создания быстрых приложений.

## Оптимизации компонентов

### Использование мемоизации

```vue
<template>
  <div>{{ expensiveValue }}</div>
</template>

<script setup>
import { computed, memoize } from 'vue'

// Вычисляемые свойства для кэширования
const expensiveValue = computed(() => {
  // Сложная вычислительная операция
  return data.items.reduce((sum, item) => sum + item.value, 0)
})
</script>
```

### Условный рендеринг

```vue
<template>
  <!-- Неэффективно -->
  <div v-if="showDetails">
    <ExpensiveComponent />
  </div>
  
  <!-- Эффективно -->
  <Suspense>
    <template #default>
      <ExpensiveComponent v-if="showDetails" />
    </template>
    <template #fallback>
      <div>Загрузка...</div>
    </template>
  </Suspense>
</template>
```

### Использование v-once для статического контента

```vue
<template>
  <!-- Кэширование статического контента -->
  <div v-once>
    <h1>{{ title }}</h1>
    <p>{{ staticContent }}</p>
  </div>
</template>
```

## Эффективная реактивность

### Избегайте лишних вычислений

```vue
<script setup>
import { ref, computed } from 'vue'

const items = ref([])
const searchTerm = ref('')

// Неэффективно - пересчитывается при каждом изменении
const filteredItems = computed(() => {
  return items.value.filter(item => 
    item.name.toLowerCase().includes(searchTerm.value.toLowerCase())
  )
})

// Эффективно - используем watch для управления обновлениями
const filteredItems = ref([])

watch([items, searchTerm], ([newItems, newSearch]) => {
  filteredItems.value = newItems.filter(item => 
    item.name.toLowerCase().includes(newSearch.toLowerCase())
  )
})
</script>
```

## Оптимизация списков и циклов

### Использование key для списков

```vue
<template>
  <div v-for="item in items" :key="item.id">
    {{ item.name }}
  </div>
</template>

<!-- Хорошо: уникальный ключ -->
<div v-for="user in users" :key="user.id">{{ user.name }}</div>

<!-- Плохо: индекс вместо уникального ключа -->
<div v-for="(item, index) in items" :key="index">{{ item.name }}</div>
```

### Виртуализация списков

```vue
<template>
  <div class="list-container" @scroll="handleScroll">
    <div :style="{ height: totalHeight + 'px' }">
      <div 
        v-for="item in visibleItems" 
        :key="item.id"
        :style="{ top: item.top + 'px' }"
        class="list-item"
      >
        {{ item.name }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const items = ref([])
const containerHeight = ref(300)
const itemHeight = ref(50)

const visibleItems = computed(() => {
  const startIndex = Math.floor(scrollTop.value / itemHeight.value)
  const endIndex = Math.min(
    startIndex + Math.ceil(containerHeight.value / itemHeight.value) + 1,
    items.value.length
  )
  
  return items.value.slice(startIndex, endIndex)
})
</script>
```

## Управление состоянием

### Эффективное использование store

```javascript
// store/userStore.js
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    users: [],
    loading: false,
    error: null
  }),
  
  // Используем getters для вычисляемых значений
  getters: {
    activeUsers: (state) => {
      return state.users.filter(user => user.active)
    },
    
    userCount: (state) => {
      return state.users.length
    }
  },
  
  actions: {
    async fetchUsers() {
      this.loading = true
      try {
        const response = await fetch('/api/users')
        this.users = await response.json()
      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    }
  }
})
```

## Ленивая загрузка компонентов

### Динамическая импортация

```vue
<template>
  <component :is="dynamicComponent" />
</template>

<script setup>
import { ref, defineAsyncComponent } from 'vue'

// Ленивая загрузка компонента
const dynamicComponent = defineAsyncComponent(() => 
  import('./HeavyComponent.vue')
)

// Или с опциями
const HeavyComponent = defineAsyncComponent({
  loader: () => import('./HeavyComponent.vue'),
  loadingComponent: LoadingSpinner,
  errorComponent: ErrorComponent,
  delay: 200,
  timeout: 3000
})
</script>
```

## Использование Suspense

```vue
<template>
  <Suspense>
    <template #default>
      <AsyncComponent />
    </template>
    <template #fallback>
      <div>Загрузка...</div>
    </template>
  </Suspense>
</template>

<script setup>
import { defineAsyncComponent } from 'vue'

const AsyncComponent = defineAsyncComponent(() => 
  import('./AsyncComponent.vue')
)
</script>
```

## Профилирование производительности

### Использование Vue DevTools

```javascript
// Включение профилирования
import { createApp } from 'vue'

const app = createApp(App)

if (process.env.NODE_ENV === 'development') {
  app.config.performance = true
}
```

### Мониторинг производительности

```javascript
// Мониторинг рендеринга
import { onRenderTracked, onRenderTriggered } from 'vue'

onRenderTracked((event) => {
  console.log('Отслежено изменение:', event)
})

onRenderTriggered((event) => {
  console.log('Триггер рендера:', event)
})
```

## Практические советы

1. **Используйте computed для вычисляемых значений**
2. **Избегайте сложных вычислений в шаблоне**
3. **Оптимизируйте списки с помощью key**
4. **Используйте lazy loading для тяжелых компонентов**
5. **Управляйте состоянием эффективно**
6. **Используйте v-once для статического контента**
7. **Тестируйте производительность на реальных данных**

## Инструменты для оптимизации

1. **Vue DevTools** - для профилирования
2. **Chrome DevTools** - для анализа производительности
3. **Lighthouse** - для автоматической проверки
4. **Vite** - для быстрой сборки
5. **Pinia** - для эффективного управления состоянием

## Мониторинг производительности

```javascript
// Простая функция для измерения времени
function measurePerformance(name, fn) {
  const start = performance.now()
  const result = fn()
  const end = performance.now()
  console.log(`${name}: ${end - start}ms`)
  return result
}

// Использование
const expensiveOperation = () => {
  // Сложная операция
  return data.reduce((sum, item) => sum + item.value, 0)
}

measurePerformance('Суммирование данных', expensiveOperation)
```
