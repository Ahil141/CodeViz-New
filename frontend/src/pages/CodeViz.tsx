import { useState } from 'react';
import { Code2 } from 'lucide-react';
import { ChatPanel } from '../components/features/ChatPanel';
import { CodeEditor } from '../components/features/CodeEditor';
import { VisualizerPanel } from '../components/features/VisualizerPanel';

export const CodeViz = () => {
    const [showEditor, setShowEditor] = useState(false);

    return (
        <div className="min-h-screen bg-gray-100 flex flex-col">
            {/* Header */}
            <header className="bg-white shadow-sm px-6 py-3 flex items-center justify-between z-10">
                <div className="flex items-center gap-6">
                    <div className="font-bold text-xl bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                        CodeViz
                    </div>
                    <button
                        onClick={() => setShowEditor(!showEditor)}
                        className={`flex items-center gap-2 px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${showEditor
                            ? 'bg-blue-100 text-blue-700 hover:bg-blue-200'
                            : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                            }`}
                    >
                        <Code2 className="w-4 h-4" />
                        {showEditor ? 'Hide Editor' : 'Show Editor'}
                    </button>
                </div>
                <div className="text-sm text-gray-500">
                    Draft Workspace
                </div>
            </header>

            {/* Main Content Grid */}
            <main className="flex-1 grid grid-cols-1 lg:grid-cols-12 overflow-hidden h-[calc(100vh-56px)]">

                {/* Left Panel: Chat */}
                <section className={`col-span-1 border-b lg:border-b-0 lg:border-r border-gray-200 overflow-hidden h-1/3 lg:h-full ${showEditor ? 'lg:col-span-3' : 'lg:col-span-7'
                    }`}>
                    <ChatPanel />
                </section>

                {/* Center Panel: Editor */}
                <section className={`col-span-1 border-b lg:border-b-0 lg:border-r border-gray-200 overflow-hidden relative h-1/3 lg:h-full ${showEditor ? 'lg:col-span-5' : 'hidden'
                    }`}>
                    <CodeEditor />
                </section>

                {/* Right Panel: Visualization */}
                <section className={`col-span-1 overflow-hidden h-1/3 lg:h-full ${showEditor ? 'lg:col-span-4' : 'lg:col-span-5'
                    }`}>
                    <VisualizerPanel />
                </section>

            </main>
        </div>
    );
};
