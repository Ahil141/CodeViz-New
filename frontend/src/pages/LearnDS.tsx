import { useState, useEffect } from 'react'
import { Layers, List, GitBranch, ArrowLeft } from 'lucide-react'
import DSWorkspace from '../components/DSWorkspace'

type DataStructure = string | null

const API_BASE_URL =
  (import.meta.env?.VITE_API_BASE_URL as string) || 'http://localhost:8000'

function LearnDS() {
  const [selectedDS, setSelectedDS] = useState<DataStructure>(null)
  const [visualizerCode, setVisualizerCode] = useState<string | null>(null)
  const [isLoadingVisualizer, setIsLoadingVisualizer] = useState(false)



  // Extended Data Structures List
  const dataStructures: { id: string, name: string, icon: any, description: string }[] = [
    { id: 'stack', name: 'Stack', icon: Layers, description: 'LIFO (Last In First Out)' },
    { id: 'queue', name: 'Queue', icon: List, description: 'FIFO (First In First Out)' },
    { id: 'linked-list', name: 'Singly Linked List', icon: GitBranch, description: 'Basic Linked List' },

    { id: 'doubly-linked-list', name: 'Doubly Linked List', icon: GitBranch, description: 'Nodes with Prev/Next pointers' },
    { id: 'circular-linked-list', name: 'Circular Linked List', icon: GitBranch, description: 'Last node points to head' },
    { id: 'circular-doubly-linked-list', name: 'Circular Doubly Linked List', icon: GitBranch, description: 'Circular + Doubly' },
    { id: 'skip-list', name: 'Skip List', icon: List, description: 'Probabilistic Data Structure' },
    { id: 'unrolled-linked-list', name: 'Unrolled Linked List', icon: List, description: 'Nodes store arrays' },
    { id: 'xor-linked-list', name: 'XOR Linked List', icon: GitBranch, description: 'Memory efficient doubly list' },

    { id: 'array', name: 'Arrays', icon: List, description: 'Contiguous memory' },
    { id: 'dynamic-array', name: 'Dynamic Array', icon: List, description: 'Resizable array (Vector)' },
    { id: 'sparse-array', name: 'Sparse Array', icon: List, description: 'Memory efficient for sparse data' },
    { id: 'jagged-array', name: 'Jagged Array', icon: List, description: 'Array of arrays (uneven)' },
    { id: 'circular-array', name: 'Circular Array', icon: List, description: 'Ring buffer' },

    { id: 'general-tree', name: 'General Tree', icon: GitBranch, description: 'N-ary Tree' },
    { id: 'binary-tree', name: 'Binary Tree', icon: GitBranch, description: 'Up to 2 children' },
    { id: 'bst', name: 'Binary Search Tree (BST)', icon: GitBranch, description: 'Ordered Binary Tree' },
    { id: 'avl', name: 'AVL Tree', icon: GitBranch, description: 'Self-balancing BST' },
    { id: 'red-black', name: 'Red-Black Tree', icon: GitBranch, description: 'Balanced BST with colors' },
    { id: 'splay', name: 'Splay Tree', icon: GitBranch, description: 'Self-optimizing BST' },
    { id: 'treap', name: 'Treap', icon: GitBranch, description: 'Tree + Heap' },
    { id: 'scapegoat', name: 'Scapegoat Tree', icon: GitBranch, description: 'Self-balancing (rebuilds)' },

    { id: 'heap-min', name: 'Min Heap', icon: Layers, description: 'Root is minimum' },
    { id: 'heap-max', name: 'Max Heap', icon: Layers, description: 'Root is maximum' },
    { id: 'binomial-heap', name: 'Binomial Heap', icon: Layers, description: 'Binomial trees collection' },
    { id: 'fibonacci-heap', name: 'Fibonacci Heap', icon: Layers, description: 'Fast amortized operations' },
    { id: 'pairing-heap', name: 'Pairing Heap', icon: Layers, description: 'Self-adjusting heap' },

    { id: 'b-tree', name: 'B-Tree', icon: GitBranch, description: 'Self-balancing search tree' },
    { id: 'b-plus-tree', name: 'B+ Tree', icon: GitBranch, description: 'B-Tree with linked leaves' },
    { id: 'b-star-tree', name: 'B* Tree', icon: GitBranch, description: 'B-Tree variant' },

    { id: 'graph-directed', name: 'Directed Graph', icon: GitBranch, description: 'One-way edges' },
    { id: 'graph-undirected', name: 'Undirected Graph', icon: GitBranch, description: 'Two-way edges' },
    { id: 'graph-weighted', name: 'Weighted Graph', icon: GitBranch, description: 'Edges with costs' },
    { id: 'graph-unweighted', name: 'Unweighted Graph', icon: GitBranch, description: 'Edges without costs' },
    { id: 'graph-cyclic', name: 'Cyclic Graph', icon: GitBranch, description: 'Contains cycles' },
    { id: 'graph-acyclic', name: 'Acyclic Graph', icon: GitBranch, description: 'No cycles' },
    { id: 'graph-dag', name: 'DAG', icon: GitBranch, description: 'Directed Acyclic Graph' },

    { id: 'adj-matrix', name: 'Adjacency Matrix', icon: List, description: 'Graph Matrix View' },
    { id: 'adj-list', name: 'Adjacency List', icon: List, description: 'Graph List View' },
    { id: 'edge-list', name: 'Edge List', icon: List, description: 'List of Edges' }

  ]

  // Fetch visualizer code when data structure changes
  useEffect(() => {
    if (!selectedDS) {
      setVisualizerCode(null)
      return
    }

    const fetchVisualizerCode = async () => {
      setIsLoadingVisualizer(true)
      try {
        const dsName = dataStructures.find((ds) => ds.id === selectedDS)?.name || ''
        const response = await fetch(`${API_BASE_URL}/api/rag/query`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            data_structure_name: dsName,
          }),
        })

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }

        const data = await response.json()
        // Extract visualizer code from response
        if (data.success && data.visualizer_code) {
          setVisualizerCode(data.visualizer_code)
        } else {
          throw new Error(data.error || 'Failed to fetch visualizer code')
        }
      } catch (error) {
        console.error('Error fetching visualizer code:', error)
        setVisualizerCode(null)
      } finally {
        setIsLoadingVisualizer(false)
      }
    }

    fetchVisualizerCode()
  }, [selectedDS])

  return (
    <div className="h-full flex flex-col">
      {selectedDS ? (
        <>
          <div className="bg-white border-b border-gray-200 px-6 py-4 flex items-center gap-4">
            <button
              onClick={() => setSelectedDS(null)}
              className="flex items-center gap-2 text-gray-600 hover:text-indigo-600 transition-colors"
            >
              <ArrowLeft className="w-5 h-5" />
              <span>Back to Selection</span>
            </button>
            <div className="h-6 w-px bg-gray-300" />
            <div className="flex items-center gap-2">
              {(() => {
                const ds = dataStructures.find((d) => d.id === selectedDS)
                const Icon = ds?.icon || Layers
                return (
                  <>
                    <Icon className="w-5 h-5 text-indigo-600" />
                    <span className="font-semibold text-gray-800">
                      {ds?.name}
                    </span>
                  </>
                )
              })()}
            </div>
          </div>
          <div className="flex-1 overflow-hidden">
            <DSWorkspace
              visualizerCode={visualizerCode}
              isLoadingVisualizer={isLoadingVisualizer}
            />
          </div>
        </>
      ) : (
        <div className="p-8 overflow-y-auto">
          <div className="max-w-6xl mx-auto">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              Learn Data Structures
            </h1>
            <p className="text-lg text-gray-600 mb-8">
              Select a data structure to learn more about it.
            </p>

            {/* Data Structure Buttons */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
              {dataStructures.map((ds) => {
                const Icon = ds.icon
                const isSelected = selectedDS === ds.id

                return (
                  <button
                    key={ds.id}
                    onClick={() => setSelectedDS(ds.id)}
                    className={`
                  bg-white rounded-lg shadow-md p-6 border-2 transition-all
                  text-left hover:shadow-lg
                  ${isSelected
                        ? 'border-indigo-600 bg-indigo-50'
                        : 'border-gray-200 hover:border-indigo-300'
                      }
                `}
                  >
                    <div className="flex items-center gap-3 mb-3">
                      <div
                        className={`
                      p-2 rounded-lg
                      ${isSelected ? 'bg-indigo-600' : 'bg-gray-100'}
                    `}
                      >
                        <Icon
                          className={`w-6 h-6 ${isSelected ? 'text-white' : 'text-gray-700'
                            }`}
                        />
                      </div>
                      <h3
                        className={`
                      text-xl font-semibold
                      ${isSelected ? 'text-indigo-700' : 'text-gray-800'}
                    `}
                      >
                        {ds.name}
                      </h3>
                    </div>
                    <p className="text-sm text-gray-600">{ds.description}</p>
                  </button>
                )
              })}
            </div>

            {!selectedDS && (
              <div className="bg-gray-50 rounded-lg p-8 text-center border border-gray-200">
                <p className="text-gray-500">
                  Select a data structure above to start learning with interactive
                  chat and visualizations.
                </p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default LearnDS
