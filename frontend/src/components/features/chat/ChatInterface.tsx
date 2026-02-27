import { useState, useRef, useEffect } from 'react';
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
            content: "Code, learn, build — I'm here to help.",
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
        const promptText = input;
        setInput('');
        setIsLoading(true);

        try {
            // Call the Dual-Agent endpoint (non-streaming)
            const response = await api.sendMessage(promptText);

            // Show the explanation text in the chat bubble
            const aiMessage: Message = {
                id: (Date.now() + 1).toString(),
                role: 'assistant',
                content: response.explanation,
                timestamp: Date.now(),
            };
            setMessages(prev => [...prev, aiMessage]);

            // Pass ai_html + fallback_html + python_code to the visualizer context
            processBackendResponse({
                ai_html:       response.ai_html,
                fallback_html: response.fallback_html,
                explanation:   response.explanation,
                type:          response.type,
                python_code:   response.python_code,
            });

        } catch (error) {
            console.error(error);
            const errMessage: Message = {
                id: (Date.now() + 1).toString(),
                role: 'assistant',
                content: 'Sorry, something went wrong. Please check if the backend is running.',
                timestamp: Date.now(),
            };
            setMessages(prev => [...prev, errMessage]);
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
            <div className="p-4 border-t border-white/5">
                <div className="flex gap-2 items-end bg-white/5 rounded-2xl border border-white/10 p-2 shadow-2xl">
                    <textarea
                        ref={textareaRef}
                        className="flex-1 bg-transparent outline-none text-sm text-white placeholder-slate-500 resize-none min-h-[24px] max-h-[120px] leading-relaxed px-2 py-1"
                        style={{ fontFamily: 'var(--font-primary)' }}
                        placeholder='Ask about a data structure or algorithm...'
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={handleKeyDown}
                        rows={1}
                    />
                    <button
                        onClick={handleSend}
                        disabled={isLoading || !input.trim()}
                        className="w-8 h-8 flex-shrink-0 flex items-center justify-center bg-blue-600 hover:bg-blue-500 disabled:opacity-40 disabled:cursor-not-allowed rounded-xl transition-all shadow-[0_0_15px_rgba(37,99,235,0.4)]"
                    >
                        {isLoading
                            ? <Loader2 className="w-4 h-4 animate-spin text-white" />
                            : <Send className="w-4 h-4 text-white" />
                        }
                    </button>
                </div>
            </div>
        </div>
    );
};
