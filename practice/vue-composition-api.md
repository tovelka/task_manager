# Vue 3 Composition API

## Введение в Composition API

Composition API - это новый способ организации кода в Vue 3, который предоставляет более гибкий и мощный способ создания компонентов по сравнению с Options API. Он позволяет лучше организовать логику компонента, повторно использовать логику между компонентами и улучшить читаемость сложных компонентов.

## Основные принципы

### 1. Реактивность
Composition API использует функции `ref` и `reactive` для создания реактивных данных:

```javascript
import { ref, reactive } from 'vue'

// Создание реактивной переменной
const count = ref(0)
const user = reactive({ name: 'John', age: 30 })
```

### 2. Функции `setup`
Функция `setup` является точкой входа для Composition API. Она выполняется до создания экземпляра компонента:

```javascript
import { ref, computed } from 'vue'

export default {
  setup() {
    const count = ref(0)
    
    // Вычисляемые свойства
    const doubleCount = computed(() => count.value * 2)
    
    // Методы
    const increment = () => {
      count.value++
    }
    
    // Возвращаем данные, которые будут доступны в шаблоне
    return {
      count,
      doubleCount,
      increment
    }
  }
}
```

### 3. Ссылки (Refs)
Функция `ref` используется для создания реактивной ссылки на примитивные значения:

```javascript
import { ref } from 'vue'

const name = ref('John')
console.log(name.value) // 'John'
name.value = 'Jane'     // Изменение значения
```

### 4. Реактивные объекты (Reactive)
Функция `reactive` создает реактивный объект:

```javascript
import { reactive } from 'vue'

const state = reactive({
  count: 0,
  user: {
    name: 'John',
    age: 30
  }
})
```

### 5. Вычисляемые свойства (Computed)
Функция `computed` создает вычисляемое свойство, которое автоматически обновляется при изменении зависимостей:

```javascript
import { ref, computed } from 'vue'

const firstName = ref('John')
const lastName = ref('Doe')

const fullName = computed(() => {
  return `${firstName.value} ${lastName.value}`
})
```

### 6. Эффекты (Effects)
Функция `watch` отслеживает изменения реактивных данных:

```javascript
import { ref, watch } from 'vue'

const count = ref(0)

// Наблюдение за одним значением
watch(count, (newValue, oldValue) => {
  console.log(`Count changed from ${oldValue} to ${newValue}`)
})

// Наблюдение за несколькими значениями
const firstName = ref('John')
const lastName = ref('Doe')

watch([firstName, lastName], ([newFirstName, newLastName], [oldFirstName, oldLastName]) => {
  console.log(`Name changed from ${oldFirstName} ${oldLastName} to ${newFirstName} ${newLastName}`)
})
```

### 7. Управление жизненным циклом
В Composition API можно использовать функции жизненного цикла:

```javascript
import { onMounted, onUnmounted, onUpdated } from 'vue'

export default {
  setup() {
    onMounted(() => {
      console.log('Component mounted')
    })
    
    onUnmounted(() => {
      console.log('Component unmounted')
    })
    
    return {}
  }
}
```

## Преимущества Composition API

1. **Лучшая организация кода** - логика может быть разделена по функциональным группам
2. **Улучшенное повторное использование логики** - можно создавать composable функции
3. **Более гибкая типизация** - особенно полезно с TypeScript
4. **Упрощение сложных компонентов** - легче разделять логику между компонентами

## Composable функции

Composable функции - это переиспользуемые функции, которые содержат логику компонента:

```javascript
// composables/useCounter.js
import { ref, computed } from 'vue'

export function useCounter(initialValue = 0) {
  const count = ref(initialValue)
  
  const doubleCount = computed(() => count.value * 2)
  
  const increment = () => {
    count.value++
  }
  
  const decrement = () => {
    count.value--
  }
  
  return {
    count,
    doubleCount,
    increment,
    decrement
  }
}

// Использование в компоненте
import { useCounter } from '@/composables/useCounter'

export default {
  setup() {
    const { count, doubleCount, increment, decrement } = useCounter(10)
    
    return {
      count,
      doubleCount,
      increment,
      decrement
    }
  }
}
```

## Сравнение с Options API

| Feature | Options API | Composition API |
|---------|-------------|-----------------|
| Организация кода | По опциям (data, methods, computed) | По функциональным группам |
| Повторное использование | Mixins, extends | Composables |
| Читаемость | Для простых компонентов | Для сложных компонентов |
| Типизация | Ограниченная | Полная поддержка TypeScript |

## Рекомендации по использованию

1. **Используйте Composition API для сложных компонентов** - он лучше организует сложную логику
2. **Создавайте переиспользуемые composable функции** - для повторного использования логики
3. **Сохраняйте совместимость** - Vue 3 поддерживает как Options API, так и Composition API
4. **Используйте правильные инструменты** - DevTools и TypeScript для лучшего опыта разработки

## Заключение

Composition API представляет собой мощный инструмент для организации кода в Vue 3. Он предоставляет более гибкий способ создания компонентов, особенно полезен для сложных приложений с повторяющейся логикой.