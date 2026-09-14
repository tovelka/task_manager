# Продвинутые компоненты Vue 3

## Слоты (Slots)

Слоты позволяют передавать контент из родительского компонента в дочерний.

### Именованные слоты

```vue
<!-- Родительский компонент -->
<template>
  <BaseLayout>
    <template #header>
      <h1>Заголовок</h1>
    </template>
    <template #main>
      <p>Основной контент</p>
    </template>
    <template #footer>
      <p>Футер</p>
    </template>
  </BaseLayout>
</template>

<!-- Дочерний компонент (BaseLayout.vue) -->
<template>
  <div class="layout">
    <header>
      <slot name="header"></slot>
    </header>
    <main>
      <slot name="main"></slot>
    </main>
    <footer>
      <slot name="footer"></slot>
    </footer>
  </div>
</template>
```

### Слоты с передачей данных

```vue
<!-- Родительский компонент -->
<template>
  <UserList>
    <template #user="{ user }">
      <div>{{ user.name }} - {{ user.email }}</div>
    </template>
  </UserList>
</template>

<!-- Дочерний компонент (UserList.vue) -->
<template>
  <div>
    <slot 
      name="user" 
      v-for="user in users" 
      :key="user.id" 
      :user="user"
    ></slot>
  </div>
</template>
```

## v-model в компонентах

Vue 3 позволяет использовать v-model с пользовательскими компонентами:

```vue
<!-- Родительский компонент -->
<template>
  <CustomInput v-model="message" />
</template>

<!-- Дочерний компонент (CustomInput.vue) -->
<template>
  <input 
    :value="modelValue" 
    @input="$emit('update:modelValue', $event.target.value)"
  />
</template>

<script setup>
defineProps(['modelValue'])
defineEmits(['update:modelValue'])
</script>
```

## Пользовательские события

```vue
<!-- Дочерний компонент -->
<template>
  <button @click="$emit('custom-event', data)">Кнопка</button>
</template>

<script setup>
defineEmits(['custom-event'])
</script>

<!-- Родительский компонент -->
<template>
  <ChildComponent @custom-event="handleEvent" />
</template>

<script setup>
const handleEvent = (data) => {
  console.log('Получены данные:', data)
}
</script>
```

## Компоненты с props

```vue
<!-- Дочерний компонент -->
<template>
  <div>{{ title }}</div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },
  count: {
    type: Number,
    default: 0
  }
})
</script>
```

## Миксины (Mixin) - устаревший подход

В Vue 3 рекомендуется использовать Composition API вместо миксинов:

```vue
<!-- Использование Composition API -->
<script setup>
import { ref, onMounted } from 'vue'

const message = ref('Привет')
const fetchData = async () => {
  // логика получения данных
}
</script>
```

## Динамические компоненты

```vue
<template>
  <component :is="currentComponent"></component>
</template>

<script setup>
import { ref } from 'vue'
import ComponentA from './ComponentA.vue'
import ComponentB from './ComponentB.vue'

const currentComponent = ref('ComponentA')
</script>
```

## Keep-alive

Для сохранения состояния компонентов:

```vue
<template>
  <keep-alive>
    <component :is="currentComponent"></component>
  </keep-alive>
</template>
```
</parameter>