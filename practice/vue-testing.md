# Тестирование компонентов Vue 3

## Введение в тестирование Vue 3

Тестирование компонентов Vue 3 важно для обеспечения качества кода и предотвращения регрессий. Vue предоставляет инструменты для тестирования как с использованием Jest, так и с Cypress.

## Установка зависимостей

```bash
# Для Jest
npm install --save-dev jest @vue/test-utils vue-jest

# Для Cypress
npm install --save-dev cypress @cypress/vue

# Для Vitest (современный вариант)
npm install --save-dev vitest @vitejs/plugin-vue jsdom
```

## Тестирование компонентов с Jest

### Базовый пример теста

```vue
<!-- Button.vue -->
<template>
  <button @click="handleClick" :disabled="disabled">
    {{ label }}
  </button>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  label: String,
  disabled: Boolean
})

const emit = defineEmits(['click'])

const handleClick = () => {
  emit('click')
}
</script>
```

```javascript
// Button.spec.js
import { mount } from '@vue/test-utils'
import Button from './Button.vue'

describe('Button', () => {
  test('renders button with correct label', () => {
    const wrapper = mount(Button, {
      props: { label: 'Click me' }
    })
    
    expect(wrapper.text()).toContain('Click me')
  })

  test('emits click event when clicked', async () => {
    const wrapper = mount(Button)
    
    await wrapper.find('button').trigger('click')
    
    expect(wrapper.emitted('click')).toHaveLength(1)
  })

  test('is disabled when disabled prop is true', () => {
    const wrapper = mount(Button, {
      props: { disabled: true }
    })
    
    expect(wrapper.find('button').attributes('disabled')).toBeDefined()
  })
})
```

## Тестирование вычисляемых свойств и методов

```vue
<!-- UserCard.vue -->
<template>
  <div class="user-card">
    <h3>{{ fullName }}</h3>
    <p>{{ userRole }}</p>
    <button @click="updateUser">Обновить</button>
  </div>
</template>

<script setup>
import { computed, defineProps } from 'vue'

const props = defineProps({
  user: {
    type: Object,
    required: true
  }
})

const fullName = computed(() => {
  return `${props.user.firstName} ${props.user.lastName}`
})

const userRole = computed(() => {
  return props.user.isAdmin ? 'Администратор' : 'Пользователь'
})

const updateUser = () => {
  // Логика обновления пользователя
}
</script>
```

```javascript
// UserCard.spec.js
import { mount } from '@vue/test-utils'
import UserCard from './UserCard.vue'

describe('UserCard', () => {
  const user = {
    firstName: 'Иван',
    lastName: 'Иванов',
    isAdmin: true
  }

  test('renders full name correctly', () => {
    const wrapper = mount(UserCard, {
      props: { user }
    })
    
    expect(wrapper.text()).toContain('Иван Иванов')
  })

  test('displays admin role for admin user', () => {
    const wrapper = mount(UserCard, {
      props: { user }
    })
    
    expect(wrapper.text()).toContain('Администратор')
  })

  test('calls updateUser method when button is clicked', async () => {
    const wrapper = mount(UserCard, {
      props: { user }
    })
    
    const updateUserSpy = jest.spyOn(wrapper.vm, 'updateUser')
    
    await wrapper.find('button').trigger('click')
    
    expect(updateUserSpy).toHaveBeenCalled()
  })
})
```

## Тестирование с асинхронными операциями

```vue
<!-- AsyncComponent.vue -->
<template>
  <div>
    <div v-if="loading">Загрузка...</div>
    <div v-else-if="error">Ошибка: {{ error }}</div>
    <div v-else>{{ data }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const loading = ref(true)
const error = ref(null)
const data = ref(null)

const fetchData = async () => {
  try {
    const response = await fetch('/api/data')
    data.value = await response.json()
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchData()
})
</script>
```

```javascript
// AsyncComponent.spec.js
import { mount } from '@vue/test-utils'
import AsyncComponent from './AsyncComponent.vue'

// Mock fetch
global.fetch = jest.fn()

describe('AsyncComponent', () => {
  beforeEach(() => {
    fetch.mockClear()
  })

  test('displays loading state initially', () => {
    const wrapper = mount(AsyncComponent)
    
    expect(wrapper.text()).toContain('Загрузка...')
  })

  test('displays data when fetch is successful', async () => {
    fetch.mockResolvedValueOnce({
      json: () => Promise.resolve({ message: 'Hello' })
    })

    const wrapper = mount(AsyncComponent)
    
    await wrapper.vm.$nextTick()
    
    expect(wrapper.text()).toContain('Hello')
  })

  test('displays error when fetch fails', async () => {
    fetch.mockRejectedValueOnce(new Error('Network error'))

    const wrapper = mount(AsyncComponent)
    
    await wrapper.vm.$nextTick()
    
    expect(wrapper.text()).toContain('Ошибка')
  })
})
```

## Тестирование компонентов с Composition API

```vue
<!-- Counter.vue -->
<template>
  <div>
    <p>Счётчик: {{ count }}</p>
    <button @click="increment">+</button>
    <button @click="decrement">-</button>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const count = ref(0)

const increment = () => {
  count.value++
}

const decrement = () => {
  count.value--
}
</script>
```

```javascript
// Counter.spec.js
import { mount } from '@vue/test-utils'
import Counter from './Counter.vue'

describe('Counter', () => {
  test('increments counter when increment button is clicked', async () => {
    const wrapper = mount(Counter)
    
    await wrapper.find('button').trigger('click')
    
    expect(wrapper.text()).toContain('Счётчик: 1')
  })

  test('decrements counter when decrement button is clicked', async () => {
    const wrapper = mount(Counter)
    
    await wrapper.findAll('button')[1].trigger('click')
    
    expect(wrapper.text()).toContain('Счётчик: -1')
  })

  test('initial count is 0', () => {
    const wrapper = mount(Counter)
    
    expect(wrapper.text()).toContain('Счётчик: 0')
  })
})
```

## Тестирование с использованием Vue Test Utils

### Тестирование событий

```javascript
const wrapper = mount(Component, {
  props: { 
    value: 'test'
  }
})

// Проверка события
wrapper.vm.$emit('input', 'new value')
expect(wrapper.emitted('input')[0]).toEqual(['new value'])
```

### Тестирование props

```javascript
const wrapper = mount(Component, {
  props: {
    title: 'Заголовок',
    disabled: true,
    items: ['item1', 'item2']
  }
})

expect(wrapper.props('title')).toBe('Заголовок')
expect(wrapper.props('disabled')).toBe(true)
```

## Использование Vitest (современный подход)

```javascript
// Counter.test.js
import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import Counter from './Counter.vue'

describe('Counter', () => {
  it('increments counter when button is clicked', async () => {
    const wrapper = mount(Counter)
    
    await wrapper.find('button').trigger('click')
    
    expect(wrapper.text()).toContain('Счётчик: 1')
  })
})
```

## Рекомендации по тестированию

1. **Тестируйте поведение, а не реализацию**
2. **Используйте минимальные компоненты для тестирования**
3. **Не тестируйте встроенные директивы Vue**
4. **Тестируйте асинхронные операции**
5. **Используйте моки для внешних зависимостей**
6. **Покрывайте критические пути**

## Покрытие кода

```bash
# Запуск тестов с покрытием
jest --coverage

# Использование Vitest
vitest run --coverage
```
