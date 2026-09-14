# Работа с API в Vue.js с помощью Axios

## Что такое Axios?

Axios - это HTTP-клиент, который позволяет делать запросы к серверу из Vue.js приложения. Он поддерживает как синхронные, так и асинхронные операции.

## Установка Axios

```bash
npm install axios
```

## Основные методы Axios

### 1. GET-запросы

```javascript
import axios from 'axios'

// Простой GET-запрос
axios.get('/api/users')
  .then(response => {
    console.log(response.data)
  })
  .catch(error => {
    console.error('Ошибка:', error)
  })

// GET-запрос с параметрами
axios.get('/api/users', {
  params: {
    page: 1,
    limit: 10
  }
})
```

### 2. POST-запросы

```javascript
// POST-запрос для создания данных
const userData = {
  name: 'Иван',
  email: 'ivan@example.com'
}

axios.post('/api/users', userData)
  .then(response => {
    console.log('Пользователь создан:', response.data)
  })
```

### 3. PUT и DELETE запросы

```javascript
// PUT-запрос для обновления данных
axios.put('/api/users/1', userData)

// DELETE-запрос для удаления данных
axios.delete('/api/users/1')
```

## Использование в Vue компонентах

### 1. В методах компонента

```javascript
const app = Vue.createApp({
  data() {
    return {
      users: [],
      loading: false
    }
  },
  
  async mounted() {
    await this.fetchUsers()
  },
  
  methods: {
    async fetchUsers() {
      try {
        this.loading = true
        const response = await axios.get('/api/users')
        this.users = response.data
      } catch (error) {
        console.error('Ошибка загрузки пользователей:', error)
      } finally {
        this.loading = false
      }
    },
    
    async createUser(userData) {
      try {
        const response = await axios.post('/api/users', userData)
        this.users.push(response.data)
      } catch (error) {
        console.error('Ошибка создания пользователя:', error)
      }
    }
  }
})
```

### 2. Создание конфигурации для axios

```javascript
// api/client.js
import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Добавление интерцепторов для обработки ошибок
apiClient.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // Обработка ошибки авторизации
      console.error('Неавторизован')
    }
    return Promise.reject(error)
  }
)

export default apiClient
```

## Практические задания

1. Создайте компонент для отображения списка пользователей
2. Реализуйте загрузку данных при монтировании компонента
3. Добавьте обработку ошибок и отображение статуса загрузки

## Задание для самостоятельной работы

Создайте приложение-каталог пользователей с возможностью:

1. Отображения списка пользователей из API
2. Добавления нового пользователя
3. Удаления пользователя
4. Обработки ошибок (например, если сервер недоступен)

Реализуйте следующую функциональность:
- Загрузка данных при монтировании компонента
- Отображение статуса загрузки
- Форма для добавления нового пользователя
- Обработку ошибок (сетевые ошибки, серверные ошибки)
- Удаление пользователей с подтверждением

Используйте axios для всех HTTP-запросов к API.\n</ARG>