import { MessageSquare } from 'lucide-react';
import { ChatInterface } from './chat/ChatInterface';

export const ChatPanel = () => {
    return (
        <div className="flex flex-col h-full bg-white border-r border-gray-200">
            <div className="p-3 border-b border-gray-200 flex items-center gap-2 bg-white shadow-sm z-10">
                <div className="p-1.5 bg-blue-50 rounded-md">
                    <MessageSquare className="w-5 h-5 text-blue-600" />
                </div>
                <div>
                    {/* Header Text Removed */}
                </div>
            </div>

            <div className="flex-1 overflow-hidden">
                <ChatInterface />
            </div>
        </div>
    );
};
