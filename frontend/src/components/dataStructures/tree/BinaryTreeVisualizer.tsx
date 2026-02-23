import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { BaseVisualizer } from '../BaseVisualizer';
import { Plus, Play, Search, Trash2 } from 'lucide-react';

interface TreeNode {
    id: string;
    value: number;
    left: TreeNode | null;
    right: TreeNode | null;
    x?: number; // Calculated for rendering
    y?: number;
}

interface TreeState {
    root: TreeNode | null;
    message: string;
    activeIds: string[];
}

// Helper to layout tree
const layoutTree = (node: TreeNode | null, x: number, y: number, level: number): TreeNode | null => {
    if (!node) return null;

    // Horizontal spacing decreases as level increases to avoid overlap
    // Level 0: 200px gap (approx) relative to parent? No, width/2^level
    const offset = 200 / Math.pow(1.5, level);

    const newNode = { ...node, x, y };
    newNode.left = layoutTree(node.left, x - offset, y + 60, level + 1);
    newNode.right = layoutTree(node.right, x + offset, y + 60, level + 1);
    return newNode;
};

interface TreeEdge {
    id: string;
    x1: number;
    y1: number;
    x2: number;
    y2: number;
}

// Flatten tree for rendering
const flattenTree = (node: TreeNode | null, nodes: TreeNode[] = [], edges: TreeEdge[] = []): { nodes: TreeNode[], edges: TreeEdge[] } => {
    if (!node) return { nodes, edges };

    nodes.push(node);

    if (node.left) {
        edges.push({ id: `${node.id}-${node.left.id}`, x1: node.x!, y1: node.y!, x2: node.left.x!, y2: node.left.y! });
        flattenTree(node.left, nodes, edges);
    }
    if (node.right) {
        edges.push({ id: `${node.id}-${node.right.id}`, x1: node.x!, y1: node.y!, x2: node.right.x!, y2: node.right.y! });
        flattenTree(node.right, nodes, edges);
    }
    return { nodes, edges };
};

const cloneTree = (node: TreeNode | null): TreeNode | null => {
    if (!node) return null;
    return {
        ...node,
        left: cloneTree(node.left),
        right: cloneTree(node.right)
    };
};

export const BinaryTreeVisualizer = () => {
    const [history, setHistory] = useState<TreeState[]>([
        { root: null, message: 'Tree is empty. Start by inserting a value.', activeIds: [] }
    ]);
    const [currentStep, setCurrentStep] = useState(0);
    const [inputValue, setInputValue] = useState('');
    const [isPlaying, setIsPlaying] = useState(false);

    const currentState = history[currentStep];

    // Calculate layout for current state
    const rootWithLayout = layoutTree(currentState.root, 400, 50, 0); // 400 is center of 800px canvas
    const { nodes: renderNodes, edges: renderEdges } = flattenTree(rootWithLayout);

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

    const addToHistory = (newState: TreeState) => {
        const newHistory = [...history.slice(0, currentStep + 1), newState];
        setHistory(newHistory);
        setCurrentStep(newHistory.length - 1);
    };

    const handleInsert = () => {
        const val = parseInt(inputValue);
        if (isNaN(val)) return;

        if (currentState.activeIds.length > 0) {
            // Clear previous selection
        }

        const newRoot = cloneTree(currentState.root);

        // BST Insert Logic
        const maxDepth = 4;

        if (!newRoot) {
            addToHistory({
                root: { id: `node-${Date.now()}`, value: val, left: null, right: null },
                message: `Inserted root ${val}.`,
                activeIds: []
            });
            setInputValue('');
            return;
        }

        const insertNode = (node: TreeNode, value: number, depth: number): boolean => {
            if (depth >= maxDepth) {
                alert("Max tree depth reached for visualization.");
                return false;
            }
            if (value < node.value) {
                if (!node.left) {
                    node.left = { id: `node-${Date.now()}`, value, left: null, right: null };
                    return true;
                } else {
                    return insertNode(node.left, value, depth + 1);
                }
            } else {
                if (!node.right) {
                    node.right = { id: `node-${Date.now()}`, value, left: null, right: null };
                    return true;
                } else {
                    return insertNode(node.right, value, depth + 1);
                }
            }
        };

        if (insertNode(newRoot, val, 0)) {
            addToHistory({
                root: newRoot,
                message: `Inserted ${val} into BST.`,
                activeIds: []
            });
        }

        setInputValue('');
    };

    const handleTraversal = (type: 'inorder' | 'preorder' | 'postorder') => {
        if (!currentState.root) return;

        const traversalSteps: string[] = [];
        const traversalNodes: TreeNode[] = [];

        const traverse = (node: TreeNode | null) => {
            if (!node) return;

            if (type === 'preorder') {
                traversalSteps.push(node.id);
                traversalNodes.push(node);
            }

            traverse(node.left);

            if (type === 'inorder') {
                traversalSteps.push(node.id);
                traversalNodes.push(node);
            }

            traverse(node.right);

            if (type === 'postorder') {
                traversalSteps.push(node.id);
                traversalNodes.push(node);
            }
        };

        traverse(currentState.root);

        // Generate history from steps
        const baseHistory = history.slice(0, currentStep + 1);
        const newHistoryItems: TreeState[] = [];

        traversalSteps.forEach((id, index) => {
            const nodeVal = traversalNodes[index].value;
            newHistoryItems.push({
                root: currentState.root, // Structure doesn't change
                message: `${type.charAt(0).toUpperCase() + type.slice(1)}: Visiting ${nodeVal}`,
                activeIds: [id]
            });
        });

        newHistoryItems.push({
            root: currentState.root,
            message: 'Traversal Complete.',
            activeIds: []
        });

        setHistory([...baseHistory, ...newHistoryItems]);
        setCurrentStep(currentStep + 1);
        setIsPlaying(true);
    };

    const handleSearch = () => {
        const val = parseInt(inputValue);
        if (isNaN(val)) return;
        if (!currentState.root) return;

        let curr: TreeNode | null = currentState.root;
        const searchSteps: TreeState[] = [];
        let found = false;

        while (curr) {
            searchSteps.push({
                root: currentState.root,
                message: `Searching for ${val}... Visiting ${curr.value}`,
                activeIds: [curr.id]
            });

            if (val === curr.value) {
                found = true;
                searchSteps.push({
                    root: currentState.root,
                    message: `Found ${val}!`,
                    activeIds: [curr.id]
                });
                break;
            } else if (val < curr.value) {
                curr = curr.left;
            } else {
                curr = curr.right;
            }
        }

        if (!found) {
            searchSteps.push({
                root: currentState.root,
                message: `${val} not found.`,
                activeIds: []
            });
        }

        const baseHistory = history.slice(0, currentStep + 1);
        setHistory([...baseHistory, ...searchSteps]);
        setCurrentStep(baseHistory.length);
        setIsPlaying(true);
        setInputValue('');
    };

    const handleDelete = () => {
        const val = parseInt(inputValue);
        if (isNaN(val)) return;

        const newRoot = cloneTree(currentState.root);
        let deleted = false;

        const deleteNode = (node: TreeNode | null, v: number): TreeNode | null => {
            if (!node) return null;
            if (v < node.value) {
                node.left = deleteNode(node.left, v);
                return node;
            } else if (v > node.value) {
                node.right = deleteNode(node.right, v);
                return node;
            } else {
                deleted = true;
                // Node with only one child or no child
                if (!node.left) return node.right;
                if (!node.right) return node.left;

                // Node with two children: Get inorder successor (smallest in the right subtree)
                let temp = node.right;
                while (temp.left) {
                    temp = temp.left;
                }
                node.value = temp.value;
                node.right = deleteNode(node.right, temp.value);
                return node;
            }
        };

        const finalRoot = deleteNode(newRoot, val);

        if (deleted) {
            addToHistory({
                root: finalRoot,
                message: `Deleted ${val}.`,
                activeIds: []
            });
        } else {
            addToHistory({
                root: currentState.root,
                message: `Cannot delete ${val}: Not found.`,
                activeIds: []
            });
        }
        setInputValue('');
    };


    return (
        <BaseVisualizer
            title="Binary Search Tree"
            description="Hierarchical data structure. Left child < Parent < Right child."
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
                            className="w-20 px-2 py-1 border rounded text-sm focus:outline-blue-500"
                            onKeyDown={(e) => {
                                if (e.key === 'Enter') handleInsert();
                            }}
                        />
                        <button onClick={handleInsert} className="flex items-center gap-1 bg-blue-600 text-white px-3 py-1 rounded text-sm hover:bg-blue-700 transition-colors">
                            <Plus className="w-3 h-3" /> Insert
                        </button>
                        <button onClick={handleSearch} className="flex items-center gap-1 bg-green-600 text-white px-3 py-1 rounded text-sm hover:bg-green-700 transition-colors">
                            <Search className="w-3 h-3" /> Search
                        </button>
                        <button onClick={handleDelete} className="flex items-center gap-1 bg-red-600 text-white px-3 py-1 rounded text-sm hover:bg-red-700 transition-colors">
                            <Trash2 className="w-3 h-3" /> Delete
                        </button>
                    </div>

                    <div className="w-px h-8 bg-gray-200 hidden md:block"></div>

                    <div className="flex gap-2">
                        <button onClick={() => handleTraversal('inorder')} className="flex items-center gap-1 bg-purple-100 text-purple-700 px-2 py-1 rounded text-xs hover:bg-purple-200 transition-colors">
                            <Play className="w-3 h-3" /> Inorder
                        </button>
                        <button onClick={() => handleTraversal('preorder')} className="flex items-center gap-1 bg-purple-100 text-purple-700 px-2 py-1 rounded text-xs hover:bg-purple-200 transition-colors">
                            <Play className="w-3 h-3" /> Pre
                        </button>
                        <button onClick={() => handleTraversal('postorder')} className="flex items-center gap-1 bg-purple-100 text-purple-700 px-2 py-1 rounded text-xs hover:bg-purple-200 transition-colors">
                            <Play className="w-3 h-3" /> Post
                        </button>
                    </div>
                </div>

                {/* Message Area */}
                <div className="min-h-[24px] text-center font-medium text-gray-600">
                    {currentState.message}
                </div>

                {/* Visualization Canvas */}
                <div className="w-full h-[400px] bg-gray-50/50 rounded-lg relative overflow-hidden flex items-center justify-center">
                    <div className="relative w-full h-full max-w-[800px]">

                        {/* SVG Layer for Edges */}
                        <svg className="absolute inset-0 w-full h-full pointer-events-none z-0">
                            {renderEdges.map(edge => (
                                <motion.line
                                    key={edge.id}
                                    initial={{ pathLength: 0, opacity: 0 }}
                                    animate={{ pathLength: 1, opacity: 1 }}
                                    x1={edge.x1}
                                    y1={edge.y1}
                                    x2={edge.x2}
                                    y2={edge.y2}
                                    stroke="#cbd5e1"
                                    strokeWidth="2"
                                />
                            ))}
                        </svg>

                        {/* Nodes Layer */}
                        <AnimatePresence>
                            {renderNodes.map((node) => (
                                <motion.div
                                    key={node.id}
                                    layout
                                    initial={{ scale: 0, opacity: 0 }}
                                    animate={{

                                        opacity: 1,
                                        left: node.x,
                                        top: node.y,
                                        x: '-50%', // Center the node on the coordinate
                                        y: '-50%',
                                        backgroundColor: currentState.activeIds.includes(node.id) ? '#dbeafe' : '#ffffff',
                                        borderColor: currentState.activeIds.includes(node.id) ? '#2563eb' : '#e5e7eb',
                                        scale: currentState.activeIds.includes(node.id) ? 1.2 : 1
                                    }}
                                    transition={{ type: "spring", stiffness: 300, damping: 25 }}
                                    className="absolute w-10 h-10 flex items-center justify-center rounded-full border-2 bg-white shadow-sm font-bold text-gray-700 z-10"
                                >
                                    {node.value}
                                </motion.div>
                            ))}
                        </AnimatePresence>

                        {renderNodes.length === 0 && (
                            <div className="absolute inset-0 flex items-center justify-center text-gray-300">
                                Empty Tree
                            </div>
                        )}
                    </div>
                </div>

            </div>
        </BaseVisualizer>
    );
};
