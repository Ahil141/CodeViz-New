import { useState, useRef, useEffect } from 'react'
import { Send, Loader2, Trash2, Code2, MessageSquare, Sparkles } from 'lucide-react'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
  visualizerCode?: string | null
  dataStructure?: string | null
  operations?: string[] | null
}

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const STORAGE_KEY = 'codeviz-smart-chat-history'

// Parse streaming response with metadata
function parseStreamResponse(fullResponse: string): {
  metadata: any | null
  text: string
} {
  const metadataMatch = fullResponse.match(/__METADATA__(.*?)__END_METADATA__/)
  if (metadataMatch) {
    try {
      const metadata = JSON.parse(metadataMatch[1])
      const text = fullResponse.replace(/__METADATA__.*?__END_METADATA__/, '')
      return { metadata, text }
    } catch (e) {
      return { metadata: null, text: fullResponse }
    }
  }
  return { metadata: null, text: fullResponse }
}

function SmartChat() {
  const [messages, setMessages] = useState<Message[]>(() => {
    const saved = localStorage.getItem(STORAGE_KEY)
    return saved ? JSON.parse(saved) : []
  })
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [activeVisualizer, setActiveVisualizer] = useState<string | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const iframeRef = useRef<HTMLIFrameElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Save to localStorage whenever messages change
  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(messages))
  }, [messages])

  // Update active visualizer when messages change
  useEffect(() => {
    const lastMessageWithViz = [...messages].reverse().find(m => m.visualizerCode)
    if (lastMessageWithViz?.visualizerCode) {
      setActiveVisualizer(lastMessageWithViz.visualizerCode)
    }
  }, [messages])

  const isSubmitting = useRef(false)
  const abortControllerRef = useRef<AbortController | null>(null)

  const clearChat = () => {
    if (window.confirm('Are you sure you want to clear the chat history?')) {
      // Abort any pending request
      if (abortControllerRef.current) {
        abortControllerRef.current.abort()
        abortControllerRef.current = null
      }

      setMessages([])
      setActiveVisualizer(null)
      setIsLoading(false)
      isSubmitting.current = false
      localStorage.removeItem(STORAGE_KEY)
    }
  }


  const sendMessage = async () => {
    if (!input.trim() || isLoading || isSubmitting.current) return

    // Cancel any previous request just in case
    if (abortControllerRef.current) {
      abortControllerRef.current.abort()
    }

    // Create new abort controller
    const abortController = new AbortController()
    abortControllerRef.current = abortController

    isSubmitting.current = true
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input.trim(),
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      // Use the smart chat streaming endpoint
      const response = await fetch(`${API_BASE_URL}/api/smart-chat/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: userMessage.content,
        }),
        signal: abortController.signal
      })

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const reader = response.body?.getReader()
      if (!reader) {
        throw new Error('Response body is not readable')
      }

      // Initialize assistant message
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: '',
        timestamp: new Date(),
      }

      setMessages((prev) => [...prev, assistantMessage])

      // Stream decoder
      const decoder = new TextDecoder()
      let fullResponse = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const chunk = decoder.decode(value, { stream: true })
        fullResponse += chunk

        // Parse and update
        const { metadata, text } = parseStreamResponse(fullResponse)

        setMessages((prev) => {
          const newMessages = [...prev]
          const lastMessageIdx = newMessages.findIndex(m => m.id === assistantMessage.id)

          if (lastMessageIdx !== -1) {
            newMessages[lastMessageIdx] = {
              ...newMessages[lastMessageIdx],
              content: text,
              visualizerCode: metadata?.visualizer_code || null,
              dataStructure: metadata?.data_structure || null,
              operations: metadata?.operations || null,
            }
          }
          return newMessages
        })
      }

    } catch (error: any) {
      if (error.name === 'AbortError') {
        console.log('Request aborted')
        return // Don't show error message for cancellations
      }

      console.error('Error sending message:', error)
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      // Only reset if this is still the active controller
      if (abortControllerRef.current === abortController) {
        setIsLoading(false)
        isSubmitting.current = false
        abortControllerRef.current = null
      }
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="flex h-full bg-gray-50">
      {/* Chat Panel - Left Side */}
      <div className="w-1/2 flex flex-col border-r border-gray-200">
        {/* Header */}
        <div className="bg-white border-b border-gray-200 px-4 py-3 flex justify-between items-center shadow-sm">
          <div className="flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-indigo-600" />
            <h2 className="font-semibold text-gray-700">Smart DS Chat</h2>
          </div>
          {messages.length > 0 && (
            <button
              onClick={clearChat}
              className="text-gray-400 hover:text-red-500 transition-colors p-1.5 rounded-lg hover:bg-red-50"
              title="Clear Conversation"
            >
              <Trash2 className="w-5 h-5" />
            </button>
          )}
        </div>

        {/* Messages List */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 ? (
            <div className="flex items-center justify-center h-full">
              <div className="text-center max-w-md">
                <div className="w-16 h-16 bg-indigo-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <MessageSquare className="w-8 h-8 text-indigo-600" />
                </div>
                <h2 className="text-2xl font-semibold text-gray-700 mb-2">
                  Learn Data Structures
                </h2>
                <p className="text-gray-500 mb-4">
                  Ask me to help you learn any data structure! Try:
                </p>
                <div className="space-y-2 text-sm">
                  <div className="bg-white rounded-lg p-3 border border-gray-200 text-left">
                    <span className="text-indigo-600">"Help me learn stack"</span>
                  </div>
                  <div className="bg-white rounded-lg p-3 border border-gray-200 text-left">
                    <span className="text-indigo-600">"Show me only the push operation"</span>
                  </div>
                  <div className="bg-white rounded-lg p-3 border border-gray-200 text-left">
                    <span className="text-indigo-600">"Explain insertion in linked list"</span>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[85%] rounded-lg px-4 py-3 ${message.role === 'user'
                      ? 'bg-indigo-600 text-white'
                      : 'bg-white text-gray-800 shadow-sm border border-gray-200'
                      }`}
                  >
                    <p className="whitespace-pre-wrap break-words">
                      {message.content}
                    </p>
                    {message.dataStructure && (
                      <div className="mt-2 pt-2 border-t border-gray-200/30 flex items-center gap-2 text-xs opacity-75">
                        <Code2 className="w-3 h-3" />
                        <span>
                          {message.dataStructure}
                          {message.operations && message.operations.length > 0 && (
                            <> · {message.operations.join(', ')}</>
                          )}
                        </span>
                      </div>
                    )}
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-white rounded-lg px-4 py-3 shadow-sm border border-gray-200">
                    <div className="flex items-center gap-2 text-gray-500">
                      <Loader2 className="w-4 h-4 animate-spin" />
                      <span>Thinking...</span>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="border-t border-gray-200 bg-white p-4">
          <div className="flex gap-2 items-end">
            <div className="flex-1 relative">
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask about any data structure..."
                rows={1}
                className="w-full px-4 py-3 pr-12 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none max-h-32 overflow-y-auto"
                disabled={isLoading}
              />
            </div>
            <button
              onClick={sendMessage}
              disabled={!input.trim() || isLoading}
              className="px-4 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center justify-center min-w-[48px]"
            >
              {isLoading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <Send className="w-5 h-5" />
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Visualization Panel - Right Side */}
      <div className="w-1/2 flex flex-col bg-gray-100">
        {/* Visualizer Header */}
        <div className="bg-white border-b border-gray-200 px-4 py-3 flex items-center gap-2 shadow-sm">
          <Code2 className="w-5 h-5 text-indigo-600" />
          <h2 className="font-semibold text-gray-700">Visualization</h2>
        </div>

        {/* Visualizer Content */}
        <div className="flex-1 overflow-hidden">
          {activeVisualizer ? (
            <iframe
              ref={iframeRef}
              srcDoc={activeVisualizer}
              className="w-full h-full border-0"
              sandbox="allow-scripts allow-same-origin"
              title="Data Structure Visualizer"
            />
          ) : (
            <div className="flex items-center justify-center h-full">
              <div className="text-center text-gray-400">
                <Code2 className="w-16 h-16 mx-auto mb-4 opacity-50" />
                <p className="text-lg">No visualization yet</p>
                <p className="text-sm mt-2">
                  Ask about a data structure to see it visualized here
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default SmartChat
