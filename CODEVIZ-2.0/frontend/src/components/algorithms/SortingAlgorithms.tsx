import { useState, useEffect } from 'react';
import { BaseVisualizer } from '../dataStructures/BaseVisualizer';
import { Play, RotateCcw } from 'lucide-react';
import { motion } from 'framer-motion';

interface SortingState {
    array: number[];
    comparedIndices: number[]; // Indices currently being compared
    swappedIndices: number[]; // Indices just swapped
    sortedIndices: number[]; // Indices that are fully sorted
    message: string;
}

export const SortingAlgorithms = () => {
    const [history, setHistory] = useState<SortingState[]>([
        { array: [], comparedIndices: [], swappedIndices: [], sortedIndices: [], message: 'Start by generating a random array.' }
    ]);
    const [currentStep, setCurrentStep] = useState(0);
    const [isPlaying, setIsPlaying] = useState(false);
    const [algorithm, setAlgorithm] = useState<'bubble' | 'selection' | 'insertion'>('bubble');

    const currentState = history[currentStep];

    useEffect(() => {
        handleGenerateArray();
    }, [algorithm]);

    useEffect(() => {
        let interval: any;
        if (isPlaying && currentStep < history.length - 1) {
            interval = setInterval(() => {
                setCurrentStep(prev => prev + 1);
            }, 50); // Fast speed for algorithms
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
        const newArr = Array.from({ length: 20 }, () => Math.floor(Math.random() * 80) + 10);
        setHistory([{
            array: newArr,
            comparedIndices: [],
            swappedIndices: [],
            sortedIndices: [],
            message: `Generated random array on ${algorithm === 'insertion' ? 'Insertion' : algorithm === 'bubble' ? 'Bubble' : 'Selection'} Sort.`
        }]);
        setCurrentStep(0);
        setIsPlaying(false);
    };

    const runBubbleSort = (arr: number[]) => {
        const steps: SortingState[] = [];
        steps.push({ array: [...arr], comparedIndices: [], swappedIndices: [], sortedIndices: [], message: 'Starting Bubble Sort...' });

        for (let i = 0; i < arr.length; i++) {
            for (let j = 0; j < arr.length - i - 1; j++) {
                steps.push({
                    array: [...arr],
                    comparedIndices: [j, j + 1],
                    swappedIndices: [],
                    sortedIndices: Array.from({ length: i }, (_, k) => arr.length - 1 - k),
                    message: `Comparing ${arr[j]} and ${arr[j + 1]}`
                });

                if (arr[j] > arr[j + 1]) {
                    [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
                    steps.push({
                        array: [...arr],
                        comparedIndices: [j, j + 1],
                        swappedIndices: [j, j + 1],
                        sortedIndices: Array.from({ length: i }, (_, k) => arr.length - 1 - k),
                        message: `Swapped ${arr[j]} and ${arr[j + 1]}`
                    });
                }
            }
            steps.push({
                array: [...arr],
                comparedIndices: [],
                swappedIndices: [],
                sortedIndices: Array.from({ length: i + 1 }, (_, k) => arr.length - 1 - k),
                message: `Pass complete.`
            });
        }

        steps.push({
            array: [...arr],
            comparedIndices: [],
            swappedIndices: [],
            sortedIndices: arr.map((_, i) => i),
            message: 'Bubble Sort Complete.'
        });
        return steps;
    };

    const runSelectionSort = (arr: number[]) => {
        const steps: SortingState[] = [];
        steps.push({ array: [...arr], comparedIndices: [], swappedIndices: [], sortedIndices: [], message: 'Starting Selection Sort...' });

        for (let i = 0; i < arr.length; i++) {
            let minIdx = i;

            for (let j = i + 1; j < arr.length; j++) {
                steps.push({
                    array: [...arr],
                    comparedIndices: [minIdx, j],
                    swappedIndices: [],
                    sortedIndices: Array.from({ length: i }, (_, k) => k),
                    message: `Checking ${arr[j]} < ${arr[minIdx]}`
                });

                if (arr[j] < arr[minIdx]) {
                    minIdx = j;
                    steps.push({
                        array: [...arr],
                        comparedIndices: [minIdx],
                        swappedIndices: [],
                        sortedIndices: Array.from({ length: i }, (_, k) => k),
                        message: `New min found: ${arr[minIdx]}`
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
                    message: `Swapped min to position ${i}`
                });
            }

            steps.push({
                array: [...arr],
                comparedIndices: [],
                swappedIndices: [],
                sortedIndices: Array.from({ length: i + 1 }, (_, k) => k),
                message: `Index ${i} sorted.`
            });
        }

        steps.push({
            array: [...arr],
            comparedIndices: [],
            swappedIndices: [],
            sortedIndices: arr.map((_, i) => i),
            message: 'Selection Sort Complete.'
        });
        return steps;
    };

    const runInsertionSort = (arr: number[]) => {
        const steps: SortingState[] = [];
        steps.push({ array: [...arr], comparedIndices: [], swappedIndices: [], sortedIndices: [0], message: 'Starting Insertion Sort...' });

        for (let i = 1; i < arr.length; i++) {
            let key = arr[i];
            let j = i - 1;

            steps.push({
                array: [...arr],
                comparedIndices: [i],
                swappedIndices: [],
                sortedIndices: Array.from({ length: i }, (_, k) => k),
                message: `Selecting ${key} to insert into sorted portion.`
            });

            while (j >= 0 && arr[j] > key) {
                steps.push({
                    array: [...arr],
                    comparedIndices: [j, j + 1],
                    swappedIndices: [],
                    sortedIndices: Array.from({ length: i }, (_, k) => k),
                    message: `Comparing ${key} with ${arr[j]} (> ${key}). Shifting ${arr[j]} right.`
                });

                arr[j + 1] = arr[j];

                steps.push({
                    array: [...arr],
                    comparedIndices: [j, j + 1],
                    swappedIndices: [j + 1],
                    sortedIndices: Array.from({ length: i }, (_, k) => k),
                    message: `Shifted.`
                });

                j = j - 1;
            }
            arr[j + 1] = key;

            steps.push({
                array: [...arr],
                comparedIndices: [j + 1],
                swappedIndices: [j + 1],
                sortedIndices: Array.from({ length: i + 1 }, (_, k) => k),
                message: `Inserted ${key} at position ${j + 1}.`
            });
        }

        steps.push({
            array: [...arr],
            comparedIndices: [],
            swappedIndices: [],
            sortedIndices: arr.map((_, i) => i),
            message: 'Insertion Sort Complete.'
        });
        return steps;
    };

    const handleSort = () => {
        const arr = [...currentState.array];
        let steps: SortingState[] = [];

        if (algorithm === 'bubble') steps = runBubbleSort(arr);
        else if (algorithm === 'selection') steps = runSelectionSort(arr);
        else if (algorithm === 'insertion') steps = runInsertionSort(arr);

        addToHistory(steps);
    };

    return (
        <BaseVisualizer
            title="Sorting Algorithms"
            description="Visualize Bubble, Selection, and Insertion Sort."
            currentStep={currentStep}
            totalSteps={history.length}
            isPlaying={isPlaying}
            onPlayPause={() => setIsPlaying(!isPlaying)}
            onNext={() => setCurrentStep(Math.min(currentStep + 1, history.length - 1))}
            onPrev={() => setCurrentStep(Math.max(currentStep - 1, 0))}
            onReset={() => setCurrentStep(0)}
            speed={100} // This is just initial, BaseViz controls speed usually if wired up
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
                        <option value="insertion">Insertion Sort</option>
                    </select>

                    <button onClick={handleSort} className="flex items-center gap-1 bg-indigo-600 text-white px-3 py-1 rounded text-sm hover:bg-indigo-700 transition-colors">
                        <Play className="w-3 h-3" /> Sort
                    </button>
                </div>

                <div className="flex items-end justify-center gap-1 h-[300px] w-full bg-slate-50 border rounded-lg p-4">
                    <motion.div className="flex items-end justify-center gap-1 w-full h-full">
                        {currentState?.array.map((val, idx) => {
                            const isCompared = currentState.comparedIndices.includes(idx);
                            const isSwapped = currentState.swappedIndices.includes(idx);
                            const isSorted = currentState.sortedIndices.includes(idx);

                            return (
                                <motion.div
                                    key={idx} // Using index as key for bars in this simple viz is often cleaner for color transitions unless we physically move DOM nodes. 
                                    // For Insertion sort, we are checking values shifting. If we want perfect movement, we need unique IDs.
                                    // But for 20+ randomly generated bars, index-key with value-height animation is standardized and performant.
                                    layout
                                    transition={{ type: "spring", stiffness: 300, damping: 25 }}
                                    className="flex-1 rounded-t-sm relative group"
                                    style={{
                                        height: `${val}%`, // Percentage height for responsiveness
                                        backgroundColor: isSwapped ? '#ef4444' : isSorted ? '#10b981' : isCompared ? '#eab308' : '#6366f1',
                                        // opacity: isSorted ? 0.5 : 1 // maybe verify sorted part visually
                                    }}
                                >
                                    {/* Tooltip */}
                                    <div className="opacity-0 group-hover:opacity-100 absolute -top-8 left-1/2 -translate-x-1/2 bg-black text-white text-xs px-2 py-1 rounded pointer-events-none">
                                        {val}
                                    </div>
                                </motion.div>
                            );
                        })}
                    </motion.div>
                </div>
            </div>
        </BaseVisualizer>
    );
};
