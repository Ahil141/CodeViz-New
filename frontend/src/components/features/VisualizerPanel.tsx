import { Eye, List, Search } from 'lucide-react';
import { useState, useEffect, useRef } from 'react';
import { useVisualization } from '../../services/VisualizationController';

// ---------------------------------------------------------------------------
// Injects a "tripwire" script into the <head> of the AI-generated HTML so
// that any uncaught runtime error inside the iframe fires a postMessage back
// to the parent, which then swaps the iframe to the safe fallback HTML.
// ---------------------------------------------------------------------------
function injectTripwire(html: string): string {
    const tripwire = `<script>window.onerror = function(msg, src, line, col, err) {
  window.parent.postMessage('AI_CRASHED', '*');
  return true;
};<\/script>`;

    // Try to insert after <head> tag (best practice)
    if (/<head[^>]*>/i.test(html)) {
        return html.replace(/(<head[^>]*>)/i, `$1${tripwire}`);
    }
    // No <head>: prepend the tripwire
    return tripwire + html;
}

// ---------------------------------------------------------------------------
// Sandboxed iframe renderer with automatic fallback
// ---------------------------------------------------------------------------
const SandboxedVisualizer = ({
    aiHtml,
    fallbackHtml,
}: {
    aiHtml: string | null;
    fallbackHtml: string | null;
}) => {
    // Start with the AI html (with tripwire injected); fall back if it crashes
    const [activeSrc, setActiveSrc] = useState<string>(() => {
        if (aiHtml) return injectTripwire(aiHtml);
        return fallbackHtml ?? '';
    });
    const [usingFallback, setUsingFallback] = useState(!aiHtml && !!fallbackHtml);
    const fallbackRef = useRef(fallbackHtml);
    fallbackRef.current = fallbackHtml;

    // When props change (new AI response), reset to the newest AI html
    useEffect(() => {
        if (aiHtml) {
            setActiveSrc(injectTripwire(aiHtml));
            setUsingFallback(false);
        } else if (fallbackHtml) {
            setActiveSrc(fallbackHtml);
            setUsingFallback(true);
        }
    }, [aiHtml, fallbackHtml]);

    // Listen for the tripwire signal
    useEffect(() => {
        const handleMessage = (event: MessageEvent) => {
            if (event.data === 'AI_CRASHED') {
                console.warn('AI visualizer crashed — switching to fallback.');
                if (fallbackRef.current) {
                    setActiveSrc(fallbackRef.current);
                    setUsingFallback(true);
                }
            }
        };
        window.addEventListener('message', handleMessage);
        return () => window.removeEventListener('message', handleMessage);
    }, []);

    if (!activeSrc) {
        return (
            <div className="flex items-center justify-center h-full text-slate-500 text-sm">
                No visualization available.
            </div>
        );
    }

    return (
        <div className="relative w-full h-full">
            {usingFallback && (
                <span className="absolute top-2 right-2 z-10 text-xs bg-yellow-500/20 text-yellow-300 border border-yellow-500/30 px-2 py-0.5 rounded-full">
                    fallback
                </span>
            )}
            <iframe
                key={activeSrc.slice(0, 40)}   /* force remount on src change */
                srcDoc={activeSrc}
                className="w-full h-full border-0"
                sandbox="allow-scripts allow-modals allow-forms"
                title="Data Structure Visualization"
            />
        </div>
    );
};

// ---------------------------------------------------------------------------
// Main panel
// ---------------------------------------------------------------------------
export const VisualizerPanel = () => {
    const {
        visualizationType,
        setVisualizationType,
        aiHtml,
        setAiHtml,
        fallbackHtml,
        setFallbackHtml,
        output,
    } = useVisualization();

    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const [searchTerm, setSearchTerm] = useState('');
    const [loading, setLoading] = useState(false);

    const availableVisualizers = [
        'Stack', 'Queue', 'Linked List', 'Heap', 'Binary Tree',
        'Bubble Sort', 'Graph',
    ];

    // Manual selection from the dropdown — fetches from the RAG endpoint
    const handleSelectVisualizer = async (name: string) => {
        setLoading(true);
        setIsMenuOpen(false);
        try {
            const response = await fetch('http://localhost:8000/api/v1/rag/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ data_structure_name: name }),
            });
            const data = await response.json();
            if (data.success && data.visualizer_code) {
                setAiHtml(data.visualizer_code);
                setFallbackHtml(null);
                setVisualizationType('data_structure');
            } else {
                console.error('Failed to fetch visualizer:', data.error);
            }
        } catch (error) {
            console.error('Error fetching visualizer:', error);
        } finally {
            setLoading(false);
        }
    };

    const renderContent = () => {
        if (loading) {
            return (
                <div className="flex flex-col items-center justify-center h-full text-gray-400">
                    <div className="w-8 h-8 border-4 border-purple-500 border-t-transparent rounded-full animate-spin mb-4" />
                    <p>Loading Visualizer...</p>
                </div>
            );
        }

        // Terminal output view
        if (visualizationType === 'output') {
            return (
                <div className="flex flex-col h-full bg-[#1e1e1e] text-white font-mono text-sm">
                    <div className="flex items-center gap-2 p-2 bg-[#2d2d2d] border-b border-[#3e3e3e] text-gray-300">
                        <span className="font-semibold">Terminal Output</span>
                    </div>
                    <pre className="flex-1 p-4 overflow-auto whitespace-pre-wrap">
                        {output ?? 'No output.'}
                    </pre>
                </div>
            );
        }

        // AI / fallback iframe renderer
        if (aiHtml || fallbackHtml) {
            return <SandboxedVisualizer aiHtml={aiHtml} fallbackHtml={fallbackHtml} />;
        }

        // Empty state
        return (
            <div className="flex flex-col items-center justify-center h-full text-slate-500 p-8 text-center bg-[#020617]">
                <div className="w-16 h-16 bg-white/5 rounded-2xl flex items-center justify-center mb-6 shadow-2xl border border-white/5">
                    <Eye className="w-8 h-8 text-blue-500/50" />
                </div>
                <h3
                    className="text-xl font-normal text-white mb-3 tracking-tight select-none"
                    style={{
                        fontFamily: 'var(--font-futuristic)',
                        filter: 'drop-shadow(0 0 8px rgba(255,255,255,0.4)) drop-shadow(0 0 20px rgba(255,255,255,0.2))',
                    }}
                >
                    No Visualization Active
                </h3>
                <p className="text-sm text-slate-400 max-w-[240px] leading-relaxed">
                    Select a data structure from the menu or ask the chat to{' '}
                    <span className="text-blue-400">"Show me a Stack"</span>.
                </p>
            </div>
        );
    };

    return (
        <div className="flex flex-col h-full bg-[#020617] border-l border-white/5 relative">
            {/* Header */}
            <div className="p-4 border-b border-white/5 flex items-center justify-between bg-[#030712]/50 backdrop-blur-md z-10 shadow-2xl">
                <div className="flex items-center gap-2">
                    <button
                        onClick={() => setIsMenuOpen(!isMenuOpen)}
                        className="p-1 hover:bg-white/5 rounded-lg text-slate-400 transition-colors"
                        title="Available Visualizers"
                    >
                        <List className="w-5 h-5" />
                    </button>
                    <h2
                        className="text-sm font-normal text-white select-none whitespace-nowrap"
                        style={{
                            fontFamily: 'var(--font-futuristic)',
                            filter: 'drop-shadow(0 0 5px rgba(255,255,255,0.5))',
                        }}
                    >
                        {visualizationType
                            ? visualizationType.replace(/_/g, ' ').toUpperCase()
                            : 'VISUALIZATION'}
                    </h2>
                </div>

                {(aiHtml || fallbackHtml) && (
                    <span className="text-xs bg-blue-500/10 text-blue-400 px-2 py-1 rounded-full font-medium border border-blue-500/20">
                        Interactive
                    </span>
                )}
            </div>

            {/* Dropdown Menu */}
            {isMenuOpen && (
                <div className="absolute top-14 left-4 bg-[#0f172a] shadow-[0_20px_50px_rgba(0,0,0,0.5)] rounded-2xl border border-white/10 w-64 z-50 backdrop-blur-xl overflow-hidden">
                    <div className="p-3 border-b border-white/5 flex items-center gap-2 bg-white/5">
                        <Search className="w-4 h-4 text-slate-500" />
                        <input
                            type="text"
                            placeholder="Search..."
                            className="text-sm w-full outline-none bg-transparent text-slate-200 placeholder-slate-500"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>
                    <div className="max-h-64 overflow-y-auto p-2 space-y-1">
                        {availableVisualizers
                            .filter(v => v.toLowerCase().includes(searchTerm.toLowerCase()))
                            .map(v => (
                                <button
                                    key={v}
                                    onClick={() => handleSelectVisualizer(v)}
                                    className="w-full text-left px-3 py-2 text-sm text-slate-400 hover:bg-blue-600/20 hover:text-blue-400 rounded-xl transition-all"
                                >
                                    {v}
                                </button>
                            ))}
                    </div>
                </div>
            )}

            {/* Main Content */}
            <div className="flex-1 overflow-hidden relative">
                {renderContent()}
            </div>
        </div>
    );
};
