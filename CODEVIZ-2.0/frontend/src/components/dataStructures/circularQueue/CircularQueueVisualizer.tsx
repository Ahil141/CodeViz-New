import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { BaseVisualizer } from '../BaseVisualizer';
import { Plus, Trash2 } from 'lucide-react';

const CAPACITY = 8;
const RADIUS = 120; // px
const CENTER = 150; // px

interface CircularQueueState {
    items: (number | null)[]; // Fixed size array
    front: number;
    rear: number;
    size: number;
    message: string;
}

export const CircularQueueVisualizer = () => {
    const [history, setHistory] = useState<CircularQueueState[]>([
        {
            items: Array(CAPACITY).fill(null),
            front: -1,
            rear: -1,
            size: 0,
            message: 'Circular Queue empty. Capacity: 8.'
        }
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

    const addToHistory = (newState: CircularQueueState) => {
        const newHistory = [...history.slice(0, currentStep + 1), newState];
        setHistory(newHistory);
        setCurrentStep(newHistory.length - 1);
    };

    const handleEnqueue = () => {
        if (!inputValue) return;
        const num = parseInt(inputValue);
        if (isNaN(num)) return;

        if ((currentState.rear + 1) % CAPACITY === currentState.front) {
            // Queue is full is mostly defined as size === capacity, 
            // but in circular queue implementation often we keep one slot empty strictly or use size count.
            // Here we track 'size', so full is size === CAPACITY
        }

        if (currentState.size === CAPACITY) {
            addToHistory({ ...currentState, message: 'Queue Overflow! Buffer is full.' });
            return;
        }

        const nextRear = (currentState.rear + 1) % CAPACITY;
        const nextFront = currentState.front === -1 ? 0 : currentState.front;

        const newItems = [...currentState.items];
        newItems[nextRear] = num;

        addToHistory({
            items: newItems,
            front: nextFront,
            rear: nextRear,
            size: currentState.size + 1,
            message: `Enqueued ${num} at index ${nextRear}.`
        });
        setInputValue('');
    };

    const handleDequeue = () => {
        if (currentState.size === 0) {
            addToHistory({ ...currentState, message: 'Queue Underflow! Buffer is empty.' });
            return;
        }

        const removedItem = currentState.items[currentState.front];
        const newItems = [...currentState.items];
        newItems[currentState.front] = null; // Visually remove

        if (currentState.front === currentState.rear) {
            // Last element removed
            addToHistory({
                items: newItems,
                front: -1,
                rear: -1,
                size: 0,
                message: `Dequeued ${removedItem}. Queue is now empty.`
            });
        } else {
            const nextFront = (currentState.front + 1) % CAPACITY;
            addToHistory({
                items: newItems,
                front: nextFront,
                rear: currentState.rear,
                size: currentState.size - 1,
                message: `Dequeued ${removedItem} from index ${currentState.front}. Front moves to ${nextFront}.`
            });
        }
    };

    // Helper to calculate position on circle
    const getPosition = (index: number) => {
        const angle = (index / CAPACITY) * 2 * Math.PI - Math.PI / 2; // Start from top (-90deg)
        return {
            x: CENTER + RADIUS * Math.cos(angle),
            y: CENTER + RADIUS * Math.sin(angle)
        };
    };

    return (
        <BaseVisualizer
            title="Circular Queue Visualization"
            description="Connects the end of the queue back to the start to utilize empty space efficiently."
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
                <div className="relative w-[300px] h-[300px] bg-slate-50/50 rounded-full border border-slate-100 mx-auto">
                    {/* Slots */}
                    {Array.from({ length: CAPACITY }).map((_, i) => {
                        const pos = getPosition(i);
                        const isFront = i === currentState.front;
                        const isRear = i === currentState.rear;
                        const hasItem = currentState.items[i] !== null;

                        return (
                            <div
                                key={i}
                                className="absolute w-12 h-12 -ml-6 -mt-6 flex items-center justify-center rounded-full border-2 transition-all duration-300"
                                style={{
                                    left: pos.x,
                                    top: pos.y,
                                    backgroundColor: hasItem ? 'white' : 'transparent',
                                    borderColor: hasItem ? '#3b82f6' : '#e5e7eb',
                                    borderStyle: hasItem ? 'solid' : 'dashed'
                                }}
                            >
                                <span className="text-sm font-bold text-gray-700">
                                    {currentState.items[i]}
                                </span>

                                {/* Index Label */}
                                <span className="absolute -top-5 text-[10px] text-gray-400">
                                    {i}
                                </span>

                                {/* Pointers */}
                                {isFront && currentState.size > 0 && (
                                    <motion.div
                                        layoutId="front-pointer"
                                        className="absolute -left-8 bg-red-100 text-red-700 text-[10px] font-bold px-1.5 py-0.5 rounded shadow-sm border border-red-200"
                                    >
                                        F
                                    </motion.div>
                                )}
                                {isRear && currentState.size > 0 && (
                                    <motion.div
                                        layoutId="rear-pointer"
                                        className="absolute -right-8 bg-blue-100 text-blue-700 text-[10px] font-bold px-1.5 py-0.5 rounded shadow-sm border border-blue-200"
                                    >
                                        R
                                    </motion.div>
                                )}
                            </div>
                        );
                    })}

                    {/* Center Info */}
                    <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                        <div className="text-center text-xs text-gray-400">
                            <div>Size: {currentState.size}</div>
                            <div>Capacity: {CAPACITY}</div>
                        </div>
                    </div>
                </div>

            </div>
        </BaseVisualizer>
    );
};
