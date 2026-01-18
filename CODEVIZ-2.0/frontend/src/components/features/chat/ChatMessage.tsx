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
            "flex w-full mb-4 px-2",
            isUser ? "justify-end" : "justify-start"
        )}>
            <div className={cn(
                "flex max-w-[85%] rounded-lg p-3 gap-3",
                isUser ? "bg-blue-600 text-white" : "bg-white border border-gray-200 shadow-sm"
            )}>
                {!isUser && (
                    <div className="w-6 h-6 rounded-full bg-purple-100 flex items-center justify-center flex-shrink-0 mt-1">
                        <Bot className="w-4 h-4 text-purple-600" />
                    </div>
                )}

                <div className="text-sm leading-relaxed whitespace-pre-wrap">
                    {message.content}
                </div>

                {isUser && (
                    <div className="w-6 h-6 rounded-full bg-blue-500 flex items-center justify-center flex-shrink-0 mt-1">
                        <User className="w-4 h-4 text-white" />
                    </div>
                )}
            </div>
        </div>
    );
};
