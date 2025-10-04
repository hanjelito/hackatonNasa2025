<template>
  <div class="chat-widget" :class="chatState">
    <!-- Botón flotante cuando está cerrado -->
    <button v-if="chatState === 'closed'" @click="openChat" class="chat-fab">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
      </svg>
    </button>

    <!-- Ventana de chat minimizada -->
    <div v-if="chatState === 'minimized'" class="chat-minimized">
      <div class="chat-minimized-header" @click="openChat">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
        </svg>
        <span>Chat about article</span>
        <span class="unread-badge" v-if="unreadCount > 0">{{ unreadCount }}</span>
      </div>
      <button @click="closeChat" class="minimize-close-btn">×</button>
    </div>

    <!-- Ventana de chat completa -->
    <div v-if="chatState === 'open'" class="chat-window">
      <div class="chat-header">
        <div class="chat-title">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
          </svg>
          <span>Chat about: {{ truncatedTitle }}</span>
        </div>
        <div class="chat-actions">
          <button @click="minimizeChat" class="header-btn" title="Minimize">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="5" y1="12" x2="19" y2="12"></line>
            </svg>
          </button>
          <button @click="closeChat" class="header-btn" title="Close">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
      </div>

      <div class="chat-messages" ref="messagesContainer">
        <div v-for="message in messages" :key="message.id" class="message" :class="message.type">
          <div class="message-avatar">
            <span v-if="message.type === 'user'">👤</span>
            <span v-else>🤖</span>
          </div>
          <div class="message-content">
            <p>{{ message.text }}</p>
            <span class="message-time">{{ formatTime(message.timestamp) }}</span>
          </div>
        </div>
      </div>

      <div class="chat-input-area">
        <input
          v-model="inputMessage"
          type="text"
          placeholder="Ask about this article..."
          @keyup.enter="sendMessage"
          class="chat-input"
        />
        <button @click="sendMessage" class="send-btn" :disabled="!inputMessage.trim()">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="22" y1="2" x2="11" y2="13"></line>
            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick } from 'vue'

const props = defineProps<{
  articleTitle: string
  paperId: string
}>()

type ChatState = 'closed' | 'minimized' | 'open'
type MessageType = 'user' | 'model'

interface Message {
  id: number
  type: MessageType
  text: string
  timestamp: Date
}

const chatState = ref<ChatState>('closed')
const inputMessage = ref('')
const messages = ref<Message[]>([
  {
    id: 1,
    type: 'model',
    text: `Hi! I'm here to help you understand more about "${props.articleTitle}". What would you like to know?`,
    timestamp: new Date()
  }
])
const unreadCount = ref(0)
const messagesContainer = ref<HTMLElement | null>(null)
let messageIdCounter = 2

const truncatedTitle = computed(() => {
  return props.articleTitle.length > 40
    ? props.articleTitle.substring(0, 40) + '...'
    : props.articleTitle
})

const openChat = () => {
  chatState.value = 'open'
  unreadCount.value = 0
  nextTick(() => scrollToBottom())
}

const minimizeChat = () => {
  chatState.value = 'minimized'
}

const closeChat = () => {
  chatState.value = 'closed'
}

const sendMessage = async () => {
  if (!inputMessage.value.trim()) return

  // Agregar mensaje del usuario
  messages.value.push({
    id: messageIdCounter++,
    type: 'user',
    text: inputMessage.value,
    timestamp: new Date()
  })

  const userQuestion = inputMessage.value
  inputMessage.value = ''
  nextTick(() => scrollToBottom())

  try {
    // Preparar mensajes para el backend
    const messagesForBackend = messages.value.map((msg: Message) => ({
      role: msg.type,
      content: msg.text
    }))

    // Llamar al backend
    const response = await fetch('/api/chat/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        messages: messagesForBackend,
        paper_id: props.paperId
      })
    })

    if (!response.ok) {
      throw new Error('Failed to get response from chat')
    }

    const data = await response.json()

    // Agregar respuesta del modelo
    messages.value.push({
      id: messageIdCounter++,
      type: 'model',
      text: data.content || data.response || 'Sorry, I could not process that request.',
      timestamp: new Date()
    })

    if (chatState.value !== 'open') {
      unreadCount.value++
    }

    nextTick(() => scrollToBottom())
  } catch (error) {
    console.error('Error sending message:', error)
    messages.value.push({
      id: messageIdCounter++,
      type: 'model',
      text: 'Sorry, there was an error processing your request. Please try again.',
      timestamp: new Date()
    })
    nextTick(() => scrollToBottom())
  }
}

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const formatTime = (date: Date) => {
  return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })
}
</script>

<style scoped>
@import '../assets/css/chat-widget.css';
</style>
