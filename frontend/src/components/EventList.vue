<template>
  <div class="event-list">
    <h2>Список событий</h2>
    
    <div class="event-actions">
      <button @click="showCreateForm = !showCreateForm">
        {{ showCreateForm ? 'Отмена' : 'Создать событие' }}
      </button>
    </div>
    
    <!-- Create Event Form -->
    <div v-if="showCreateForm" class="create-event-form">
      <h3>Создать новое событие</h3>
      <form @submit.prevent="createEvent" class="event-form">
        <div>
          <label for="eventName">Название события:</label>
          <input type="text" id="eventName" v-model="newEvent.name" required />
        </div>
        
        <div>
          <label for="eventDescription">Описание:</label>
          <textarea id="eventDescription" v-model="newEvent.description"></textarea>
        </div>
        
        <div>
          <label for="eventDate">Дата события:</label>
          <input type="date" id="eventDate" v-model="newEvent.date" required />
        </div>
        
        <div>
          <label for="eventTime">Время события:</label>
          <input type="time" id="eventTime" v-model="newEvent.time" />
        </div>
        
        <div class="checkbox-group">
          <label>
            <input type="checkbox" v-model="newEvent.is_public" />
            Публичное событие
          </label>
        </div>
        
        <button type="submit" :disabled="creating">Создать</button>
        <button type="button" @click="showCreateForm = false">Отмена</button>
      </form>
    </div>
    
    <!-- Events List -->
    <div v-if="!showCreateForm && events.length > 0" class="events-list">
      <h3>События</h3>
      <div v-for="event in events" :key="event.id" class="event-card">
        <h4>{{ event.title }}</h4>
        <p>{{ event.description }}</p>
        <p><strong>Дата:</strong> {{ formatDate(event.starts_at) }} {{ event.ends_at || '' }}</p>
        <p><strong>Статус:</strong> {{ event.is_public ? 'Публичное' : 'Приватное' }}</p>
        <div class="event-actions">
          <button @click="editEvent(event)">Редактировать</button>
          <button @click="deleteEvent(event.id)">Удалить</button>
        </div>
      </div>
    </div>
    
    <div v-else-if="!showCreateForm && events.length === 0">
      <p>Нет событий. Создайте первое событие!</p>
    </div>
    
    <!-- Edit Event Form -->
    <div v-if="editingEvent" class="edit-event-form">
      <h3>Редактировать событие</h3>
      <form @submit.prevent="updateEvent" class="event-form">
        <div>
          <label for="editEventName">Название события:</label>
          <input type="text" id="editEventName" v-model="editingEvent.title" required />
        </div>
        
        <div>
          <label for="editEventDescription">Описание:</label>
          <textarea id="editEventDescription" v-model="editingEvent.description"></textarea>
        </div>
        
        <div>
          <label for="editEventDate">Дата события:</label>
          <input type="date" id="editEventDate" v-model="editingEvent.starts_at" required />
        </div>
        
        <div>
          <label for="editEventTime">Время события:</label>
          <input type="time" id="editEventTime" v-model="editingEvent.ends_at" />
        </div>
        
        <div class="checkbox-group">
          <label>
            <input type="checkbox" v-model="editingEvent.is_public" />
            Публичное событие
          </label>
        </div>
        
        <button type="submit" :disabled="updating">Сохранить</button>
        <button type="button" @click="cancelEdit">Отмена</button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { eventsApi } from '@/api/full'

const showCreateForm = ref(false)
const creating = ref(false)
const updating = ref(false)
const events = ref<any[]>([])
const newEvent = ref({
  title: '',
  description: '',
  starts_at: '',
  ends_at: '',
  is_public: false
})
const editingEvent = ref<any>(null)

// Fetch all events on component mount
onMounted(async () => {
  await fetchEvents()
})

const fetchEvents = async () => {
  try {
    const response = await eventsApi.getAll()
    events.value = response.events
  } catch (error) {
    console.error('Error fetching events:', error)
    // Handle error appropriately (show notification, etc.)
  }
}

const createEvent = async () => {
  creating.value = true
  
  try {
    const eventData = {
      ...newEvent.value,
      starts_at: newEvent.value.starts_at + 'T' + (newEvent.value.ends_at || '00:00') + 'Z'
    }
    
    const response = await eventsApi.create(eventData)
    events.value.push(response)
    newEvent.value = {
      title: '',
      description: '',
      starts_at: '',
      ends_at: '',
      is_public: false
    }
    showCreateForm.value = false
  } catch (error) {
    console.error('Error creating event:', error)
  } finally {
    creating.value = false
  }
}

const editEvent = (event: any) => {
  editingEvent.value = { ...event }
}

const updateEvent = async () => {
  updating.value = true
  
  try {
    const eventData = {
      ...editingEvent.value,
      starts_at: editingEvent.value.starts_at + 'T' + (editingEvent.value.ends_at || '00:00') + 'Z'
    }
    
    const response = await eventsApi.update(editingEvent.value.id, eventData)
    const index = events.value.findIndex(e => e.id === response.id)
    if (index !== -1) {
      events.value[index] = response
    }
    editingEvent.value = null
  } catch (error) {
    console.error('Error updating event:', error)
  } finally {
    updating.value = false
  }
}

const cancelEdit = () => {
  editingEvent.value = null
}

const deleteEvent = async (id: number) => {
  if (confirm('Вы уверены, что хотите удалить это событие?')) {
    try {
      await eventsApi.delete(id)
      events.value = events.value.filter(event => event.id !== id)
    } catch (error) {
      console.error('Error deleting event:', error)
    }
  }
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('ru-RU')
}

</script>

<style scoped>
.event-list {
  max-width: 800px;
  margin: 2rem auto;
  padding: 1rem;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.event-actions {
  margin-top: 1rem;
}

.event-actions button {
  margin-right: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.event-actions button:hover {
  background-color: #0056b3;
}

.event-card {
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 1rem;
  margin-bottom: 1rem;
  background-color: #f8f9fa;
}

.event-card h4 {
  margin-top: 0;
  color: #333;
}

.event-card p {
  margin: 0.5rem 0;
  color: #666;
}

.create-event-form,
.edit-event-form {
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.event-form div {
  margin-bottom: 1rem;
}

.event-form label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
  color: #555;
}

.event-form input[type="text"],
.event-form textarea,
.event-form input[type="date"],
.event-form input[type="time"] {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

.checkbox-group {
  margin-bottom: 1rem;
}

.checkbox-group label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: normal;
  color: #555;
}

.checkbox-group input[type="checkbox"] {
  width: auto;
}

.event-form button {
  padding: 0.5rem 1rem;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 0.5rem;
}

.event-form button:hover:not(:disabled) {
  background-color: #218838;
}

.event-form button[type="button"] {
  background-color: #6c757d;
}

.event-form button[type="button"]:hover {
  background-color: #5a6268;
}

.event-form button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.events-list {
  margin-top: 1rem;
}
</style>