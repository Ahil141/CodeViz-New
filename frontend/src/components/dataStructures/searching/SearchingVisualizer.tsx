import { useState, useEffect, useCallback } from 'react';
import { BaseVisualizer } from '../BaseVisualizer';
import { RotateCcw, Search } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface SearchState {
    array: number[];
    activeIndices: number[]; // Indices currently being checked
    foundIndex: number | null; // index where value was found
    low: number | null; // For Binary Search
    high: number | null; // For Binary Search
    mid: number | null; // For Binary Search
    message: string;
}

export const SearchingVisualizer = () => {
    const [history, setHistory] = useState<SearchState[]>([
        { array: [], activeIndices: [], foundIndex: null, low: null, high: null, mid: null, message: 'Start by generating an array.' }
    ]);
    const [currentStep, setCurrentStep] = useState(0);
    const [isPlaying, setIsPlaying] = useState(false);
    const [algorithm, setAlgorithm] = useState<'linear' | 'binary'>('linear');
    const [targetValue, setTargetValue] = useState('');

    const currentState = history[currentStep];

    const handleGenerateArray = useCallback(() => {
        const newArr = Array.from({ length: 15 }, () => Math.floor(Math.random() * 99) + 1);
        if (algorithm === 'binary') {
            newArr.sort((a, b) => a - b);
        }
        setHistory([{
            array: newArr,
            activeIndices: [],
            foundIndex: null,
            low: null,
            high: null,
            mid: null,
            message: `Generated ${algorithm === 'binary' ? 'sorted' : 'random'} array.`
        }]);
        setCurrentStep(0);
        setIsPlaying(false);
    }, [algorithm]);

    const addToHistory = (steps: SearchState[]) => {
        setHistory(steps);
        setCurrentStep(0);
        setIsPlaying(true);
    };

    useEffect(() => {
        // eslint-disable-next-line react-hooks/set-state-in-effect
        handleGenerateArray();
    }, [handleGenerateArray]);

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
        }, 800);

        return () => clearInterval(interval);
    }, [isPlaying, history.length]);

    const runLinearSearch = () => {
        const target = parseInt(targetValue);
        if (isNaN(target)) return;

        const arr = currentState.array;
        const steps: SearchState[] = [];
        let found = false;

        steps.push({
            array: arr,
            activeIndices: [],
            foundIndex: null,
            low: null, high: null, mid: null,
            message: `Starting Linear Search for ${target}...`
        });

        for (let i = 0; i < arr.length; i++) {
            steps.push({
                array: arr,
                activeIndices: [i],
                foundIndex: null,
                low: null, high: null, mid: null,
                message: `Checking index ${i} (Value: ${arr[i]})...`
            });

            if (arr[i] === target) {
                found = true;
                steps.push({
                    array: arr,
                    activeIndices: [i],
                    foundIndex: i,
                    low: null, high: null, mid: null,
                    message: `Found ${target} at index ${i}!`
                });
                break;
            }
        }

        if (!found) {
            steps.push({
                array: arr,
                activeIndices: [],
                foundIndex: null,
                low: null, high: null, mid: null,
                message: `${target} not found in the array.`
            });
        }

        addToHistory(steps);
    };

    const runBinarySearch = () => {
        const target = parseInt(targetValue);
        if (isNaN(target)) return;

        const arr = currentState.array;
        const steps: SearchState[] = [];
        let low = 0;
        let high = arr.length - 1;
        let found = false;

        steps.push({
            array: arr,
            activeIndices: [],
            foundIndex: null,
            low: low, high: high, mid: null,
            message: `Starting Binary Search for ${target}...`
        });

        while (low <= high) {
            const mid = Math.floor((low + high) / 2);

            steps.push({
                array: arr,
                activeIndices: [mid],
                foundIndex: null,
                low: low, high: high, mid: mid,
                message: `Checking Middle Index ${mid} (Value: ${arr[mid]})...`
            });

            if (arr[mid] === target) {
                found = true;
                steps.push({
                    array: arr,
                    activeIndices: [mid],
                    foundIndex: mid,
                    low: low, high: high, mid: mid,
                    message: `Found ${target} at index ${mid}!`
                });
                break;
            } else if (arr[mid] < target) {
                steps.push({
                    array: arr,
                    activeIndices: [mid],
                    foundIndex: null,
                    low: low, high: high, mid: mid,
                    message: `${arr[mid]} < ${target}. Ignoring left half.`
                });
                low = mid + 1;
            } else {
                steps.push({
                    array: arr,
                    activeIndices: [mid],
                    foundIndex: null,
                    low: low, high: high, mid: mid,
                    message: `${arr[mid]} > ${target}. Ignoring right half.`
                });
                high = mid - 1;
            }

            // Show new range
            if (low <= high) {
                steps.push({
                    array: arr,
                    activeIndices: [],
                    foundIndex: null,
                    low: low, high: high, mid: null,
                    message: `New Range: [${low}, ${high}]`
                });
            }
        }

        if (!found) {
            steps.push({
                array: arr,
                activeIndices: [],
                foundIndex: null,
                low: null, high: null, mid: null,
                message: `${target} not found.`
            });
        }

        addToHistory(steps);
    };

    const handleSearch = () => {
        if (algorithm === 'linear') runLinearSearch();
        else runBinarySearch();
    };

    return (
        <BaseVisualizer
            title="Searching Algorithms"
            description="Linear Search vs Binary Search."
            currentStep={currentStep}
            totalSteps={history.length}
            isPlaying={isPlaying}
            onPlayPause={() => setIsPlaying(!isPlaying)}
            onNext={() => setCurrentStep(Math.min(currentStep + 1, history.length - 1))}
            onPrev={() => setCurrentStep(Math.max(currentStep - 1, 0))}
            onReset={() => setCurrentStep(0)}
            speed={800}
            onSpeedChange={() => { }}
        >
            <div className="flex flex-col items-center gap-6 w-full max-w-4xl">
                <div className="flex items-center gap-2 bg-white p-4 rounded-lg shadow-sm border border-gray-200">
                    <button onClick={handleGenerateArray} className="flex items-center gap-1 bg-gray-100 text-gray-700 px-3 py-1 rounded text-sm hover:bg-gray-200 transition-colors">
                        <RotateCcw className="w-3 h-3" /> Reset
                    </button>

                    <div className="w-px h-8 bg-gray-200 mx-2"></div>

                    <select
                        value={algorithm}
                        onChange={(e) => {
                            const newAlgo = e.target.value as 'linear' | 'binary';
                            setAlgorithm(newAlgo);
                            // Generate new array immediately
                            const newArr = Array.from({ length: 15 }, () => Math.floor(Math.random() * 99) + 1);
                            if (newAlgo === 'binary') {
                                newArr.sort((a, b) => a - b);
                            }
                            setHistory([{
                                array: newArr,
                                activeIndices: [],
                                foundIndex: null,
                                low: null,
                                high: null,
                                mid: null,
                                message: `Generated ${newAlgo === 'binary' ? 'sorted' : 'random'} array.`
                            }]);
                            setCurrentStep(0);
                            setIsPlaying(false);
                        }}
                        className="px-2 py-1 border rounded text-sm"
                    >
                        <option value="linear">Linear Search</option>
                        <option value="binary">Binary Search (Sorted)</option>
                    </select>

                    <input
                        type="number"
                        value={targetValue}
                        onChange={(e) => setTargetValue(e.target.value)}
                        placeholder="Target"
                        className="w-20 px-2 py-1 border rounded text-sm"
                    />

                    <button onClick={handleSearch} className="flex items-center gap-1 bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700 transition-colors">
                        <Search className="w-3 h-3" /> Find
                    </button>
                </div>

                <div className="flex items-center justify-center gap-2 flex-wrap w-full bg-gray-50 border rounded-lg p-8 min-h-[200px]">
                    <AnimatePresence>
                        {currentState?.array.map((val, idx) => {
                            const isActive = currentState.activeIndices.includes(idx);
                            const isFound = currentState.foundIndex === idx;

                            // Binary search specific styles
                            let isRange = false;
                            if (algorithm === 'binary' && currentState.low !== null && currentState.high !== null) {
                                if (idx >= currentState.low && idx <= currentState.high) {
                                    isRange = true;
                                }
                            }
                            const isMid = currentState.mid === idx;

                            return (
                                <motion.div
                                    key={idx}
                                    layout
                                    initial={{ scale: 0.8, opacity: 0 }}
                                    animate={{
                                        scale: isFound ? 1.1 : 1,
                                        opacity: algorithm === 'binary' && !isRange && currentState.low !== null ? 0.3 : 1, // Dim items out of range
                                        backgroundColor: isFound ? '#22c55e' : isMid ? '#eab308' : isActive ? '#3b82f6' : '#ffffff',
                                        borderColor: isFound ? '#16a34a' : isMid ? '#ca8a04' : isActive ? '#2563eb' : '#cbd5e1',
                                        color: (isActive || isFound || isMid) ? '#ffffff' : '#1e293b'
                                    }}
                                    className="w-10 h-10 flex items-center justify-center rounded border-2 font-bold shadow-sm relative"
                                >
                                    {val}
                                    <div className="absolute -bottom-5 text-[10px] text-gray-400">
                                        {idx}
                                    </div>
                                    {isMid && algorithm === 'binary' && <div className="absolute -top-6 text-[10px] text-yellow-600 font-bold">MID</div>}
                                    {idx === currentState.low && algorithm === 'binary' && <div className="absolute -top-6 text-[10px] text-blue-600 font-bold">L</div>}
                                    {idx === currentState.high && algorithm === 'binary' && <div className="absolute -top-6 text-[10px] text-blue-600 font-bold">H</div>}
                                </motion.div>
                            );
                        })}
                    </AnimatePresence>
                </div>
            </div>
        </BaseVisualizer>
    );
};
