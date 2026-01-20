import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { BaseVisualizer } from '../BaseVisualizer';
import { Plus, Trash2, Eye } from 'lucide-react';

interface StackState {
    items: number[];
    message: string;
    highlightIndex: number | null;
}

export const StackVisualizer = () => {
    const [history, setHistory] = useState<StackState[]>([
        { items: [], message: 'Stack is empty. Start by pushing an item.', highlightIndex: null }
    ]);
    const [currentStep, setCurrentStep] = useState(0);
    const [inputValue, setInputValue] = useState('');
    const [isPlaying, setIsPlaying] = useState(false);

    const currentState = history[currentStep];

    // Playback Logic
    useEffect(() => {
        let interval: any;
        if (isPlaying && currentStep < history.length - 1) {
            interval = setInterval(() => {
                setCurrentStep(prev => prev + 1);
            }, 1000); // Default speed, can be connected to props later
        } else if (currentStep >= history.length - 1) {
            setIsPlaying(false);
        }
        return () => clearInterval(interval);
    }, [isPlaying, currentStep, history.length]);

    const addToHistory = (newState: StackState) => {
        const newHistory = [...history.slice(0, currentStep + 1), newState];
        setHistory(newHistory);
        setCurrentStep(newHistory.length - 1);
    };

    const handlePush = () => {
        if (!inputValue) return;
        const num = parseInt(inputValue);
        if (isNaN(num)) return;

        if (currentState.items.length >= 8) {
            alert("Stack overflow! Max 8 items for visualization.");
            return;
        }

        addToHistory({
            items: [num, ...currentState.items], // Stack acts as LIFO, pushing to front for visual stacking
            message: `Pushed ${num} to the stack.`,
            highlightIndex: 0
        });
        setInputValue('');
    };

    const handlePop = () => {
        if (currentState.items.length === 0) {
            addToHistory({
                items: [],
                message: 'Stack Underflow! Cannot pop from empty stack.',
                highlightIndex: null
            });
            return;
        }

        const [popped, ...rest] = currentState.items;
        addToHistory({
            items: rest,
            message: `Popped ${popped} from the stack.`,
            highlightIndex: null
        });
    };

    const handlePeek = () => {
        if (currentState.items.length === 0) {
            addToHistory({
                ...currentState,
                message: 'Stack is empty. Nothing to peek.',
                highlightIndex: null
            });
            return;
        }
        addToHistory({
            ...currentState,
            message: `Top element is ${currentState.items[0]}.`,
            highlightIndex: 0
        });
    };

    return (
        <BaseVisualizer
            title="Stack Visualization"
            description="A Stack is a Last-In-First-Out (LIFO) data structure."
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
            <div className="flex flex-col items-center gap-8 w-full max-w-md">

                {/* Operations Panel */}
                <div className="flex gap-2 w-full bg-white p-4 rounded-lg shadow-sm border border-gray-200">
                    <div className="flex-1 flex gap-2">
                        <input
                            type="number"
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                            placeholder="Value"
                            className="w-20 px-2 py-1 border rounded text-sm focus:outline-blue-500"
                            onKeyDown={(e) => e.key === 'Enter' && handlePush()}
                        />
                        <button onClick={handlePush} className="flex-1 flex items-center justify-center gap-1 bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700 transition-colors">
                            <Plus className="w-3 h-3" /> Push
                        </button>
                    </div>

                    <button onClick={handlePop} className="flex items-center gap-1 bg-red-100 text-red-700 px-3 py-1 rounded text-sm hover:bg-red-200 transition-colors">
                        <Trash2 className="w-3 h-3" /> Pop
                    </button>

                    <button onClick={handlePeek} className="flex items-center gap-1 bg-purple-100 text-purple-700 px-3 py-1 rounded text-sm hover:bg-purple-200 transition-colors">
                        <Eye className="w-3 h-3" /> Peek
                    </button>
                </div>

                {/* Message Area */}
                <div className="min-h-[24px] text-center font-medium text-gray-600">
                    {currentState.message}
                </div>

                {/* Visualization Canvas */}
                <div className="flex flex-col-reverse items-center justify-end w-40 min-h-[300px] border-b-4 border-l-4 border-r-4 border-gray-400 rounded-b-lg p-2 bg-gray-50/50 relative">
                    <AnimatePresence>
                        {currentState.items.map((item, index) => (
                            <motion.div
                                key={`${item}-${currentState.items.length - index}`} // Unique key for LIFO order
                                layout
                                initial={{ opacity: 0, y: -50, scale: 0.8 }}
                                animate={{
                                    opacity: 1,
                                    y: 0,
                                    scale: 1,
                                    backgroundColor: index === currentState.highlightIndex ? '#dbeafe' : '#ffffff', // blue-100 vs white
                                    borderColor: index === currentState.highlightIndex ? '#2563eb' : '#e5e7eb' // blue-600 vs gray-200
                                }}
                                exit={{ opacity: 0, scale: 0.8, x: 50 }}
                                transition={{ type: "spring", stiffness: 300, damping: 25 }}
                                className="w-full h-12 flex items-center justify-center rounded-md border-2 shadow-sm text-lg font-bold text-gray-700 mb-2 last:mb-0 relative"
                            >
                                {item}
                                <span className="absolute -left-12 text-xs text-gray-400 font-normal">
                                    Index {currentState.items.length - 1 - index}
                                </span>
                            </motion.div>
                        ))}
                    </AnimatePresence>

                    {currentState.items.length === 0 && (
                        <div className="absolute inset-0 flex items-center justify-center text-gray-300 text-sm pointer-events-none">
                            Empty Stack
                        </div>
                    )}
                </div>

            </div>
        </BaseVisualizer>
    );
};
