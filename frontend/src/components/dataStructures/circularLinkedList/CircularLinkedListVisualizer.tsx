import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { BaseVisualizer } from '../BaseVisualizer';
import { ArrowRight, CornerDownLeft } from 'lucide-react';

interface ListNode {
    id: string;
    value: number;
}

interface CircularLinkedListState {
    nodes: ListNode[];
    message: string;
    activeIndices: number[];
}

export const CircularLinkedListVisualizer = () => {
    const [history, setHistory] = useState<CircularLinkedListState[]>([
        { nodes: [{ id: 'init-10', value: 10 }, { id: 'init-20', value: 20 }], message: 'Initial Circular Linked List.', activeIndices: [] }
    ]);
    const [currentStep, setCurrentStep] = useState(0);
    const [inputValue, setInputValue] = useState('');
    const [indexValue, setIndexValue] = useState('0');
    const [isPlaying, setIsPlaying] = useState(false);

    const currentState = history[currentStep];

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

    const addToHistory = (newState: CircularLinkedListState) => {
        const newHistory = [...history.slice(0, currentStep + 1), newState];
        setHistory(newHistory);
        setCurrentStep(newHistory.length - 1);
    };

    const getInputs = () => {
        const val = parseInt(inputValue);
        const idx = parseInt(indexValue);
        return { val, idx };
    };

    const handleInsert = (position: 'head' | 'tail' | 'index') => {
        const { val, idx } = getInputs();
        if (isNaN(val)) return;

        if (currentState.nodes.length >= 7) {
            alert("List full! Max 7 nodes.");
            return;
        }

        const newNodes = [...currentState.nodes];
        const newNode = { id: `node-${Date.now()}`, value: val };

        if (position === 'head') {
            newNodes.unshift(newNode);
            addToHistory({
                nodes: newNodes,
                message: `Inserted ${val} at Head. Tail's next points to new Head.`,
                activeIndices: [0]
            });
        } else if (position === 'tail') {
            newNodes.push(newNode);
            addToHistory({
                nodes: newNodes,
                message: `Inserted ${val} at Tail. New Tail points to Head.`,
                activeIndices: [newNodes.length - 1]
            });
        } else {
            if (isNaN(idx) || idx < 0 || idx > currentState.nodes.length) {
                alert("Invalid index");
                return;
            }
            newNodes.splice(idx, 0, newNode);
            addToHistory({
                nodes: newNodes,
                message: `Inserted ${val} at index ${idx}.`,
                activeIndices: [idx]
            });
        }
        setInputValue('');
    };

    const handleDelete = (position: 'head' | 'tail' | 'index') => {
        if (currentState.nodes.length === 0) {
            alert("List empty!");
            return;
        }

        const newNodes = [...currentState.nodes];
        let removedVal;

        if (position === 'head') {
            removedVal = newNodes.shift()?.value;
            addToHistory({
                nodes: newNodes,
                message: `Deleted Head (${removedVal}). Tail's next updated to new Head.`,
                activeIndices: []
            });
        } else if (position === 'tail') {
            removedVal = newNodes.pop()?.value;
            addToHistory({
                nodes: newNodes,
                message: `Deleted Tail (${removedVal}). New Tail points to Head.`,
                activeIndices: []
            });
        } else {
            const { idx } = getInputs();
            if (isNaN(idx) || idx < 0 || idx >= currentState.nodes.length) {
                alert("Invalid index");
                return;
            }
            removedVal = newNodes.splice(idx, 1)[0].value;
            addToHistory({
                nodes: newNodes,
                message: `Deleted index ${idx} (${removedVal}).`,
                activeIndices: []
            });
        }
    };

    return (
        <BaseVisualizer
            title="Circular Linked List"
            description="Singly Linked List where the last node points back to the first node."
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
            <div className="flex flex-col items-center gap-8 w-full max-w-4xl">

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

                    <div className="flex flex-col gap-1">
                        <div className="flex gap-1">
                            <button onClick={() => handleInsert('head')} className="px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs hover:bg-blue-200">Add Head</button>
                            <button onClick={() => handleInsert('tail')} className="px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs hover:bg-blue-200">Add Tail</button>
                            <button onClick={() => handleInsert('index')} className="px-2 py-1 bg-blue-100 text-blue-700 rounded text-xs hover:bg-blue-200">Add Idx</button>
                        </div>
                        <div className="flex gap-1">
                            <button onClick={() => handleDelete('head')} className="px-2 py-1 bg-red-100 text-red-700 rounded text-xs hover:bg-red-200">Del Head</button>
                            <button onClick={() => handleDelete('tail')} className="px-2 py-1 bg-red-100 text-red-700 rounded text-xs hover:bg-red-200">Del Tail</button>
                            <button onClick={() => handleDelete('index')} className="px-2 py-1 bg-red-100 text-red-700 rounded text-xs hover:bg-red-200">Del Idx</button>
                        </div>
                    </div>
                </div>

                {/* Message Area */}
                <div className="min-h-[24px] text-center font-medium text-gray-600">
                    {currentState.message}
                </div>

                {/* Visualization Canvas */}
                <div className="flex items-center justify-start w-full min-h-[180px] bg-gray-50/50 rounded-lg p-8 overflow-x-auto relative">
                    <div className="flex items-center min-w-max relative pl-4">
                        <AnimatePresence mode="popLayout">
                            {currentState.nodes.map((node, index) => (
                                <div key={node.id} className="flex items-center">
                                    {/* Node */}
                                    <motion.div
                                        layout
                                        initial={{ opacity: 0, scale: 0.8, y: -20 }}
                                        animate={{
                                            opacity: 1,
                                            scale: 1,
                                            y: 0,
                                            backgroundColor: currentState.activeIndices.includes(index) ? '#dbeafe' : '#ffffff',
                                            borderColor: currentState.activeIndices.includes(index) ? '#2563eb' : '#e5e7eb'
                                        }}
                                        exit={{ opacity: 0, scale: 0.5, y: 20 }}
                                        transition={{ type: "spring", stiffness: 300, damping: 25 }}
                                        className="w-24 h-12 flex rounded border-2 shadow-sm bg-white overflow-hidden z-10"
                                    >
                                        <div className="flex-1 flex items-center justify-center font-bold text-gray-700 border-r border-gray-200">
                                            {node.value}
                                        </div>
                                        <div className="w-8 flex items-center justify-center bg-gray-50 text-gray-400 text-[10px]">
                                            •
                                        </div>
                                    </motion.div>

                                    {/* Arrow Connection */}
                                    {index < currentState.nodes.length - 1 && (
                                        <motion.div
                                            layout
                                            className="mx-2 text-gray-400"
                                        >
                                            <ArrowRight className="w-5 h-5" />
                                        </motion.div>
                                    )}
                                </div>
                            ))}
                        </AnimatePresence>

                        {/* Visual loop back to start */}
                        {currentState.nodes.length > 0 ? (
                            <motion.div
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                className="ml-2 flex items-center"
                            >
                                <div className="relative">
                                    <ArrowRight className="w-5 h-5 text-purple-400" />
                                    {/* Dotted line loop back - purely visual CSS hack for now or just an indicator */}
                                    <div className="absolute top-1/2 left-full w-4 h-0.5 bg-purple-400"></div>
                                    <div className="absolute top-1/2 left-[calc(100%+16px)] w-[1px] h-20 bg-purple-400 origin-top"></div>
                                    <CornerDownLeft className="absolute top-[80px] -left-[200%] text-purple-400 w-5 h-5" /> {/* This is static, doesn't stretch. Real loop needs SVG. */}
                                    <span className="text-[10px] text-purple-500 font-bold ml-1 absolute -top-4 w-20">To Head</span>
                                </div>
                            </motion.div>
                        ) : (
                            <div className="w-full text-center text-gray-300 pointer-events-none">Empty List</div>
                        )}

                        {/* Better loop visualization using SVG overlay */}
                        {currentState.nodes.length > 0 && (
                            <div className="absolute inset-x-0 bottom-0 top-1/2 pointer-events-none z-0">
                                {/* We can use an SVG line that goes from last node position to first. 
                             Hard to exact coordinate without refs. 
                             For simple visual, we can just show a "Loop" text or arrow at the end. */}
                            </div>
                        )}
                    </div>
                </div>

            </div>
        </BaseVisualizer>
    );
};
