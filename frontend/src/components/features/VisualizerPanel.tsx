import { Eye, List, Search, Terminal, Code } from 'lucide-react';
import { useState } from 'react';
import { useVisualization } from '../../services/VisualizationController';
import Visualizer from './Visualizer'; // The new component
// Keep existing imports for native fallback if needed
import { StackVisualizer } from '../dataStructures/stack/StackVisualizer';

export const VisualizerPanel = () => {
    const { visualizationType, code, setCode, setVisualizationType, output, implementationCode } = useVisualization();
    const [isMenuOpen, setIsMenuOpen] = useState(false);
    const [searchTerm, setSearchTerm] = useState('');
    const [loading, setLoading] = useState(false);
    const [showImplementation, setShowImplementation] = useState(false);

    // List of available DS for manual selection
    const availableVisualizers = [
        "Stack", "Bubble Sort", "Queue", "Linked List", "Binary Tree"
    ];

    const handleSelectVisualizer = async (name: string) => {
        setLoading(true);
        setIsMenuOpen(false);
        try {
            const response = await fetch('http://localhost:8000/api/v1/rag/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ data_structure_name: name })
            });
            const data = await response.json();

            if (data.success && data.visualizer_code) {
                setCode(data.visualizer_code);
                setVisualizationType('html'); // Force HTML renderer
            } else {
                console.error("Failed to fetch visualizer:", data.error);
                // Fallback to purely setting type if native component exists
                setVisualizationType(name.toLowerCase().replace(" ", "_"));
            }
        } catch (error) {
            console.error("Error fetching visualizer:", error);
        } finally {
            setLoading(false);
        }
    };

    const renderContent = () => {
        if (loading) {
            return (
                <div className="flex flex-col items-center justify-center h-full text-gray-400">
                    <div className="w-8 h-8 border-4 border-purple-500 border-t-transparent rounded-full animate-spin mb-4"></div>
                    <p>Loading Visualizer...</p>
                </div>
            );
        }

        // 0. Show Implementation Code (New Feature)
        if (showImplementation && implementationCode) {
            return (
                <div className="flex flex-col h-full bg-[#1e1e1e] text-white">
                    <div className="flex items-center justify-between p-2 bg-[#2d2d2d] border-b border-[#3e3e3e]">
                        <span className="text-sm text-gray-300 font-mono">implementation.py</span>
                        <button
                            onClick={() => navigator.clipboard.writeText(implementationCode)}
                            className="text-xs bg-gray-700 hover:bg-gray-600 px-2 py-1 rounded text-gray-200 transition-colors"
                        >
                            Copy Code
                        </button>
                    </div>
                    <pre className="flex-1 p-4 overflow-auto font-mono text-sm leading-relaxed">
                        {implementationCode}
                    </pre>
                </div>
            );
        }

        // 1. Execution Output
        if (visualizationType === 'output') {
            return (
                <div className="flex flex-col h-full bg-[#1e1e1e] text-white font-mono text-sm">
                    <div className="flex items-center gap-2 p-2 bg-[#2d2d2d] border-b border-[#3e3e3e] text-gray-300">
                        <Terminal className="w-4 h-4" />
                        <span className="font-semibold">Terminal Output</span>
                    </div>
                    <pre className="flex-1 p-4 overflow-auto whitespace-pre-wrap">
                        {output || "No output."}
                    </pre>
                </div>
            );
        }

        // 2. RAG/Code based visualization (Priority)
        if (visualizationType === 'html' && code) {
            return <Visualizer code={code} title={visualizationType || 'Visualization'} />;
        }

        // 3. Generic Code Fallback
        if (code && code.length > 50 && (!visualizationType || visualizationType === 'data_structure')) {
            return <Visualizer code={code} title={visualizationType || 'Visualization'} />;
        }

        // 4. Native Component Fallback
        switch (visualizationType?.toLowerCase()) {
            case 'stack': return <StackVisualizer />;
            case 'queue': return <StackVisualizer />; // Placeholder if queue not implemented or native
            // We can add back other native components if imports are restored
            default:
                break;
        }

        // If no code and no native component, show instructions
        return (
            <div className="flex flex-col items-center justify-center h-full text-gray-400 p-8 text-center">
                <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
                    <Eye className="w-8 h-8 text-gray-400" />
                </div>
                <h3 className="text-lg font-medium text-gray-600 mb-2">No Visualization Active</h3>
                <p className="text-sm">
                    Select a data structure from the menu or ask the chat to "Show me a Stack".
                </p>
            </div>
        );
    };

    return (
        <div className="flex flex-col h-full bg-slate-50 border-l border-gray-200 relative">
            {/* Header */}
            <div className="p-4 border-b border-gray-200 flex items-center justify-between bg-white z-10">
                <div className="flex items-center gap-2">
                    <button
                        onClick={() => setIsMenuOpen(!isMenuOpen)}
                        className="p-1 hover:bg-gray-100 rounded text-gray-600"
                        title="Available Visualizers"
                    >
                        <List className="w-5 h-5" />
                    </button>
                    <h2 className="font-semibold text-gray-800">
                        {visualizationType ? visualizationType.replace(/_/g, ' ').toUpperCase() : 'Visualization'}
                    </h2>
                </div>

                <div className="flex items-center gap-2">
                    {/* Show Code Button */}
                    {implementationCode && (
                        <button
                            onClick={() => setShowImplementation(!showImplementation)}
                            className={`flex items-center gap-1 px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${showImplementation
                                    ? 'bg-purple-100 text-purple-700'
                                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                                }`}
                            title={showImplementation ? "Show Visualization" : "Show Implementation Code"}
                        >
                            <Code className="w-4 h-4" />
                            {showImplementation ? 'Hide Code' : 'Show Code'}
                        </button>
                    )}

                    {visualizationType && (
                        <span className="text-xs bg-purple-100 text-purple-700 px-2 py-1 rounded-full font-medium">
                            Interactive
                        </span>
                    )}
                </div>
            </div>

            {/* Dropdown Menu for Selection */}
            {isMenuOpen && (
                <div className="absolute top-14 left-4 bg-white shadow-xl rounded-lg border border-gray-200 w-64 z-50">
                    <div className="p-2 border-b border-gray-100 flex items-center gap-2">
                        <Search className="w-4 h-4 text-gray-400" />
                        <input
                            type="text"
                            placeholder="Search..."
                            className="text-sm w-full outline-none"
                            value={searchTerm}
                            onChange={(e) => setSearchTerm(e.target.value)}
                        />
                    </div>
                    <div className="max-h-64 overflow-y-auto p-1">
                        {availableVisualizers
                            .filter(v => v.toLowerCase().includes(searchTerm.toLowerCase()))
                            .map(v => (
                                <button
                                    key={v}
                                    onClick={() => handleSelectVisualizer(v)}
                                    className="w-full text-left px-3 py-2 text-sm text-gray-700 hover:bg-purple-50 hover:text-purple-700 rounded transition-colors"
                                >
                                    {v}
                                </button>
                            ))
                        }
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


