import type { Message } from './types';
import { cn } from './utils';
import { Bot, User } from 'lucide-react';
import { useVisualization } from './VisualizationController';

interface ChatMessageProps {
    message: Message;
}

export const ChatMessage = ({ message }: ChatMessageProps) => {
    const isUser = message.role === 'user';
    const { setPythonCode, setShowEditor } = useVisualization();

    const handleSendToEditor = () => {
        if (message.pythonCode) {
            setPythonCode(message.pythonCode);
            setShowEditor(true);
        }
    };

    return (
        <div className={cn(
            "flex w-full mb-6 px-4",
            isUser ? "justify-end" : "justify-start"
        )}>
            <div className={cn(
                "flex flex-col max-w-[80%] rounded-2xl p-4 gap-3 transition-all shadow-2xl border border-white/10 relative overflow-hidden",
                isUser
                    ? "bg-blue-600/10 shadow-[0_0_25px_rgba(37,99,235,0.15)] border-blue-500/30"
                    : "bg-white/5 shadow-[0_0_25px_rgba(255,255,255,0.08)] border-white/20"
            )}>
                <div className="flex gap-4">
                    {!isUser && (
                        <div className="w-8 h-8 rounded-xl bg-blue-500/10 flex items-center justify-center flex-shrink-0 mt-0.5 border border-white/5">
                            <Bot className="w-5 h-5 text-blue-400" />
                        </div>
                    )}

                    <div
                        className="text-sm leading-relaxed whitespace-pre-wrap font-normal select-text"
                        style={{
                            fontFamily: "var(--font-primary)",
                            color: isUser ? "#60a5fa" : "#ffffff",
                            filter: isUser
                                ? "drop-shadow(0 0 5px rgba(59, 130, 246, 0.5))"
                                : "drop-shadow(0 0 5px rgba(255, 255, 255, 0.4))",
                        }}
                    >
                        {message.content}
                    </div>

                    {isUser && (
                        <div className="w-8 h-8 rounded-xl bg-white/5 flex items-center justify-center flex-shrink-0 mt-0.5 border border-white/5">
                            <User className="w-5 h-5 text-blue-400" />
                        </div>
                    )}
                </div>

                {!isUser && message.pythonCode && (
                    <div className="rounded-xl overflow-hidden border border-white/10 bg-[#0d1117]">
                        <div className="flex items-center justify-between px-3 py-1.5 bg-white/5 border-b border-white/10">
                            <span className="text-xs text-slate-400 font-mono">python</span>
                            <button
                                onClick={handleSendToEditor}
                                className="text-xs text-blue-400 hover:text-blue-300 transition-colors px-2 py-0.5 rounded-md hover:bg-blue-500/10"
                            >
                                📋 Copy to Editor &amp; Open
                            </button>
                        </div>
                        <pre className="text-xs text-slate-300 font-mono p-3 overflow-x-auto max-h-48 leading-relaxed">
                            {message.pythonCode}
                        </pre>
                    </div>
                )}
            </div>
        </div>
    );
};
