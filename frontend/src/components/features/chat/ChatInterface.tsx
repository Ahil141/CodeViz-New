import { useState, useRef, useEffect } from 'react';
import { flushSync } from 'react-dom';
import { Send, Loader2 } from 'lucide-react';
import type { Message } from '../../../types';
import { api } from '../../../services/api';
import { ChatMessage } from './ChatMessage';
import { useVisualization } from '../../../services/VisualizationController';

export const ChatInterface = () => {
    const [messages, setMessages] = useState<Message[]>([
        {
            id: 'welcome',
            role: 'assistant',
            content: 'Code, learn, build — I’m here to help.',
            timestamp: Date.now(),
        }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const { processBackendResponse } = useVisualization();

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    // Auto-resize textarea
    const textareaRef = useRef<HTMLTextAreaElement>(null);
    useEffect(() => {
        if (textareaRef.current) {
            textareaRef.current.style.height = 'auto';
            textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px';
        }
    }, [input]);

    const handleSend = async () => {
        if (!input.trim() || isLoading) return;

        const userMessage: Message = {
            id: Date.now().toString(),
            role: 'user',
            content: input,
            timestamp: Date.now(),
        };

        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        // Create placeholder AI message for streaming
        const aiMessageId = (Date.now() + 1).toString();
        const aiMessage: Message = {
            id: aiMessageId,
            role: 'assistant',
            content: '',
            timestamp: Date.now(),
        };

        setMessages(prev => [...prev, aiMessage]);

        try {
            let fullText = '';
            let visualizationData: any = null;

            // Stream the response
            for await (const chunk of api.sendMessageStream(userMessage.content)) {
                if (chunk.type === 'text') {
                    // Append text chunk progressively
                    fullText += chunk.content || '';

                    // Force immediate render (bypass React 18 batching)
                    flushSync(() => {
                        setMessages(prev =>
                            prev.map(msg =>
                                msg.id === aiMessageId
                                    ? { ...msg, content: fullText }
                                    : msg
                            )
                        );
                    });
                } else if (chunk.type === 'complete') {
                    // Store visualization data for processing
                    visualizationData = chunk;
                } else if (chunk.type === 'error') {
                    console.error('Stream error:', chunk.message);
                    setMessages(prev =>
                        prev.map(msg =>
                            msg.id === aiMessageId
                                ? { ...msg, content: 'Sorry, something went wrong. Please try again.' }
                                : msg
                        )
                    );
                }
            }

            // Process visualization data if available
            if (visualizationData) {
                const backendResponse = {
                    text_response: fullText,
                    visualization_type: visualizationData.visualization_type,
                    code_blocks: visualizationData.code_blocks || [],
                    visualization_data: visualizationData.visualization_data,
                    implementation_code: visualizationData.implementation_code,
                };
                processBackendResponse(backendResponse);
            }

        } catch (error) {
            console.error(error);

            setMessages(prev =>
                prev.map(msg =>
                    msg.id === aiMessageId
                        ? { ...msg, content: 'Sorry, something went wrong. Please check if the backend is running.' }
                        : msg
                )
            );
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <div className="flex flex-col h-full bg-[#020617]">
            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4 scrollbar-hide">
                {messages.map((msg) => (
                    <ChatMessage key={msg.id} message={msg} />
                ))}
                {isLoading && (
                    <div className="flex justify-start px-2">
                        <div className="bg-white/5 border border-white/10 backdrop-blur-md shadow-2xl rounded-2xl p-3 flex items-center gap-2">
                            <Loader2 className="w-4 h-4 animate-spin text-blue-400" />
                            <span className="text-sm text-slate-400">Thinking...</span>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            {/* Input Area */}
            <div className="p-4 bg-[#020617] border-t border-white/5">
                <div className="relative flex items-end max-w-4xl mx-auto w-full">
                    <textarea
                        ref={textareaRef}
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={handleKeyDown}
                        placeholder="Ask about code..."
                        className="w-full pl-4 pr-12 py-3 rounded-2xl border border-white/10 bg-white/5 text-slate-200 placeholder-slate-500 focus:border-blue-500/50 focus:ring-2 focus:ring-blue-500/10 outline-none transition-all shadow-2xl resize-none min-h-[50px] max-h-[200px]"
                        style={{ height: 'auto', minHeight: '50px', fontFamily: "var(--font-primary)" }}
                        disabled={isLoading}
                        rows={1}
                    />
                    <button
                        onClick={handleSend}
                        disabled={!input.trim() || isLoading}
                        className="absolute right-2 bottom-2 p-2.5 bg-blue-600 text-white rounded-xl hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-[0_0_15px_rgba(37,99,235,0.4)]"
                    >
                        <Send className="w-4 h-4" />
                    </button>
                </div>
            </div>
        </div>
    );
};
