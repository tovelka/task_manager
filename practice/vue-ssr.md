# Server-Side Rendering (SSR) в Vue 3

## Введение в SSR

Server-Side Rendering (SSR) позволяет рендерить Vue-приложения на сервере, что улучшает SEO, производительность и UX. Vue 3 предоставляет мощные возможности для создания SSR-приложений.

## Преимущества SSR

1. **SEO**: Содержимое доступно для поисковых систем сразу при загрузке
2. **Производительность**: Быстрая отрисовка первого экрана
3. **UX**: Уменьшает время до интерактивности
4. **Консистентность**: Один и тот же код на сервере и клиенте

## Основные концепции SSR

### Гидратация

Гидратация - это процесс, при котором сервер отправляет HTML-код, а клиент превращает его в интерактивное приложение.

```javascript
// server.js
import { createSSRApp } from 'vue'
import { renderToString } from '@vue/server-renderer'
import App from './App.vue'

const app = createSSRApp(App)
const html = await renderToString(app)
```

### Клиентская и серверная части

```javascript
// main.js (клиентский код)
import { createApp } from 'vue'
import App from './App.vue'

createApp(App).mount('#app')

// server.js (серверный код)
import { createSSRApp } from 'vue'
import { renderToString } from '@vue/server-renderer'
import App from './App.vue'

const app = createSSRApp(App)
const html = await renderToString(app)
```

## Настройка SSR в Vue 3

### Базовая конфигурация

```javascript
// vue.config.js (для Vue CLI)
module.exports = {
  ssr: true,
  configureWebpack: {
    output: {
      filename: 'js/[name].js',
      chunkFilename: 'js/[name].js'
    }
  }
}
```

### Использование Vite с SSR

```javascript
// vite.config.js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueSSR from '@vitejs/plugin-vue-ssr'

export default defineConfig({
  plugins: [
    vue(),
    vueSSR()
  ]
})
```

## SSR с Pinia и Vuex

### Использование Pinia с SSR

```javascript
// store/index.js
import { createPinia } from 'pinia'

export function createApp() {
  const app = createSSRApp(App)
  const pinia = createPinia()
  
  // Инициализация Pinia для SSR
  if (typeof window === 'undefined') {
    pinia.ssrContext = {
      url: '/'
    }
  }
  
  app.use(pinia)
  return { app, pinia }
}
```

### Пример с серверным рендерингом

```vue
<template>
  <div>
    <h1>{{ title }}</h1>
    <p>{{ content }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const title = ref('Заголовок')
const content = ref('Содержимое')

// Используем только на клиенте
onMounted(() => {
  console.log('Компонент смонтирован')
})
</script>
```

## Создание SSR-приложения

### Основной файл сервера

```javascript
// server.js
import express from 'express'
import { createApp } from './main.js'
import { renderToString } from '@vue/server-renderer'

const app = express()

app.get('*', async (req, res) => {
  try {
    const { app } = createApp()
    
    const html = await renderToString(app)
    
    res.send(`
      <!DOCTYPE html>
      <html>
        <head><title>SSR App</title></head>
        <body>
          <div id="app">${html}</div>
          <script type="module" src="/src/main.js"></script>
        </body>
      </html>
    `)
  } catch (error) {
    console.error(error)
    res.status(500).send('Server error')
  }
})

app.listen(3000)
```

### Файл main.js

```javascript
// main.js
import { createSSRApp } from 'vue'
import App from './App.vue'

export function createApp() {
  const app = createSSRApp(App)
  
  // Добавляем плагины
  return { app }
}
```

## Оптимизация SSR

### Предзагрузка данных

```vue
<template>
  <div v-if="loading">Загрузка...</div>
  <div v-else>{{ user.name }}</div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const user = ref(null)
const loading = ref(true)

// Метод для предзагрузки данных
const preloadData = async () => {
  try {
    const response = await fetch('/api/user')
    user.value = await response.json()
  } catch (error) {
    console.error('Ошибка загрузки данных:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  preloadData()
})
</script>
```

### Динамическая загрузка компонентов

```vue
<template>
  <component :is="dynamicComponent" />
</template>

<script setup>
import { ref, defineAsyncComponent } from 'vue'

const dynamicComponent = defineAsyncComponent(() => 
  import('./HeavyComponent.vue')
)
</script>
```

## Проблемы и решения

### Проблема с жизненным циклом

```javascript
// Неправильно - будет работать только на клиенте
const mounted = () => {
  // Код, зависящий от DOM
}

// Правильно - проверка окружения
const mounted = () => {
  if (typeof window !== 'undefined') {
    // Код для клиента
  }
}
```

### Проблема с localStorage

```vue
<script setup>
import { onMounted } from 'vue'

const loadFromStorage = () => {
  if (typeof window !== 'undefined') {
    const data = localStorage.getItem('userData')
    // Логика работы с localStorage
  }
}
</script>
```

## Интеграция с Express.js

```javascript
// server.js
import express from 'express'
import { createApp } from './main.js'
import { renderToString } from '@vue/server-renderer'
import { createRouter, createMemoryHistory } from 'vue-router'

const app = express()

app.get('*', async (req, res) => {
  const { app: vueApp } = createApp()
  
  // Создаем роутер для сервера
  const router = createRouter({
    history: createMemoryHistory(req.url),
    routes: [
      { path: '/', component: Home }
    ]
  })
  
  await router.isReady()
  vueApp.use(router)
  
  const html = await renderToString(vueApp)
  
  res.send(`
    <!DOCTYPE html>
    <html>
      <head><title>SSR App</title></head>
      <body>
        <div id="app">${html}</div>
      </body>
    </html>
  `)
})

app.listen(3000)
```

## Инструменты для SSR

1. **Nuxt.js** - фреймворк для Vue SSR
2. **Vite + SSR** - современный подход к SSR с Vite
3. **Express.js** - серверная часть
4. **Webpack** - сборка приложения

## Рекомендации по SSR

1. **Оптимизируйте загрузку данных на сервере**
2. **Используйте кэширование**
3. **Минимизируйте количество клиентских компонентов**
4. **Проверяйте работу в разных окружениях**
5. **Тестируйте SSR отдельно от клиентской части**
6. **Используйте предзагрузку данных**

## Тестирование SSR

```javascript
// test/ssr.test.js
import { renderToString } from '@vue/server-renderer'
import { createSSRApp } from 'vue'
import App from '../src/App.vue'

describe('SSR Rendering', () => {
  test('should render app correctly', async () => {
    const app = createSSRApp(App)
    const html = await renderToString(app)
    
    expect(html).toContain('<div id="app">')
  })
})
```
