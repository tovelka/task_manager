<template>
  <div>
    <h2>Create Event</h2>
    <form @submit.prevent="createEvent">
      <input v-model="event.title" placeholder="Title" required />
      <input v-model="event.description" placeholder="Description" required />
      <input v-model="event.date" type="date" required />
      <button type="submit">Create</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      event: {
        title: '',
        description: '',
        date: ''
      }
    };
  },
  methods: {
    createEvent() {
      this.$emit('create', this.event);
    }
  }
}
</script>
```

Теперь, когда у нас есть все необходимые компоненты, давайте добавим их в существующие файлы `RegisterVue` и `HomeVue`, чтобы отображать их в зависимости от авторизации пользователя.

```tool
TOOL_NAME: read_file
BEGIN_ARG: filepath
src/views/RegisterVue.vue