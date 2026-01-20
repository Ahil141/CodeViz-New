import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { BaseVisualizer } from '../BaseVisualizer';
import { Plus, Trash2, ArrowRight, ArrowLeft } from 'lucide-react';

interface DequeState {
    items: number[];
    message: string;
}

export const DequeVisualizer = () => {
    const [history, setHistory] = useState<DequeState[]>([
        { items: [], message: 'Deque is empty. You can insert at Front or Rear.' }
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

    const addToHistory = (newState: DequeState) => {
        const newHistory = [...history.slice(0, currentStep + 1), newState];
        setHistory(newHistory);
        setCurrentStep(newHistory.length - 1);
    };

    const handleInsertFront = () => {
        if (!inputValue) return;
        const num = parseInt(inputValue);
        if (isNaN(num)) return;

        if (currentState.items.length >= 7) {
            alert("Deque full! Max 7 items for visualization.");
            return;
        }

        addToHistory({
            items: [num, ...currentState.items],
            message: `Inserted ${num} at the Front.`
        });
        setInputValue('');
    };

    const handleInsertRear = () => {
        if (!inputValue) return;
        const num = parseInt(inputValue);
        if (isNaN(num)) return;

        if (currentState.items.length >= 7) {
            alert("Deque full! Max 7 items for visualization.");
            return;
        }

        addToHistory({
            items: [...currentState.items, num],
            message: `Inserted ${num} at the Rear.`
        });
        setInputValue('');
    };

    const handleDeleteFront = () => {
        if (currentState.items.length === 0) {
            addToHistory({
                items: [],
                message: 'Underflow! Cannot delete from empty Deque.'
            });
            return;
        }

        const [removed, ...rest] = currentState.items;
        addToHistory({
            items: rest,
            message: `Deleted ${removed} from the Front.`
        });
    };

    const handleDeleteRear = () => {
        if (currentState.items.length === 0) {
            addToHistory({
                items: [],
                message: 'Underflow! Cannot delete from empty Deque.'
            });
            return;
        }

        const newItems = [...currentState.items];
        const removed = newItems.pop();
        addToHistory({
            items: newItems,
            message: `Deleted ${removed} from the Rear.`
        });
    };

    return (
        <BaseVisualizer
            title="Deque Visualization"
            description="Double-Ended Queue allows insertion and deletion from both ends."
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
                <div className="flex flex-col md:flex-row gap-4 w-full bg-white p-4 rounded-lg shadow-sm border border-gray-200 justify-center">

                    <div className="flex gap-2">
                        <input
                            type="number"
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                            placeholder="Val"
                            className="w-16 px-2 py-1 border rounded text-sm focus:outline-blue-500"
                        />
                        <div className="flex flex-col gap-1">
                            <button onClick={handleInsertFront} className="flex items-center gap-1 bg-green-100 text-green-700 px-2 py-1 rounded text-xs hover:bg-green-200 transition-colors">
                                <Plus className="w-3 h-3" /> Front
                            </button>
                            <button onClick={handleInsertRear} className="flex items-center gap-1 bg-blue-100 text-blue-700 px-2 py-1 rounded text-xs hover:bg-blue-200 transition-colors">
                                <Plus className="w-3 h-3" /> Rear
                            </button>
                        </div>
                    </div>

                    <div className="w-px bg-gray-200 mx-2 hidden md:block"></div>

                    <div className="flex flex-col gap-1">
                        <button onClick={handleDeleteFront} className="flex items-center gap-1 bg-red-100 text-red-700 px-2 py-1 rounded text-xs hover:bg-red-200 transition-colors">
                            <Trash2 className="w-3 h-3" /> Front
                        </button>
                        <button onClick={handleDeleteRear} className="flex items-center gap-1 bg-orange-100 text-orange-700 px-2 py-1 rounded text-xs hover:bg-orange-200 transition-colors">
                            <Trash2 className="w-3 h-3" /> Rear
                        </button>
                    </div>
                </div>

                {/* Message Area */}
                <div className="min-h-[24px] text-center font-medium text-gray-600">
                    {currentState.message}
                </div>

                {/* Visualization Canvas */}
                <div className="flex items-center justify-center w-full min-h-[120px] bg-gray-50/50 rounded-lg p-8 relative overflow-hidden">

                    {/* Labels */}
                    {currentState.items.length > 0 && (
                        <>
                            <div className="absolute left-8 top-1/2 -translate-y-1/2 text-xs font-bold text-green-600 -rotate-90 origin-center flex items-center gap-1">
                                <ArrowLeft className="w-3 h-3 rotate-90" /> FRONT
                            </div>
                            <div className="absolute right-8 top-1/2 -translate-y-1/2 text-xs font-bold text-blue-600 -rotate-90 origin-center flex items-center gap-1">
                                REAR <ArrowRight className="w-3 h-3 rotate-90" />
                            </div>
                        </>
                    )}

                    <div className="flex items-center gap-2 border-t-2 border-b-2 border-dashed border-gray-300 px-8 py-4 min-w-[200px] justify-center">
                        <AnimatePresence mode="popLayout">
                            {currentState.items.map((item, index) => (
                                <motion.div
                                    key={`${item}-${index}-${currentState.items.length}`} // Ensure uniqueness for animations
                                    layout
                                    initial={{ opacity: 0, scale: 0.8, y: -20 }}
                                    animate={{
                                        opacity: 1,
                                        scale: 1,
                                        y: 0,
                                        backgroundColor: '#ffffff',
                                        borderColor: '#e5e7eb'
                                    }}
                                    exit={{ opacity: 0, scale: 0.8, y: 20, backgroundColor: '#fee2e2' }}
                                    transition={{ type: "spring", stiffness: 300, damping: 25 }}
                                    className="w-12 h-12 flex items-center justify-center rounded-md border-2 shadow-sm text-lg font-bold text-gray-700 relative bg-white min-w-[3rem]"
                                >
                                    {item}
                                </motion.div>
                            ))}
                        </AnimatePresence>

                        {currentState.items.length === 0 && (
                            <div className="text-gray-300 text-sm pointer-events-none absolute inset-0 flex items-center justify-center">
                                Empty Deque
                            </div>
                        )}
                    </div>
                </div>

            </div>
        </BaseVisualizer>
    );
};
