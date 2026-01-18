import { useState, useEffect } from 'react';
import { BaseVisualizer } from '../BaseVisualizer';
import { Plus, Trash2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface HeapNode {
    id: string;
    value: number;
    x: number;
    y: number;
}

interface HeapState {
    array: number[];
    activeIndices: number[];
    shiningIndices: number[]; // For highlighting swap targets
    message: string;
}

export const HeapVisualizer = () => {
    const [history, setHistory] = useState<HeapState[]>([
        { array: [], activeIndices: [], shiningIndices: [], message: 'Heap is empty. Insert a value to start.' }
    ]);
    const [currentStep, setCurrentStep] = useState(0);
    const [inputValue, setInputValue] = useState('');
    const [isPlaying, setIsPlaying] = useState(false);

    const currentState = history[currentStep];

    const generateNodes = (arr: number[]): HeapNode[] => {
        const nodes: HeapNode[] = [];
        if (arr.length === 0) return nodes;

        const startX = 400;
        const startY = 50;

        // Using a map to store positions for parent lookup
        const positions = new Map<number, { x: number, y: number }>();
        const levelOffset = 60;

        arr.forEach((val, i) => {
            if (i === 0) {
                positions.set(i, { x: startX, y: startY });
                nodes.push({ id: `node-${i}-${val}`, value: val, x: startX, y: startY });
            } else {
                const parentIdx = Math.floor((i - 1) / 2);
                const parentPos = positions.get(parentIdx);
                if (parentPos) {
                    const level = Math.floor(Math.log2(i + 1));
                    // Check max depth 4 to avoid clutter
                    // Offset needs to depend on level to avoid overlap
                    // Root level 0. Level 1 offset 100. Level 2 offset 50.
                    // General formula: 200 / 2^level?
                    // Actually, total width is fixed. 
                    // Let's try: 200 / (1.8 ^ (level - 1))

                    const offset = 200 / Math.pow(2, level - 1);

                    const isLeft = (i % 2) !== 0;
                    const x = isLeft ? parentPos.x - offset : parentPos.x + offset;
                    const y = parentPos.y + levelOffset;

                    positions.set(i, { x, y });
                    nodes.push({ id: `node-${i}-${val}`, value: val, x, y });
                }
            }
        });

        return nodes;
    };

    const renderNodes = generateNodes(currentState.array);

    useEffect(() => {
        let interval: any;
        if (isPlaying && currentStep < history.length - 1) {
            interval = setInterval(() => {
                setCurrentStep(prev => prev + 1);
            }, 800);
        } else if (currentStep >= history.length - 1) {
            setIsPlaying(false);
        }
        return () => clearInterval(interval);
    }, [isPlaying, currentStep, history.length]);

    const addToHistory = (steps: HeapState[]) => {
        const base = history.slice(0, currentStep + 1);
        setHistory([...base, ...steps]);
        setCurrentStep(base.length);
        setIsPlaying(true);
    };

    const handleInsert = () => {
        const val = parseInt(inputValue);
        if (isNaN(val)) return;
        if (currentState.array.length >= 15) { // Limit size
            alert("Heap full (max 15 nodes for visualizer)");
            return;
        }

        const newArr = [...currentState.array, val];
        const steps: HeapState[] = [];

        // Step 1: Add to end
        steps.push({
            array: [...newArr],
            activeIndices: [newArr.length - 1],
            shiningIndices: [],
            message: `Inserted ${val} at the end.`
        });

        // Step 2: Heapify Up
        let curr = newArr.length - 1;
        while (curr > 0) {
            const parent = Math.floor((curr - 1) / 2);

            steps.push({
                array: [...newArr],
                activeIndices: [curr],
                shiningIndices: [parent],
                message: `Comparing ${newArr[curr]} with parent ${newArr[parent]}...`
            });

            if (newArr[curr] > newArr[parent]) {
                // Swap
                [newArr[curr], newArr[parent]] = [newArr[parent], newArr[curr]];
                steps.push({
                    array: [...newArr],
                    activeIndices: [parent],
                    shiningIndices: [],
                    message: `Swapped: ${newArr[parent]} > ${newArr[curr]}. Moving up.`
                });
                curr = parent;
            } else {
                steps.push({
                    array: [...newArr],
                    activeIndices: [curr],
                    shiningIndices: [],
                    message: `Heap property satisfied (${newArr[curr]} <= ${newArr[parent]}).`
                });
                break;
            }
        }

        steps.push({
            array: [...newArr],
            activeIndices: [],
            shiningIndices: [],
            message: `Insert complete.`
        });

        addToHistory(steps);
        setInputValue('');
    };

    const handleDelete = () => { // Extract Max
        if (currentState.array.length === 0) return;

        const newArr = [...currentState.array];
        const steps: HeapState[] = [];
        const maxVal = newArr[0];

        // Step 1: Highlight root
        steps.push({
            array: [...newArr],
            activeIndices: [0],
            shiningIndices: [],
            message: `Extracting max value: ${maxVal}`
        });

        const lastVal = newArr.pop()!; // Remove last

        if (newArr.length > 0) {
            // Move last to root
            newArr[0] = lastVal;
            steps.push({
                array: [...newArr],
                activeIndices: [0],
                shiningIndices: [],
                message: `Moved last element (${lastVal}) to root.`
            });

            // Heapify Down
            let curr = 0;
            while (true) {
                const left = 2 * curr + 1;
                const right = 2 * curr + 2;
                let largest = curr;

                if (left < newArr.length && newArr[left] > newArr[largest]) {
                    largest = left;
                }
                if (right < newArr.length && newArr[right] > newArr[largest]) {
                    largest = right;
                }

                if (largest !== curr) {
                    steps.push({
                        array: [...newArr],
                        activeIndices: [curr],
                        shiningIndices: [largest],
                        message: `Comparing with children... ${newArr[largest]} is larger.`
                    });

                    // Swap
                    [newArr[curr], newArr[largest]] = [newArr[largest], newArr[curr]];

                    steps.push({
                        array: [...newArr],
                        activeIndices: [largest],
                        shiningIndices: [],
                        message: `Swapped with ${newArr[largest]}. Moving down.`
                    });

                    curr = largest;
                } else {
                    steps.push({
                        array: [...newArr],
                        activeIndices: [curr],
                        shiningIndices: [],
                        message: `Heap property satisfied.`
                    });
                    break;
                }
            }
        } else {
            steps.push({
                array: [],
                activeIndices: [],
                shiningIndices: [],
                message: `Heap is now empty.`
            });
        }

        steps.push({
            array: [...newArr],
            activeIndices: [],
            shiningIndices: [],
            message: `Extract Max Complete.`
        });

        addToHistory(steps);
    };

    return (
        <BaseVisualizer
            title="Max Heap"
            description="Complete Binary Tree where Parent >= Children. Root is Max."
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
            <div className="flex flex-col items-center gap-8 w-full max-w-4xl">
                <div className="flex items-center gap-2 bg-white p-4 rounded-lg shadow-sm border border-gray-200">
                    <input
                        type="number"
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                        placeholder="Val"
                        className="w-20 px-2 py-1 border rounded text-sm focus:outline-blue-500"
                        onKeyDown={(e) => e.key === 'Enter' && handleInsert()}
                    />
                    <button onClick={handleInsert} className="flex items-center gap-1 bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700 transition-colors">
                        <Plus className="w-3 h-3" /> Insert
                    </button>
                    <button onClick={handleDelete} className="flex items-center gap-1 bg-red-600 text-white px-3 py-1 rounded text-sm hover:bg-red-700 transition-colors">
                        <Trash2 className="w-3 h-3" /> Extract Max
                    </button>
                </div>

                <div className="relative w-full h-[400px] border rounded-lg bg-gray-50 overflow-hidden flex justify-center pt-8">
                    <AnimatePresence>
                        {/* Edges */}
                        {renderNodes.map(node => {
                            // Find parent to draw edge
                            const nodeIdx = parseInt(node.id.split('-')[1]);
                            if (nodeIdx === 0) return null;
                            const parentIdx = Math.floor((nodeIdx - 1) / 2);
                            const parent = renderNodes.find(n => parseInt(n.id.split('-')[1]) === parentIdx);
                            if (!parent) return null;

                            return (
                                <motion.svg key={`edge-${node.id}`} className="absolute top-0 left-0 w-full h-full pointer-events-none" style={{ zIndex: 0 }}>
                                    <line
                                        x1={parent.x}
                                        y1={parent.y}
                                        x2={node.x}
                                        y2={node.y}
                                        stroke="#cbd5e1"
                                        strokeWidth="2"
                                    />
                                </motion.svg>
                            );
                        })}

                        {/* Nodes */}
                        {renderNodes.map((node) => {
                            // find real index from id
                            const realIndex = parseInt(node.id.split('-')[1]);
                            const isActive = currentState.activeIndices.includes(realIndex);
                            const isShining = currentState.shiningIndices.includes(realIndex);

                            return (
                                <motion.div
                                    key={node.id} // Stable key
                                    initial={{ scale: 0, opacity: 0 }}
                                    animate={{
                                        scale: 1,
                                        opacity: 1,
                                        x: node.x - 20, // Center the 40px div
                                        y: node.y - 20,
                                        backgroundColor: isActive ? '#3b82f6' : isShining ? '#fbbf24' : '#ffffff',
                                        color: isActive ? '#ffffff' : '#1e293b',
                                        borderColor: isActive ? '#2563eb' : isShining ? '#d97706' : '#94a3b8'
                                    }}
                                    exit={{ scale: 0, opacity: 0 }}
                                    transition={{ duration: 0.5 }}
                                    className="absolute flex items-center justify-center w-10 h-10 rounded-full border-2 shadow-sm font-bold z-10"
                                >
                                    {node.value}
                                </motion.div>
                            );
                        })}
                    </AnimatePresence>
                </div>

                {/* Array view */}
                <div className="flex gap-1 flex-wrap justify-center p-4 bg-gray-50 rounded w-full">
                    {currentState.array.map((val, idx) => (
                        <div key={idx} className={`border p-2 min-w-[30px] text-center ${currentState.activeIndices.includes(idx) ? 'bg-blue-200' : 'bg-white'}`}>
                            <div className="text-xs text-gray-500 mb-1">{idx}</div>
                            <div className="font-semibold">{val}</div>
                        </div>
                    ))}
                </div>
            </div>
        </BaseVisualizer>
    );
};
