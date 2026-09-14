# Vue 3 Reactivity System

## Введение в реактивность

Vue 3 использует новый механизм реактивности, основанный на Proxy и Reflect API. Это дает более мощные возможности по сравнению с Vue 2, где использовался Object.defineProperty.

## Как работает реактивность в Vue 3

### 1. Прокси (Proxy) и Reflect
Vue 3 использует Proxy для создания реактивных объектов:

```javascript
// Внутренняя реализация Vue
const target = { name: 'John', age: 30 }
const observed = new Proxy(target, {
  get(target, key, receiver) {
    // Логика отслеживания зависимостей
    console.log(`Reading ${key}`)
    return Reflect.get(target, key, receiver)
  },
  set(target, key, value, receiver) {
    // Логика обновления зависимостей
    console.log(`Setting ${key} to ${value}`)
    return Reflect.set(target, key, value, receiver)
  }
})
```

### 2. Создание реактивных данных

#### ref()
Функция `ref` создает реактивную ссылку на значение:

```javascript
import { ref } from 'vue'

const count = ref(0)
console.log(count.value) // 0

count.value = 5
// При изменении значения, все зависимые части обновляются автоматически
```

#### reactive()
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

state.count = 5 // Обновление значения
```

### 3. Реактивные массивы

Vue 3 автоматически делает массивы реактивными:

```javascript
import { reactive } from 'vue'

const list = reactive([1, 2, 3])
list.push(4) // Этот метод будет отслеживаться реактивностью
```

### 4. Глубокая реактивность

По умолчанию `reactive` создает глубоко реактивный объект:

```javascript
import { reactive } from 'vue'

const state = reactive({
  user: {
    profile: {
      name: 'John'
    }
  }
})

// Все уровни вложенности реактивны
state.user.profile.name = 'Jane' // Автоматическое обновление
```

### 5. Система отслеживания зависимостей

Vue 3 использует систему отслеживания зависимостей:

```javascript
// Когда компонент читает значение ref или reactive свойства,
// он добавляется в список зависимостей
const count = ref(0)

// При использовании в шаблоне или вычисляемом свойстве
// Vue автоматически отслеживает зависимости
```

### 6. Компоненты и реактивность

```javascript
import { ref, computed } from 'vue'

export default {
  setup() {
    const count = ref(0)
    const doubled = computed(() => count.value * 2)
    
    // Когда count меняется, doubled автоматически пересчитывается
    
    const increment = () => {
      count.value++
    }
    
    return {
      count,
      doubled,
      increment
    }
  }
}
```

## Основные особенности

### 1. Поддержка примитивов
В отличие от Vue 2, `ref` может работать с примитивами:

```javascript
const name = ref('John') // Создает ссылку на строку
const count = ref(0)      // Создает ссылку на число

// Использование в шаблоне
// {{ name }} // Работает напрямую
// {{ name.value }} // Нужно только если используете внутри JavaScript
```

### 2. Передача ссылок в функции
Функции могут принимать ссылки и работать с ними:

```javascript
function useCounter(initialValue) {
  const count = ref(initialValue)
  
  function increment() {
    count.value++ // Нужно использовать .value
  }
  
  return { count, increment }
}
```

### 3. Использование в шаблонах
```vue
<template>
  <div>
    <p>{{ count }}</p> <!-- Автоматически отслеживает count -->
    <p>{{ doubled }}</p> <!-- Автоматически отслеживает doubled -->
    <button @click="increment">Increment</button>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const count = ref(0)
const doubled = computed(() => count.value * 2)

function increment() {
  count.value++
}
</script>
```

## Преимущества новой системы реактивности

1. **Более высокая производительность** - меньшее количество обработчиков и отслеживаний
2. **Поддержка всех типов данных** - примитивы, объекты, массивы
3. **Улучшенная поддержка TypeScript**
4. **Предсказуемое поведение** - все изменения отслеживаются автоматически

## Ограничения и особенности

### 1. Массивы и индексация
Vue 3 может не отслеживать изменения по индексам:

```javascript
const items = reactive([1, 2, 3])
// Эти изменения могут не быть отслежены
items[0] = 5
// Лучше использовать методы массивов или set()
```

### 2. Добавление новых свойств
Новые свойства в реактивных объектах нужно добавлять через `set`:

```javascript
import { set } from 'vue'

const state = reactive({ a: 1 })
// Правильно
set(state, 'b', 2)
// Неправильно - может не отслеживаться
state.b = 2
```

## Заключение

Система реактивности Vue 3 представляет собой значительное улучшение по сравнению с Vue 2. Использование Proxy позволяет более эффективно отслеживать изменения и упрощает работу с различными типами данных. Это делает код более предсказуемым и удобным для поддержки.