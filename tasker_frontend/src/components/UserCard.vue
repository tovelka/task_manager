<script setup lang="ts">
    const props = defineProps<{
        name: string
        age: number
    }>()

    const emit = defineEmits<{
        (e: 'add_age'): void
    }>()

    function birthday() {
        emit('add_age')
    }
</script>

<template>
    <div>
        <p>{{ name }}: {{ age }} лет.</p>
        <button @click="birthday">День рождения</button>
    </div>
</template>