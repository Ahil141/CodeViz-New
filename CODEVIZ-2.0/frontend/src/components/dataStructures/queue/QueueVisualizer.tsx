import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { BaseVisualizer } from '../BaseVisualizer';
import { Plus, Trash2, ArrowRight } from 'lucide-react';

interface QueueState {
    items: number[];
    message: string;
    activeOperation: 'enqueue' | 'dequeue' | null;
}

export const QueueVisualizer = () => {
    const [history, setHistory] = useState<QueueState[]>([
        { items: [], message: 'Queue is empty. Start by enqueuing an item.', activeOperation: null }
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
            }, 1000);
        } else if (currentStep >= history.length - 1) {
            setIsPlaying(false);
        }
        return () => clearInterval(interval);
    }, [isPlaying, currentStep, history.length]);

    const addToHistory = (newState: QueueState) => {
        const newHistory = [...history.slice(0, currentStep + 1), newState];
        setHistory(newHistory);
        setCurrentStep(newHistory.length - 1);
    };

    const handleEnqueue = () => {
        if (!inputValue) return;
        const num = parseInt(inputValue);
        if (isNaN(num)) return;

        if (currentState.items.length >= 7) {
            alert("Queue full! Max 7 items for visualization.");
            return;
        }

        addToHistory({
            items: [...currentState.items, num], // Append to end
            message: `Enqueued ${num} to the rear.`,
            activeOperation: 'enqueue'
        });
        setInputValue('');
    };

    const handleDequeue = () => {
        if (currentState.items.length === 0) {
            addToHistory({
                items: [],
                message: 'Queue Underflow! Cannot dequeue from empty queue.',
                activeOperation: null
            });
            return;
        }

        const [removed, ...rest] = currentState.items;
        addToHistory({
            items: rest,
            message: `Dequeued ${removed} from the front.`,
            activeOperation: 'dequeue'
        });
    };

    return (
        <BaseVisualizer
            title="Queue Visualization"
            description="A Queue is a First-In-First-Out (FIFO) data structure."
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
            <div className="flex flex-col items-center gap-8 w-full max-w-2xl">

                {/* Operations Panel */}
                <div className="flex gap-2 w-full max-w-md bg-white p-4 rounded-lg shadow-sm border border-gray-200">
                    <div className="flex-1 flex gap-2">
                        <input
                            type="number"
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                            placeholder="Value"
                            className="w-20 px-2 py-1 border rounded text-sm focus:outline-blue-500"
                            onKeyDown={(e) => e.key === 'Enter' && handleEnqueue()}
                        />
                        <button onClick={handleEnqueue} className="flex-1 flex items-center justify-center gap-1 bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700 transition-colors">
                            <Plus className="w-3 h-3" /> Enqueue
                        </button>
                    </div>

                    <button onClick={handleDequeue} className="flex items-center gap-1 bg-red-100 text-red-700 px-3 py-1 rounded text-sm hover:bg-red-200 transition-colors">
                        <Trash2 className="w-3 h-3" /> Dequeue
                    </button>
                </div>

                {/* Message Area */}
                <div className="min-h-[24px] text-center font-medium text-gray-600">
                    {currentState.message}
                </div>

                {/* Visualization Canvas */}
                {/* Horizontal Layout for Queue */}
                <div className="flex items-center justify-center w-full min-h-[120px] bg-gray-50/50 rounded-lg p-8 relative overflow-hidden">

                    {/* Labels */}
                    {currentState.items.length > 0 && (
                        <>
                            <div className="absolute left-4 top-1/2 -translate-y-1/2 text-xs font-bold text-red-500 -rotate-90 origin-center">FRONT</div>
                            <div className="absolute right-4 top-1/2 -translate-y-1/2 text-xs font-bold text-blue-500 -rotate-90 origin-center">REAR</div>
                        </>
                    )}

                    <div className="flex items-center gap-4">
                        <AnimatePresence mode="popLayout">
                            {currentState.items.map((item, index) => (
                                <motion.div
                                    key={`${item}-${index}`} // Composite key to ensure uniqueness relative to position in this specific history flow isn't strictly necessary if items are unique, but better safe. Actually, index changes on dequeue, so we need a stable ID if possible, but for simple numbers, re-rendering is fine. Let's use value-index for generic visual.
                                    layout
                                    initial={{ opacity: 0, x: 100, scale: 0.8 }}
                                    animate={{
                                        opacity: 1,
                                        x: 0,
                                        scale: 1,
                                        backgroundColor: '#ffffff',
                                        borderColor: '#e5e7eb'
                                    }}
                                    exit={{ opacity: 0, scale: 0.8, x: -100, backgroundColor: '#fee2e2' }}
                                    transition={{ type: "spring", stiffness: 300, damping: 25 }}
                                    className="w-16 h-16 flex flex-col items-center justify-center rounded-lg border-2 shadow-sm text-xl font-bold text-gray-700 relative bg-white"
                                >
                                    {item}
                                    <span className="absolute -bottom-6 text-[10px] text-gray-400 font-normal">
                                        {index}
                                    </span>
                                    {index === 0 && (
                                        <div className="absolute -top-3 w-2 h-2 rounded-full bg-red-500" title="Head" />
                                    )}
                                    {index === currentState.items.length - 1 && (
                                        <div className="absolute -top-3 w-2 h-2 rounded-full bg-blue-500" title="Tail" />
                                    )}
                                </motion.div>
                            ))}
                        </AnimatePresence>
                    </div>

                    {currentState.items.length === 0 && (
                        <div className="text-gray-300 text-sm pointer-events-none flex flex-col items-center gap-2">
                            <ArrowRight className="w-8 h-8 opacity-20" />
                            Empty Queue
                        </div>
                    )}
                </div>

            </div>
        </BaseVisualizer>
    );
};
