<template>
  <div>
    <Header />
    <EventList />
  </div>
</template>

<script>
import Header from '../components/Header.vue';
import EventList from '../components/EventList.vue';

export default {
  components: {
    Header,
    EventList
  }
}
</script>
