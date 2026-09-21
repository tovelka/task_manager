<template>
  <div class="home">
    <Header />
    <div class="content">
    <EventList />
  </div>
  </div>
</template>

<script setup lang="ts">
import Header from '@/components/Header.vue'
import EventList from '@/components/EventList.vue'
</script>

<style scoped>
.home {
  min-height: 100vh;
}

.content {
  padding: 2rem;
}
</style>

