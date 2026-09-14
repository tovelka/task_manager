<script setup lang="ts">
  import {ref} from 'vue';
  import ChildCard from '@/components/ChildCard.vue';
  import UserCard from '@/components/UserCard.vue';

  const message = ref('Привет, мгу!');
  const age = ref(0);

  function click_func() {
    message.value += '!';
  };

  const counter = ref(0)
  const currentUser = ref({ name: 'Анна' })

  function onSelect(id: number) {
    counter.value += 1;
    console.log('Выбран id:', id)
  }

  function add_age() {
    age.value +=1; 
  }

</script>

<template>
  <h1>You did it!</h1>
  <p>
    Visit <a href="https://vuejs.org/" target="_blank" rel="noopener">vuejs.org</a> to read the
    documentation
  </p>
  <h1>Общий счетчик: {{ counter }}</h1>
  <h3>{{ message }}</h3>
  <button @click="click_func">Кликни</button>
  <ChildCard 
    title="nhgb"
    @select="onSelect"
  />

  <ChildCard
    title="Счётчик"
    :count=counter
    :user=currentUser
    @select="onSelect"
  />

  <h1>Возраст: {{ age }}</h1>

  <UserCard name="Миша" :age="2" @add_age="add_age"/>
  <UserCard name="Олег" :age="1" @add_age="add_age"/>
</template>

<style scoped></style>
