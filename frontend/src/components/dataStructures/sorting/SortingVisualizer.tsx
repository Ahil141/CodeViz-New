import { useState, useEffect } from 'react';
import { BaseVisualizer } from '../BaseVisualizer';
import { Play, RotateCcw } from 'lucide-react';
import { motion } from 'framer-motion';

interface SortingState {
    array: number[];
    comparedIndices: number[]; // Indices currently being compared
    swappedIndices: number[]; // Indices just swapped
    sortedIndices: number[]; // Indices that are fully sorted
    message: string;
}

export const SortingVisualizer = () => {
    const [history, setHistory] = useState<SortingState[]>([
        { array: [], comparedIndices: [], swappedIndices: [], sortedIndices: [], message: 'Start by generating a random array.' }
    ]);
    const [currentStep, setCurrentStep] = useState(0);
    const [isPlaying, setIsPlaying] = useState(false);
    const [algorithm, setAlgorithm] = useState<'bubble' | 'selection'>('bubble');

    const currentState = history[currentStep];

    useEffect(() => {
        // Initial random array
        handleGenerateArray();
    }, []);

    useEffect(() => {
        let interval: any;
        if (isPlaying && currentStep < history.length - 1) {
            interval = setInterval(() => {
                setCurrentStep(prev => prev + 1);
            }, 100); // 100ms for faster sorting viz
        } else if (currentStep >= history.length - 1) {
            setIsPlaying(false);
        }
        return () => clearInterval(interval);
    }, [isPlaying, currentStep, history.length]);

    const addToHistory = (steps: SortingState[]) => {
        setHistory(steps);
        setCurrentStep(0);
        setIsPlaying(true);
    };

    const handleGenerateArray = () => {
        const newArr = Array.from({ length: 15 }, () => Math.floor(Math.random() * 80) + 10);
        setHistory([{
            array: newArr,
            comparedIndices: [],
            swappedIndices: [],
            sortedIndices: [],
            message: 'Generated new random array.'
        }]);
        setCurrentStep(0);
        setIsPlaying(false);
    };

    const runBubbleSort = () => {
        const arr = [...currentState.array];
        const steps: SortingState[] = [];

        // Initial state
        steps.push({
            array: [...arr],
            comparedIndices: [],
            swappedIndices: [],
            sortedIndices: [],
            message: 'Starting Bubble Sort...'
        });

        for (let i = 0; i < arr.length; i++) {
            for (let j = 0; j < arr.length - i - 1; j++) {
                // Compare
                steps.push({
                    array: [...arr],
                    comparedIndices: [j, j + 1],
                    swappedIndices: [],
                    sortedIndices: [...(steps[steps.length - 1]?.sortedIndices || [])],
                    message: `Comparing ${arr[j]} and ${arr[j + 1]}`
                });

                if (arr[j] > arr[j + 1]) {
                    // Swap
                    [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
                    steps.push({
                        array: [...arr],
                        comparedIndices: [j, j + 1],
                        swappedIndices: [j, j + 1],
                        sortedIndices: [...(steps[steps.length - 1]?.sortedIndices || [])],
                        message: `Swapped ${arr[j]} and ${arr[j + 1]}`
                    });
                }
            }
            // Mark last element as sorted
            const sorted = [];
            for (let k = 0; k <= i; k++) {
                sorted.push(arr.length - 1 - k);
            }
            steps.push({
                array: [...arr],
                comparedIndices: [],
                swappedIndices: [],
                sortedIndices: sorted,
                message: `${arr[arr.length - 1 - i]} is now in sorted position.`
            });
        }

        steps.push({
            array: [...arr],
            comparedIndices: [],
            swappedIndices: [],
            sortedIndices: arr.map((_, i) => i),
            message: 'Bubble Sort Complete.'
        });

        addToHistory(steps);
    };

    const runSelectionSort = () => {
        const arr = [...currentState.array];
        const steps: SortingState[] = [];

        steps.push({
            array: [...arr],
            comparedIndices: [],
            swappedIndices: [],
            sortedIndices: [],
            message: 'Starting Selection Sort...'
        });

        for (let i = 0; i < arr.length; i++) {
            let minIdx = i;

            for (let j = i + 1; j < arr.length; j++) {
                steps.push({
                    array: [...arr],
                    comparedIndices: [minIdx, j],
                    swappedIndices: [],
                    sortedIndices: Array.from({ length: i }, (_, k) => k),
                    message: `Checking if ${arr[j]} < current min ${arr[minIdx]}`
                });

                if (arr[j] < arr[minIdx]) {
                    minIdx = j;
                    steps.push({
                        array: [...arr],
                        comparedIndices: [minIdx],
                        swappedIndices: [],
                        sortedIndices: Array.from({ length: i }, (_, k) => k),
                        message: `Found new minimum: ${arr[minIdx]}`
                    });
                }
            }

            if (minIdx !== i) {
                [arr[i], arr[minIdx]] = [arr[minIdx], arr[i]];
                steps.push({
                    array: [...arr],
                    comparedIndices: [i, minIdx],
                    swappedIndices: [i, minIdx],
                    sortedIndices: Array.from({ length: i }, (_, k) => k),
                    message: `Swapped minimum ${arr[i]} into position ${i}`
                });
            }

            steps.push({
                array: [...arr],
                comparedIndices: [],
                swappedIndices: [],
                sortedIndices: Array.from({ length: i + 1 }, (_, k) => k),
                message: `Index ${i} is now sorted.`
            });
        }

        steps.push({
            array: [...arr],
            comparedIndices: [],
            swappedIndices: [],
            sortedIndices: arr.map((_, i) => i),
            message: 'Selection Sort Complete.'
        });

        addToHistory(steps);
    };

    const handleSort = () => {
        if (algorithm === 'bubble') runBubbleSort();
        else runSelectionSort();
    };

    return (
        <BaseVisualizer
            title="Sorting Algorithms"
            description="Comparing Bubble Sort and Selection Sort."
            currentStep={currentStep}
            totalSteps={history.length}
            isPlaying={isPlaying}
            onPlayPause={() => setIsPlaying(!isPlaying)}
            onNext={() => setCurrentStep(Math.min(currentStep + 1, history.length - 1))}
            onPrev={() => setCurrentStep(Math.max(currentStep - 1, 0))}
            onReset={() => setCurrentStep(0)}
            speed={100}
            onSpeedChange={() => { }}
        >
            <div className="flex flex-col items-center gap-6 w-full max-w-4xl">
                <div className="flex items-center gap-2 bg-white p-4 rounded-lg shadow-sm border border-gray-200">
                    <button onClick={handleGenerateArray} className="flex items-center gap-1 bg-gray-100 text-gray-700 px-3 py-1 rounded text-sm hover:bg-gray-200 transition-colors">
                        <RotateCcw className="w-3 h-3" /> Randomize
                    </button>

                    <div className="w-px h-8 bg-gray-200 mx-2"></div>

                    <select
                        value={algorithm}
                        onChange={(e) => setAlgorithm(e.target.value as any)}
                        className="px-2 py-1 border rounded text-sm"
                    >
                        <option value="bubble">Bubble Sort</option>
                        <option value="selection">Selection Sort</option>
                    </select>

                    <button onClick={handleSort} className="flex items-center gap-1 bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700 transition-colors">
                        <Play className="w-3 h-3" /> Sort
                    </button>
                </div>

                <div className="flex items-end justify-center gap-2 h-[300px] w-full bg-gray-50 border rounded-lg p-8">
                    {currentState?.array.map((val, idx) => {
                        const isCompared = currentState.comparedIndices.includes(idx);
                        const isSwapped = currentState.swappedIndices.includes(idx);
                        const isSorted = currentState.sortedIndices.includes(idx);

                        return (
                            <motion.div
                                key={idx} // Index key is fine here as we aren't adding/removing, just swapping values
                                layout
                                transition={{ type: "spring", stiffness: 300, damping: 20 }}
                                className="w-8 rounded-t-md relative group"
                                style={{
                                    height: `${val * 3}px`,
                                    backgroundColor: isSwapped ? '#ef4444' : isSorted ? '#22c55e' : isCompared ? '#eab308' : '#3b82f6'
                                }}
                            >
                                <span className="absolute -top-6 left-1/2 -translate-x-1/2 text-xs text-gray-500 opacity-0 group-hover:opacity-100 transition-opacity">
                                    {val}
                                </span>
                            </motion.div>
                        );
                    })}
                </div>
            </div>
        </BaseVisualizer>
    );
};
