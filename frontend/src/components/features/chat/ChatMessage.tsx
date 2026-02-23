import type { Message } from '../../../types';
import { cn } from '../../../lib/utils';
import { Bot, User } from 'lucide-react';

interface ChatMessageProps {
    message: Message;
}

export const ChatMessage = ({ message }: ChatMessageProps) => {
    const isUser = message.role === 'user';

    return (
        <div className={cn(
            "flex w-full mb-6 px-4",
            isUser ? "justify-end" : "justify-start"
        )}>
            <div className={cn(
                "flex max-w-[80%] rounded-2xl p-4 gap-4 transition-all shadow-2xl border border-white/10 relative overflow-hidden",
                "bg-[#000000]",
                isUser
                    ? "bg-blue-600/10 shadow-[0_0_25px_rgba(37,99,235,0.15)] border-blue-500/30"
                    : "bg-white/5 shadow-[0_0_25px_rgba(255,255,255,0.08)] border-white/20"
            )}>
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
                        opacity: 1
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
        </div>
    );
};
