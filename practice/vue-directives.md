# Пользовательские директивы в Vue 3

## Что такое директивы?

Директивы - это специальные атрибуты с префиксом `v-`, которые применяют реактивные эффекты к DOM. Vue предоставляет ряд встроенных директив, но также позволяет создавать пользовательские.

## Создание пользовательских директив

### Глобальная директива

```javascript
// main.js
import { createApp } from 'vue'

const app = createApp({})

// Глобальная директива
app.directive('focus', {
  mounted(el) {
    el.focus()
  }
})
```

### Локальная директива

```vue
<template>
  <input v-focus />
</template>

<script setup>
const focusDirective = {
  mounted(el) {
    el.focus()
  }
}
</script>
```

## Хуки жизненного цикла директив

```javascript
app.directive('example', {
  // Вызывается до того, как элемент привязан к DOM
  created(el, binding, vnode) {
    console.log('created')
  },
  
  // Вызывается, когда элемент привязан к DOM
  mounted(el, binding, vnode) {
    console.log('mounted')
  },
  
  // Вызывается до обновления компонента
  beforeUpdate(el, binding, vnode, prevVnode) {
    console.log('beforeUpdate')
  },
  
  // Вызывается после обновления компонента
  updated(el, binding, vnode, prevVnode) {
    console.log('updated')
  },
  
  // Вызывается перед тем, как элемент будет удалён из DOM
  beforeUnmount(el, binding, vnode) {
    console.log('beforeUnmount')
  },
  
  // Вызывается после того, как элемент был удалён из DOM
  unmounted(el, binding, vnode) {
    console.log('unmounted')
  }
})
```

## Аргументы и значения директив

```vue
<template>
  <div v-example:arg.modifier="value">Пример</div>
</template>

<script setup>
// Пример использования
app.directive('example', {
  mounted(el, binding) {
    console.log(binding.arg)      // arg
    console.log(binding.value)    // value
    console.log(binding.modifiers) // { modifier: true }
  }
})
</script>
```

## Примеры пользовательских директив

### Директива для подсветки текста

```javascript
app.directive('highlight', {
  mounted(el, binding) {
    el.style.backgroundColor = binding.value || 'yellow'
  },
  updated(el, binding) {
    el.style.backgroundColor = binding.value || 'yellow'
  }
})
```

### Директива для таймера

```javascript
app.directive('timer', {
  mounted(el, binding) {
    const interval = setInterval(() => {
      if (binding.value) {
        binding.value()
      }
    }, binding.arg || 1000)
    
    el._interval = interval
  },
  unmounted(el) {
    clearInterval(el._interval)
  }
})
```

### Директива для фокуса

```javascript
app.directive('focus', {
  mounted(el, binding) {
    if (binding.value !== false) {
      el.focus()
    }
  },
  updated(el, binding) {
    if (binding.value === true) {
      el.focus()
    }
  }
})
```

## Использование в шаблонах

```vue
<template>
  <div v-highlight="'#ff0000'">Красный фон</div>
  <input v-focus />
  <button v-timer:2000="updateCounter">Обновить</button>
</template>
```

## Директивы в Composition API

```vue
<script setup>
import { onMounted, onUnmounted } from 'vue'

const directive = {
  mounted(el, binding) {
    // Логика при монтировании
  },
  unmounted(el, binding) {
    // Логика при размонтировании
  }
}
</script>
```
