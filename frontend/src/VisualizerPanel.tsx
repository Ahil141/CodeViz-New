import { Eye } from 'lucide-react';
import { useState, useEffect, useRef } from 'react';
import { useVisualization } from './VisualizationController';

// Injects an onerror tripwire so AI crashes fall back to the hardcoded visualizer
function injectTripwire(html: string): string {
    const tripwire = `<script>window.onerror = function(msg, src, line, col, err) {
  window.parent.postMessage('AI_CRASHED', '*');
  return true;
};<\/script>`;
    if (/<head[^>]*>/i.test(html)) {
        return html.replace(/(<head[^>]*>)/i, `$1${tripwire}`);
    }
    return tripwire + html;
}

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

    useEffect(() => {
        if (aiHtml) {
            setActiveSrc(injectTripwire(aiHtml));
            setUsingFallback(false);
        } else if (fallbackHtml) {
            setActiveSrc(fallbackHtml);
            setUsingFallback(true);
        }
    }, [aiHtml, fallbackHtml]);

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

export const VisualizerPanel = () => {
    const {
        visualizationType,
        aiHtml,
        fallbackHtml,
        output,
    } = useVisualization();

    const renderContent = () => {
        if (visualizationType === 'output') {
            return (
                <div className="flex flex-col h-full bg-[#0d1117] font-mono text-sm">
                    <pre className="flex-1 p-4 overflow-auto whitespace-pre-wrap text-green-400 text-xs leading-relaxed">
                        {output || 'No output.'}
                    </pre>
                </div>
            );
        }
        if (aiHtml || fallbackHtml) {
            return <SandboxedVisualizer aiHtml={aiHtml} fallbackHtml={fallbackHtml} />;
        }
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
            <div className="px-3 py-[18px] border-b border-white/5 flex items-center justify-between bg-[#030712]/50 backdrop-blur-md z-10 shadow-2xl">
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

                {(aiHtml || fallbackHtml) && (
                    <span className="text-xs bg-blue-500/10 text-blue-400 px-2 py-1 rounded-full font-medium border border-blue-500/20">
                        Interactive
                    </span>
                )}
            </div>

            <div className="flex-1 overflow-hidden relative">
                {renderContent()}
            </div>
        </div>
    );
};
