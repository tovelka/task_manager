<script setup lang="ts">
const props = defineProps<{
  title: string
  count?: number
  user?: { name: string }
}>()

const emit = defineEmits<{
  (e: 'select', id: number): void
}>()

function handleClick() {
  emit('select', props.count ?? 0)
}
</script>

<template>
  <div class="card">
    <h3>{{ title }}</h3>
    <p v-if="count !== undefined">Счётчик: {{ count }}</p>
    <p v-if="user">Пользователь: {{ user.name }}</p>
    <button @click="handleClick">Выбрать</button>
  </div>
</template>

<style scoped>
.card {
  border: 1px solid #ccc;
  padding: 1rem;
  margin: 0.5rem 0;
}
</style>