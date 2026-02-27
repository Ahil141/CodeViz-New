import { useState } from 'react';
import { Code2 } from 'lucide-react';
import { ChatPanel } from '../components/features/ChatPanel';
import { CodeEditor } from '../components/features/CodeEditor';
import { VisualizerPanel } from '../components/features/VisualizerPanel';

export const CodeViz = () => {
    const [showEditor, setShowEditor] = useState(false);

    return (
        <div className="min-h-screen bg-[#020617] flex flex-col text-slate-100">
            <header className="bg-white/5 backdrop-blur-xl border-b border-white/10 px-6 py-4 flex items-center justify-between z-10 shadow-2xl relative">
                <div className="flex items-center gap-8">
                    <div
                        className="text-xl font-normal tracking-tight select-none cursor-pointer hover:opacity-80 transition-opacity"
                        style={{
                            fontFamily: "var(--font-futuristic)",
                            color: "#ffffff",
                            filter: "drop-shadow(0 0 5px rgba(59, 130, 246, 0.6)) drop-shadow(0 0 15px rgba(59, 130, 246, 0.3))"
                        }}
                    >
                        CodeViz
                    </div>
                    <button
                        onClick={() => setShowEditor(!showEditor)}
                        className={`flex items-center gap-2 px-4 py-2 rounded-xl text-xs font-bold uppercase tracking-widest transition-all duration-300 border ${showEditor
                            ? 'bg-blue-600/20 border-blue-500/50 text-white shadow-[0_0_20px_rgba(37,99,235,0.3)]'
                            : 'bg-white/5 border-white/10 text-slate-400 hover:bg-white/10 hover:border-white/20'
                            }`}
                    >
                        <Code2 className="w-3.5 h-3.5" />
                        {showEditor ? 'Hide Editor' : 'Show Editor'}
                    </button>
                </div>
                <div className="text-sm text-slate-400 font-medium">
                    Draft Workspace
                </div>
            </header>

            <main className="flex-1 grid grid-cols-1 lg:grid-cols-12 overflow-hidden h-[calc(100vh-56px)] bg-[#020617]">
                <section className={`col-span-1 border-b lg:border-b-0 lg:border-r border-white/5 overflow-hidden h-1/3 lg:h-full ${showEditor ? 'lg:col-span-3' : 'lg:col-span-6'}`}>
                    <ChatPanel />
                </section>

                <section className={`col-span-1 border-b lg:border-b-0 lg:border-r border-white/5 overflow-hidden relative h-1/3 lg:h-full ${showEditor ? 'lg:col-span-5' : 'hidden'}`}>
                    <CodeEditor />
                </section>

                <section className={`col-span-1 overflow-hidden h-1/3 lg:h-full ${showEditor ? 'lg:col-span-4' : 'lg:col-span-6'}`}>
                    <VisualizerPanel />
                </section>
            </main>
        </div>
    );
};
