import { MessageSquare } from 'lucide-react';
import { ChatInterface } from './chat/ChatInterface';

export const ChatPanel = () => {
    return (
        <div className="flex flex-col h-full bg-[#030712] border-r border-white/5">
            <div className="p-3 border-b border-white/5 flex items-center gap-2 bg-[#030712]/50 backdrop-blur-md shadow-2xl z-10">
                <div className="p-1.5 bg-blue-500/10 rounded-lg">
                    <MessageSquare className="w-5 h-5 text-blue-400" />
                </div>
            </div>

            <div className="flex-1 overflow-hidden">
                <ChatInterface />
            </div>
        </div>
    );
};
