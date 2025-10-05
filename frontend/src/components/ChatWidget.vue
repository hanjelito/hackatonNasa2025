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
    <div v-if="chatState === 'open'" class="chat-window" :class="{ expanded: isExpanded }">
      <div class="chat-header">
        <div class="chat-title">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
          </svg>
          <span>Chat about: {{ truncatedTitle }}</span>
        </div>
        <div class="chat-actions">
          <button @click="toggleExpand" class="header-btn" :title="isExpanded ? 'Collapse' : 'Expand'">
            <svg v-if="!isExpanded" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="15 3 21 3 21 9"></polyline>
              <polyline points="9 21 3 21 3 15"></polyline>
              <line x1="21" y1="3" x2="14" y2="10"></line>
              <line x1="3" y1="21" x2="10" y2="14"></line>
            </svg>
            <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="4 14 10 14 10 20"></polyline>
              <polyline points="20 10 14 10 14 4"></polyline>
              <line x1="14" y1="10" x2="21" y2="3"></line>
              <line x1="3" y1="21" x2="10" y2="14"></line>
            </svg>
          </button>
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
          <div class="message-content" :class="{ typing: message.text === '...' }">
            <template v-if="message.text === '...'">
              <span class="typing-dot"></span>
              <span class="typing-dot"></span>
              <span class="typing-dot"></span>
            </template>
            <template v-else>
              <div v-html="renderMarkdown(message.text)" class="markdown-body"></div>
              <span class="message-time">{{ formatTime(message.timestamp) }}</span>
            </template>
          </div>
        </div>
      </div>

      <div class="chat-input-area">
        <div class="input-wrapper">
          <input
            v-model="inputMessage"
            type="text"
            placeholder="Ask about this article..."
            @keyup.enter="sendMessage"
            maxlength="500"
            class="chat-input"
          />
          <span class="char-counter" :class="{ 'near-limit': inputMessage.length > 450 }">
            {{ inputMessage.length }}/500
          </span>
        </div>
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
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import 'github-markdown-css/github-markdown-dark.css'

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
const isExpanded = ref(false)
const messages = ref<Message[]>([])
const unreadCount = ref(0)
const messagesContainer = ref<HTMLElement | null>(null)
const sessionToken = ref<string | null>(null)
let messageIdCounter = 1

const truncatedTitle = computed(() => {
  return props.articleTitle.length > 40
    ? props.articleTitle.substring(0, 40) + '...'
    : props.articleTitle
})

// Función para inicializar o recuperar una sesión
const initializeSession = async () => {
  try {
    // Intentar recuperar token del localStorage
    const storedToken = localStorage.getItem(`chat_session_${props.paperId}`)

    // Llamar al backend para inicializar/recuperar sesión
    const url = storedToken
      ? `/api/chat/session/${props.paperId}?session_token=${storedToken}`
      : `/api/chat/session/${props.paperId}`

    const response = await fetch(url)

    if (!response.ok) {
      throw new Error('Failed to initialize session')
    }

    const data = await response.json()

    // Guardar el token en el estado y localStorage
    sessionToken.value = data.session_token
    localStorage.setItem(`chat_session_${props.paperId}`, data.session_token)

    // Si se recuperó una sesión existente, cargar los mensajes
    if (!data.is_new_session && data.messages && data.messages.length > 0) {
      messages.value = data.messages.map((msg: any, index: number) => ({
        id: index + 1,
        type: msg.role,
        text: msg.content,
        timestamp: new Date(msg.timestamp)
      }))
      messageIdCounter = messages.value.length + 1
    } else {
      // Nueva sesión: agregar mensaje de bienvenida
      messages.value = [{
        id: messageIdCounter++,
        type: 'model',
        text: `Hi! I'm here to help you understand more about "${props.articleTitle}". What would you like to know?`,
        timestamp: new Date()
      }]
    }
  } catch (error) {
    console.error('Error initializing session:', error)
    // En caso de error, crear una sesión local sin token
    messages.value = [{
      id: messageIdCounter++,
      type: 'model',
      text: `Hi! I'm here to help you understand more about "${props.articleTitle}". What would you like to know?`,
      timestamp: new Date()
    }]
  }
}

const openChat = async () => {
  chatState.value = 'open'
  unreadCount.value = 0

  // Inicializar o recuperar sesión
  await initializeSession()

  nextTick(() => scrollToBottom())
}

const minimizeChat = () => {
  chatState.value = 'minimized'
}

const closeChat = () => {
  chatState.value = 'closed'
}

const toggleExpand = () => {
  isExpanded.value = !isExpanded.value
  nextTick(() => scrollToBottom())
}

const sendMessage = async () => {
  if (!inputMessage.value.trim()) return

  // Guardar el texto del mensaje antes de limpiar el input
  const userMessageText = inputMessage.value

  // Agregar mensaje del usuario
  const userMessage = {
    id: messageIdCounter++,
    type: 'user' as MessageType,
    text: userMessageText,
    timestamp: new Date()
  }
  messages.value.push(userMessage)

  inputMessage.value = ''
  nextTick(() => scrollToBottom())

  // Agregar mensaje de "escribiendo..."
  const typingMessageId = messageIdCounter++
  messages.value.push({
    id: typingMessageId,
    type: 'model',
    text: '...',
    timestamp: new Date()
  })
  nextTick(() => scrollToBottom())

  try {
    // Verificar que tenemos un token de sesión
    if (!sessionToken.value) {
      throw new Error('No session token. Please reopen the chat.')
    }

    // SOLO enviar el último mensaje del usuario, no todo el historial
    const messagesForBackend = [{
      role: userMessage.type,
      content: userMessage.text
    }]

    // Llamar al backend
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        messages: messagesForBackend,
        paper_id: props.paperId,
        session_token: sessionToken.value
      })
    })

    // Si la sesión expiró (410), inicializar nueva sesión
    if (response.status === 410) {
      // Limpiar token expirado
      localStorage.removeItem(`chat_session_${props.paperId}`)
      sessionToken.value = null

      // Remover mensaje de "escribiendo..."
      const typingIndex = messages.value.findIndex(msg => msg.id === typingMessageId)
      if (typingIndex !== -1) {
        messages.value.splice(typingIndex, 1)
      }

      // Mostrar mensaje de sesión expirada
      messages.value.push({
        id: messageIdCounter++,
        type: 'model',
        text: 'Your session has expired due to inactivity. Please send your message again to start a new conversation.',
        timestamp: new Date()
      })

      // Reinicializar sesión
      await initializeSession()
      return
    }

    if (!response.ok) {
      throw new Error('Failed to get response from chat')
    }

    const data = await response.json()

    // Remover mensaje de "escribiendo..."
    const typingIndex = messages.value.findIndex(msg => msg.id === typingMessageId)
    if (typingIndex !== -1) {
      messages.value.splice(typingIndex, 1)
    }

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

    // Remover mensaje de "escribiendo..."
    const typingIndex = messages.value.findIndex(msg => msg.id === typingMessageId)
    if (typingIndex !== -1) {
      messages.value.splice(typingIndex, 1)
    }

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

// Configurar marked
marked.setOptions({
  gfm: true,
  breaks: true
})

const renderMarkdown = (text: string): string => {
  const rawHtml = marked(text) as string
  const sanitized = DOMPurify.sanitize(rawHtml)

  // Agregar bullets manualmente para sobrescribir reset de Tailwind
  const withBullets = sanitized
    .replace(/<li>/g, '<li style="display: list-item; margin-left: 1.5rem; list-style-type: disc; list-style-position: outside;">')

  return withBullets
}
</script>

<style scoped>
@import '../assets/css/chat-widget.css';
</style>
