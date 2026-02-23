import { useState, useEffect } from 'react';
import { BaseVisualizer } from '../BaseVisualizer';
import { Plus, Play, Share2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface GraphNode {
    id: string; // Label
    x: number;
    y: number;
}

interface GraphEdge {
    source: string;
    target: string;
}

interface GraphState {
    nodes: GraphNode[];
    edges: GraphEdge[];
    adjList: Record<string, string[]>;
    activeNodes: string[];
    visitedNodes: string[];
    queueStack: string[]; // For BFS Queue or DFS Stack visualization
    message: string;
}

export const GraphVisualizer = () => {
    const [history, setHistory] = useState<GraphState[]>([
        { nodes: [], edges: [], adjList: {}, activeNodes: [], visitedNodes: [], queueStack: [], message: 'Graph is empty. Add vertices to start.' }
    ]);
    const [currentStep, setCurrentStep] = useState(0);
    const [isPlaying, setIsPlaying] = useState(false);

    // Inputs
    const [vertexLabel, setVertexLabel] = useState('');
    const [edgeSource, setEdgeSource] = useState('');
    const [edgeTarget, setEdgeTarget] = useState('');
    const [startNode, setStartNode] = useState('');

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

    const addToHistory = (steps: GraphState[]) => {
        const base = history.slice(0, currentStep + 1);
        setHistory([...base, ...steps]);
        setCurrentStep(base.length);
        setIsPlaying(true);
    };

    const handleAddVertex = () => {
        const label = vertexLabel.trim();
        if (!label) return;
        if (currentState.nodes.some(n => n.id === label)) {
            alert("Vertex already exists!");
            return;
        }

        // Random position within 600x400 canvas, with some padding
        const x = 50 + Math.random() * 500;
        const y = 50 + Math.random() * 300;

        const newNode: GraphNode = { id: label, x, y };

        const newState: GraphState = {
            ...currentState,
            nodes: [...currentState.nodes, newNode],
            adjList: { ...currentState.adjList, [label]: [] },
            message: `Added vertex ${label}`
        };

        addToHistory([newState]);
        setVertexLabel('');
    };

    const handleAddEdge = () => {
        const u = edgeSource.trim();
        const v = edgeTarget.trim();

        if (!u || !v) return;
        if (!currentState.nodes.some(n => n.id === u) || !currentState.nodes.some(n => n.id === v)) {
            alert("Both vertices must exist.");
            return;
        }
        if (currentState.edges.some(e => (e.source === u && e.target === v) || (e.source === v && e.target === u))) {
            alert("Edge already exists.");
            return;
        }

        const newEdge: GraphEdge = { source: u, target: v };

        // Undirected graph logic
        const newAdjList = { ...currentState.adjList };
        newAdjList[u] = [...(newAdjList[u] || []), v];
        newAdjList[v] = [...(newAdjList[v] || []), u];

        const newState: GraphState = {
            ...currentState,
            edges: [...currentState.edges, newEdge],
            adjList: newAdjList,
            message: `Added edge ${u} - ${v}`
        };

        addToHistory([newState]);
        setEdgeSource('');
        setEdgeTarget('');
    };

    const handleBFS = () => {
        const start = startNode.trim();
        if (!start || !currentState.nodes.some(n => n.id === start)) return;

        const steps: GraphState[] = [];
        const visited = new Set<string>();
        const queue: string[] = [start];
        visited.add(start);

        // Initial Step
        steps.push({
            ...currentState,
            activeNodes: [start],
            visitedNodes: [...Array.from(visited)],
            queueStack: [...queue],
            message: `BFS Start: Initialized queue with ${start}`
        });

        let head = 0; // Simulate queue dequeue index
        while (head < queue.length) {
            const curr = queue[head];
            head++; // Dequeue

            steps.push({
                ...currentState,
                activeNodes: [curr],
                visitedNodes: [...Array.from(visited)],
                queueStack: queue.slice(head),
                message: `Dequeued ${curr}. Processing neighbors...`
            });

            const neighbors = currentState.adjList[curr] || [];
            for (const neighbor of neighbors) {
                if (!visited.has(neighbor)) {
                    visited.add(neighbor);
                    queue.push(neighbor);

                    steps.push({
                        ...currentState,
                        activeNodes: [curr, neighbor], // Highlight current and neighbor
                        visitedNodes: [...Array.from(visited)],
                        queueStack: queue.slice(head),
                        message: `Visited neighbor ${neighbor}, added to queue.`
                    });
                }
            }
        }

        steps.push({
            ...currentState,
            activeNodes: [],
            visitedNodes: [...Array.from(visited)],
            queueStack: [],
            message: `BFS Complete.`
        });

        addToHistory(steps);
    };

    const handleDFS = () => {
        const start = startNode.trim();
        if (!start || !currentState.nodes.some(n => n.id === start)) return;

        const steps: GraphState[] = [];
        const visited = new Set<string>();
        const stack: string[] = [start];
        // We'll use an iterative DFS for easier state capturing, or recursive with explicit step pushing.
        // Recursive is standard for DFS but iterative is easier to visualize stack. 
        // Let's use iterative to visualize the "Stack".

        steps.push({
            ...currentState,
            activeNodes: [],
            visitedNodes: [],
            queueStack: [...stack],
            message: `DFS Start: Pushed ${start} to stack.`
        });

        while (stack.length > 0) {
            const curr = stack.pop()!;

            if (!visited.has(curr)) {
                visited.add(curr);

                steps.push({
                    ...currentState,
                    activeNodes: [curr],
                    visitedNodes: [...Array.from(visited)],
                    queueStack: [...stack],
                    message: `Popped ${curr}. Mark as visited.`
                });

                const neighbors = currentState.adjList[curr] || [];
                // Reverse to process in natural order if pushed
                for (let i = neighbors.length - 1; i >= 0; i--) {
                    const neighbor = neighbors[i];
                    if (!visited.has(neighbor)) {
                        stack.push(neighbor);
                        steps.push({
                            ...currentState,
                            activeNodes: [curr],
                            visitedNodes: [...Array.from(visited)],
                            queueStack: [...stack],
                            message: `Push neighbor ${neighbor} to stack.`
                        });
                    }
                }
            }
        }

        steps.push({
            ...currentState,
            activeNodes: [],
            visitedNodes: [...Array.from(visited)],
            queueStack: [],
            message: `DFS Complete.`
        });

        addToHistory(steps);
    };


    return (
        <BaseVisualizer
            title="Graph"
            description="Network of nodes (vertices) and edges. Supports BFS and DFS."
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
            <div className="flex flex-col items-center gap-6 w-full max-w-4xl">
                {/* Controls */}
                <div className="flex flex-wrap items-center justify-center gap-4 bg-white p-4 rounded-lg shadow-sm border border-gray-200">
                    {/* Add Vertex */}
                    <div className="flex items-center gap-2">
                        <input
                            type="text"
                            value={vertexLabel}
                            onChange={(e) => setVertexLabel(e.target.value)}
                            placeholder="Vertex (e.g. A)"
                            className="w-24 px-2 py-1 border rounded text-sm"
                        />
                        <button onClick={handleAddVertex} className="flex items-center gap-1 bg-blue-600 text-white px-2 py-1 rounded text-sm hover:bg-blue-700">
                            <Plus className="w-3 h-3" /> Node
                        </button>
                    </div>
                    <div className="w-px h-8 bg-gray-200"></div>

                    {/* Add Edge */}
                    <div className="flex items-center gap-2">
                        <input
                            type="text"
                            value={edgeSource}
                            onChange={(e) => setEdgeSource(e.target.value)}
                            placeholder="Src"
                            className="w-16 px-2 py-1 border rounded text-sm"
                        />
                        <input
                            type="text"
                            value={edgeTarget}
                            onChange={(e) => setEdgeTarget(e.target.value)}
                            placeholder="Tgt"
                            className="w-16 px-2 py-1 border rounded text-sm"
                        />
                        <button onClick={handleAddEdge} className="flex items-center gap-1 bg-indigo-600 text-white px-2 py-1 rounded text-sm hover:bg-indigo-700">
                            <Share2 className="w-3 h-3" /> Edge
                        </button>
                    </div>
                    <div className="w-px h-8 bg-gray-200"></div>

                    {/* Algorithms */}
                    <div className="flex items-center gap-2">
                        <input
                            type="text"
                            value={startNode}
                            onChange={(e) => setStartNode(e.target.value)}
                            placeholder="Start"
                            className="w-16 px-2 py-1 border rounded text-sm"
                        />
                        <button onClick={handleBFS} className="flex items-center gap-1 bg-green-600 text-white px-2 py-1 rounded text-sm hover:bg-green-700">
                            <Play className="w-3 h-3" /> BFS
                        </button>
                        <button onClick={handleDFS} className="flex items-center gap-1 bg-purple-600 text-white px-2 py-1 rounded text-sm hover:bg-purple-700">
                            <Play className="w-3 h-3" /> DFS
                        </button>
                    </div>
                </div>

                <div className="flex gap-8 w-full">
                    {/* Canvas */}
                    <div className="relative w-full h-[400px] border rounded-lg bg-gray-50 overflow-hidden shadow-inner">
                        <AnimatePresence>
                            {/* Edges */}
                            {currentState.edges.map((edge, idx) => {
                                const u = currentState.nodes.find(n => n.id === edge.source);
                                const v = currentState.nodes.find(n => n.id === edge.target);
                                if (!u || !v) return null;

                                return (
                                    <motion.svg key={`edge-${idx}`} className="absolute top-0 left-0 w-full h-full pointer-events-none">
                                        <line
                                            x1={u.x}
                                            y1={u.y}
                                            x2={v.x}
                                            y2={v.y}
                                            stroke="#94a3b8"
                                            strokeWidth="2"
                                        />
                                    </motion.svg>
                                );
                            })}

                            {/* Vertices */}
                            {currentState.nodes.map((node) => {
                                const isVisited = currentState.visitedNodes.includes(node.id);
                                const isActive = currentState.activeNodes.includes(node.id);

                                return (
                                    <motion.div
                                        key={node.id}
                                        initial={{ scale: 0 }}
                                        animate={{
                                            scale: 1,
                                            backgroundColor: isActive ? '#facc15' : isVisited ? '#4ade80' : '#ffffff',
                                            borderColor: isActive ? '#ca8a04' : isVisited ? '#16a34a' : '#94a3b8',
                                            // Ensure contrast
                                            color: '#1e293b'
                                        }}
                                        className="absolute w-10 h-10 -ml-5 -mt-5 flex items-center justify-center rounded-full border-2 font-bold shadow-sm z-10 cursor-default"
                                        style={{ left: node.x, top: node.y }}
                                    >
                                        {node.id}
                                    </motion.div>
                                );
                            })}
                        </AnimatePresence>
                    </div>

                    {/* Data Structures View (Queue/Stack) */}
                    <div className="w-48 flex flex-col gap-4">
                        <div className="bg-white p-2 rounded border h-full">
                            <h3 className="font-semibold text-sm mb-2 text-center text-gray-700">Queue / Stack</h3>
                            <div className="flex flex-col gap-1">
                                {currentState.queueStack.map((val, idx) => (
                                    <div key={idx} className="bg-gray-100 p-1 text-center rounded text-sm border">
                                        {val}
                                    </div>
                                ))}
                                {currentState.queueStack.length === 0 && <span className="text-xs text-gray-400 text-center italic">Empty</span>}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </BaseVisualizer>
    );
};
