# Компоненты Vue.js

## Что такое компонент?

Компонент в Vue.js - это переиспользуемый блок кода, который может содержать свою логику, шаблон и стили. Компоненты позволяют создавать сложные интерфейсы из более простых частей.

## Основы создания компонентов

### Определение компонента

```javascript
const MyComponent = {
  template: `
    <div>
      <h2>{{ title }}</h2>
      <p>{{ content }}</p>
    </div>
  `,
  data() {
    return {
      title: 'Заголовок',
      content: 'Содержание компонента'
    }
  }
}
```

### Регистрация компонентов

#### Глобальная регистрация
```javascript
Vue.component('my-component', MyComponent)
```

#### Локальная регистрация
```javascript
const app = Vue.createApp({
  components: {
    'my-component': MyComponent
  }
})
```

## Свойства (Props)

Свойства позволяют передавать данные от родительского компонента дочернему:

```javascript
// Дочерний компонент
const ChildComponent = {
  props: ['message'],
  template: `<p>{{ message }}</p>`
}

// Родительский компонент
const ParentComponent = {
  template: `
    <div>
      <child-component :message="parentMessage"></child-component>
    </div>
  `,
  data() {
    return {
      parentMessage: 'Привет от родителя'
    }
  }
}
```

## События (Events)

Компоненты могут отправлять события родительским компонентам:

```javascript
// Дочерний компонент
const ChildComponent = {
  template: `<button @click="handleClick">Нажми меня</button>`,
  methods: {
    handleClick() {
      this.$emit('child-event', 'Данные от дочернего компонента')
    }
  }
}

// Родительский компонент
const ParentComponent = {
  template: `
    <div>
      <child-component @child-event="handleChildEvent"></child-component>
    </div>
  `,
  methods: {
    handleChildEvent(data) {
      console.log('Получены данные:', data)
    }
  }
}
```

## Практические задания

1. Создайте компонент карточки пользователя с полями: имя, возраст, email
2. Реализуйте родительский компонент, который отображает список пользователей
3. Добавьте возможность удаления пользователей через событие из дочернего компонента

## Задание для самостоятельной работы

Создайте приложение с каталогом товаров. У вас должен быть:
- Компонент товара с полями: название, цена, описание
- Компонент каталога, который отображает список товаров
- Возможность добавления нового товара через форму
- События для обработки действий с товарами

Реализуйте взаимодействие между компонентами с использованием props и events.
</ARG>