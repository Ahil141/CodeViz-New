import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { BaseVisualizer } from '../BaseVisualizer';
import { Plus, Trash2, Edit, Play } from 'lucide-react';

interface ArrayState {
    items: number[];
    message: string;
    activeIndices: number[]; // For highlighting during traversal or operations
}

export const ArrayVisualizer = () => {
    const [history, setHistory] = useState<ArrayState[]>([
        { items: [10, 20, 30, 40], message: 'Initial Array.', activeIndices: [] }
    ]);
    const [currentStep, setCurrentStep] = useState(0);
    const [inputValue, setInputValue] = useState('');
    const [indexValue, setIndexValue] = useState('0');
    const [isPlaying, setIsPlaying] = useState(false);

    const currentState = history[currentStep];

    // Playback Logic
    useEffect(() => {
        if (!isPlaying) return;

        const interval = setInterval(() => {
            setCurrentStep(prev => {
                if (prev >= history.length - 1) {
                    setIsPlaying(false);
                    return prev;
                }
                const next = prev + 1;
                if (next >= history.length - 1) {
                    setIsPlaying(false);
                }
                return next;
            });
        }, 1000);

        return () => clearInterval(interval);
    }, [isPlaying, history.length]);

    const addToHistory = (newState: ArrayState) => {
        const newHistory = [...history.slice(0, currentStep + 1), newState];
        setHistory(newHistory);
        setCurrentStep(newHistory.length - 1);
    };

    const parseInput = () => {
        const val = parseInt(inputValue);
        const idx = parseInt(indexValue);
        if (isNaN(val) || isNaN(idx)) return null;
        return { val, idx };
    };

    const handleInsert = () => {
        const inputs = parseInput();
        if (!inputs) return;
        const { val, idx } = inputs;

        if (idx < 0 || idx > currentState.items.length) {
            alert("Index out of bounds!");
            return;
        }
        if (currentState.items.length >= 8) {
            alert("Array full! Max 8 items.");
            return;
        }

        const newItems = [...currentState.items];
        newItems.splice(idx, 0, val);

        addToHistory({
            items: newItems,
            message: `Inserted ${val} at index ${idx}. Elements shifted right.`,
            activeIndices: [idx]
        });
        setInputValue('');
    };

    const handleDelete = () => {
        const idx = parseInt(indexValue);
        if (isNaN(idx) || idx < 0 || idx >= currentState.items.length) {
            alert("Invalid Index!");
            return;
        }

        const item = currentState.items[idx];
        const newItems = [...currentState.items];
        newItems.splice(idx, 1);

        addToHistory({
            items: newItems,
            message: `Deleted ${item} from index ${idx}. Elements shifted left.`,
            activeIndices: [] // Highlighting handled by exit animation mostly
        });
    };

    const handleUpdate = () => {
        const inputs = parseInput();
        if (!inputs) return;
        const { val, idx } = inputs;

        if (idx < 0 || idx >= currentState.items.length) {
            alert("Index out of bounds!");
            return;
        }

        const newItems = [...currentState.items];
        newItems[idx] = val;

        addToHistory({
            items: newItems,
            message: `Updated index ${idx} to ${val}.`,
            activeIndices: [idx]
        });
        setInputValue('');
    };

    // Traversal is a multi-step operation, usually best handled by generating multiple history steps automatically
    const handleTraverse = () => {
        if (currentState.items.length === 0) return;

        // We will generate N steps and add them all to history immediately
        const steps: ArrayState[] = [];
        const baseItems = currentState.items;

        for (let i = 0; i < baseItems.length; i++) {
            steps.push({
                items: baseItems,
                message: `Traversing: Visited index ${i} (Value: ${baseItems[i]})`,
                activeIndices: [i]
            });
        }

        // Append last step clearing highlight
        steps.push({
            items: baseItems,
            message: 'Traversal Complete.',
            activeIndices: []
        });

        const newHistory = [...history.slice(0, currentStep + 1), ...steps];
        setHistory(newHistory);
        // Auto-play the traversal
        setCurrentStep(currentStep + 1); // Start first step
        setIsPlaying(true);
    };

    return (
        <BaseVisualizer
            title="Array Visualization"
            description="Fundamental linear data structure with contiguous memory locations."
            currentStep={currentStep}
            totalSteps={history.length}
            isPlaying={isPlaying}
            onPlayPause={() => setIsPlaying(!isPlaying)}
            onNext={() => setCurrentStep(Math.min(currentStep + 1, history.length - 1))}
            onPrev={() => setCurrentStep(Math.max(currentStep - 1, 0))}
            onReset={() => setCurrentStep(0)}
            speed={1000}
            onSpeedChange={() => { }}
        >
            <div className="flex flex-col items-center gap-8 w-full max-w-3xl">

                {/* Operations Panel */}
                <div className="flex flex-wrap items-center justify-center gap-4 w-full bg-white p-4 rounded-lg shadow-sm border border-gray-200">

                    <div className="flex items-center gap-2">
                        <input
                            type="number"
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                            placeholder="Val"
                            className="w-16 px-2 py-1 border rounded text-sm focus:outline-blue-500"
                        />
                        <span className="text-gray-400">@</span>
                        <input
                            type="number"
                            value={indexValue}
                            onChange={(e) => setIndexValue(e.target.value)}
                            placeholder="Idx"
                            className="w-14 px-2 py-1 border rounded text-sm focus:outline-blue-500"
                        />
                    </div>

                    <div className="w-px h-8 bg-gray-200 hidden md:block"></div>

                    <div className="flex gap-2">
                        <button onClick={handleInsert} className="flex items-center gap-1 bg-blue-100 text-blue-700 px-2 py-1 rounded text-xs hover:bg-blue-200 transition-colors">
                            <Plus className="w-3 h-3" /> Ins
                        </button>
                        <button onClick={handleUpdate} className="flex items-center gap-1 bg-green-100 text-green-700 px-2 py-1 rounded text-xs hover:bg-green-200 transition-colors">
                            <Edit className="w-3 h-3" /> Upd
                        </button>
                        <button onClick={handleDelete} className="flex items-center gap-1 bg-red-100 text-red-700 px-2 py-1 rounded text-xs hover:bg-red-200 transition-colors">
                            <Trash2 className="w-3 h-3" /> Del
                        </button>
                    </div>

                    <div className="w-px h-8 bg-gray-200 hidden md:block"></div>

                    <button onClick={handleTraverse} className="flex items-center gap-1 bg-purple-100 text-purple-700 px-3 py-1 rounded text-xs hover:bg-purple-200 transition-colors">
                        <Play className="w-3 h-3" /> Traverse
                    </button>
                </div>

                {/* Message Area */}
                <div className="min-h-[24px] text-center font-medium text-gray-600">
                    {currentState.message}
                </div>

                {/* Visualization Canvas */}
                <div className="flex items-center justify-center w-full min-h-[120px] bg-gray-50/50 rounded-lg p-8">
                    <div className="flex items-center gap-1">
                        <AnimatePresence mode="popLayout">
                            {currentState.items.map((item, index) => (
                                <motion.div
                                    key={index}
                                    layout
                                    initial={{ opacity: 0, scale: 0.8, y: -20 }}
                                    animate={{
                                        opacity: 1,

                                        y: 0,
                                        backgroundColor: currentState.activeIndices.includes(index) ? '#dbeafe' : '#ffffff',
                                        borderColor: currentState.activeIndices.includes(index) ? '#2563eb' : '#e5e7eb',
                                        scale: currentState.activeIndices.includes(index) ? 1.1 : 1
                                    }}
                                    exit={{ opacity: 0, scale: 0.8, y: 20 }}
                                    transition={{ type: "spring", stiffness: 300, damping: 25 }}
                                    className="w-14 h-14 flex flex-col items-center justify-center rounded-md border-2 shadow-sm text-lg font-bold text-gray-700 relative bg-white"
                                >
                                    {item}
                                    <span className="absolute -bottom-6 text-[10px] text-gray-400 font-normal">
                                        {index}
                                    </span>
                                </motion.div>
                            ))}
                        </AnimatePresence>

                        {currentState.items.length === 0 && (
                            <div className="text-gray-300 text-sm pointer-events-none">
                                Empty Array
                            </div>
                        )}
                    </div>
                </div>

            </div>
        </BaseVisualizer>
    );
};
