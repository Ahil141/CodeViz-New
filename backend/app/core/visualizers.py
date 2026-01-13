from typing import Dict, Optional
from app.core.visualizers_linked_lists import *
from app.core.visualizers_arrays import *
from app.core.visualizers_trees import *
from app.core.visualizers_graphs import *
from app.core.visualizers_heaps import *
from app.core.visualizers_advanced import *


# Stack Visualizer
STACK_VISUALIZER = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stack Visualizer</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 600px;
            width: 100%;
        }
        h1 {
            color: #333;
            margin-bottom: 20px;
            text-align: center;
        }
        .controls {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        input, button {
            padding: 12px 20px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
        }
        input {
            flex: 1;
            min-width: 150px;
        }
        button {
            background: #667eea;
            color: white;
            border: none;
            cursor: pointer;
            transition: background 0.3s;
        }
        button:hover {
            background: #5568d3;
        }
        button:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        .stack-container {
            min-height: 400px;
            border: 3px solid #667eea;
            border-radius: 10px;
            padding: 20px;
            display: flex;
            flex-direction: column-reverse;
            justify-content: flex-start;
            align-items: center;
            gap: 10px;
            background: #f8f9fa;
        }
        .stack-item {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 30px;
            border-radius: 8px;
            font-size: 18px;
            font-weight: bold;
            min-width: 200px;
            text-align: center;
            animation: slideIn 0.3s ease;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .stack-empty {
            color: #999;
            font-style: italic;
            margin: auto;
        }
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        .info {
            margin-top: 20px;
            padding: 15px;
            background: #e3f2fd;
            border-radius: 8px;
            color: #1976d2;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 Stack Visualizer</h1>
        <div class="controls">
            <input type="text" id="valueInput" placeholder="Enter value to push">
            <button onclick="push()">Push</button>
            <button onclick="pop()">Pop</button>
            <button onclick="clearStack()">Clear</button>
        </div>
        <div class="stack-container" id="stackContainer">
            <div class="stack-empty">Stack is empty</div>
        </div>
        <div class="info">
            <strong>Operations:</strong> Push (add to top) | Pop (remove from top)<br>
            <strong>Principle:</strong> LIFO (Last In, First Out)
        </div>
    </div>
    <script>
        let stack = [];
        const stackContainer = document.getElementById('stackContainer');
        const valueInput = document.getElementById('valueInput');
        function updateDisplay() {
            stackContainer.innerHTML = '';
            if (stack.length === 0) {
                stackContainer.innerHTML = '<div class="stack-empty">Stack is empty</div>';
            } else {
                stack.forEach((item, index) => {
                    const element = document.createElement('div');
                    element.className = 'stack-item';
                    element.textContent = item;
                    stackContainer.appendChild(element);
                });
            }
        }
        function push() {
            const value = valueInput.value.trim();
            if (value === '') {
                alert('Please enter a value');
                return;
            }
            stack.push(value);
            valueInput.value = '';
            updateDisplay();
        }
        function pop() {
            if (stack.length === 0) {
                alert('Stack is empty!');
                return;
            }
            const popped = stack.pop();
            alert(`Popped: ${popped}`);
            updateDisplay();
        }
        function clearStack() {
            stack = [];
            updateDisplay();
        }
        valueInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                push();
            }
        });
        updateDisplay();
    </script>
</body>
</html>"""


# Queue Visualizer
QUEUE_VISUALIZER = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Queue Visualizer</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 700px;
            width: 100%;
        }
        h1 {
            color: #333;
            margin-bottom: 20px;
            text-align: center;
        }
        .controls {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        input, button {
            padding: 12px 20px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
        }
        input {
            flex: 1;
            min-width: 150px;
        }
        button {
            background: #f5576c;
            color: white;
            border: none;
            cursor: pointer;
            transition: background 0.3s;
        }
        button:hover {
            background: #e0485c;
        }
        button:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        .queue-container {
            min-height: 200px;
            border: 3px solid #f5576c;
            border-radius: 10px;
            padding: 20px;
            display: flex;
            flex-direction: row;
            justify-content: flex-start;
            align-items: center;
            gap: 15px;
            background: #f8f9fa;
            overflow-x: auto;
        }
        .queue-item {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 20px 25px;
            border-radius: 8px;
            font-size: 18px;
            font-weight: bold;
            min-width: 80px;
            text-align: center;
            animation: slideIn 0.3s ease;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            flex-shrink: 0;
        }
        .queue-empty {
            color: #999;
            font-style: italic;
            margin: auto;
        }
        .queue-labels {
            display: flex;
            justify-content: space-between;
            margin-top: 10px;
            font-size: 14px;
            color: #666;
        }
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        .info {
            margin-top: 20px;
            padding: 15px;
            background: #fce4ec;
            border-radius: 8px;
            color: #c2185b;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚶 Queue Visualizer</h1>
        <div class="controls">
            <input type="text" id="valueInput" placeholder="Enter value to enqueue">
            <button onclick="enqueue()">Enqueue</button>
            <button onclick="dequeue()">Dequeue</button>
            <button onclick="clearQueue()">Clear</button>
        </div>
        <div class="queue-container" id="queueContainer">
            <div class="queue-empty">Queue is empty</div>
        </div>
        <div class="queue-labels">
            <span>← Front (Dequeue)</span>
            <span>Back (Enqueue) →</span>
        </div>
        <div class="info">
            <strong>Operations:</strong> Enqueue (add to back) | Dequeue (remove from front)<br>
            <strong>Principle:</strong> FIFO (First In, First Out)
        </div>
    </div>
    <script>
        let queue = [];
        const queueContainer = document.getElementById('queueContainer');
        const valueInput = document.getElementById('valueInput');
        function updateDisplay() {
            queueContainer.innerHTML = '';
            if (queue.length === 0) {
                queueContainer.innerHTML = '<div class="queue-empty">Queue is empty</div>';
            } else {
                queue.forEach((item, index) => {
                    const element = document.createElement('div');
                    element.className = 'queue-item';
                    element.textContent = item;
                    queueContainer.appendChild(element);
                });
            }
        }
        function enqueue() {
            const value = valueInput.value.trim();
            if (value === '') {
                alert('Please enter a value');
                return;
            }
            queue.push(value);
            valueInput.value = '';
            updateDisplay();
        }
        function dequeue() {
            if (queue.length === 0) {
                alert('Queue is empty!');
                return;
            }
            const dequeued = queue.shift();
            alert(`Dequeued: ${dequeued}`);
            updateDisplay();
        }
        function clearQueue() {
            queue = [];
            updateDisplay();
        }
        valueInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                enqueue();
            }
        });
        updateDisplay();
    </script>
</body>
</html>"""


# Singly Linked List Visualizer
LINKED_LIST_VISUALIZER = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Singly Linked List Visualizer</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 900px;
            width: 100%;
        }
        h1 {
            color: #333;
            margin-bottom: 20px;
            text-align: center;
        }
        .controls {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        input, button {
            padding: 12px 20px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
        }
        input {
            flex: 1;
            min-width: 150px;
        }
        button {
            background: #4facfe;
            color: white;
            border: none;
            cursor: pointer;
            transition: background 0.3s;
        }
        button:hover {
            background: #3d8fe0;
        }
        button:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        .list-container {
            min-height: 300px;
            border: 3px solid #4facfe;
            border-radius: 10px;
            padding: 30px;
            background: #f8f9fa;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 20px;
        }
        .node {
            display: flex;
            align-items: center;
            gap: 0;
            animation: slideIn 0.3s ease;
        }
        .node-box {
            background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            padding: 15px 25px;
            border-radius: 8px 0 0 8px;
            font-size: 18px;
            font-weight: bold;
            min-width: 80px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .node-pointer {
            background: #333;
            color: white;
            padding: 15px 20px;
            border-radius: 0 8px 8px 0;
            font-size: 16px;
            min-width: 60px;
            text-align: center;
            position: relative;
        }
        .node-pointer::after {
            content: '→';
            margin-left: 10px;
        }
        .node:last-child .node-pointer::after {
            content: 'null';
            margin-left: 10px;
        }
        .list-empty {
            color: #999;
            font-style: italic;
            margin: auto;
        }
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        .info {
            margin-top: 20px;
            padding: 15px;
            background: #e0f7fa;
            border-radius: 8px;
            color: #006064;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔗 Singly Linked List Visualizer</h1>
        <div class="controls">
            <input type="text" id="valueInput" placeholder="Enter value">
            <input type="number" id="indexInput" placeholder="Index (for insert/delete)" min="0">
            <button onclick="insertAtHead()">Insert at Head</button>
            <button onclick="insertAtTail()">Insert at Tail</button>
            <button onclick="insertAtIndex()">Insert at Index</button>
            <button onclick="deleteByValue()">Delete by Value</button>
            <button onclick="clearList()">Clear</button>
        </div>
        <div class="list-container" id="listContainer">
            <div class="list-empty">Linked List is empty</div>
        </div>
        <div class="info">
            <strong>Operations:</strong> Insert at Head/Tail/Index | Delete by Value<br>
            <strong>Structure:</strong> Each node contains data and a pointer to the next node
        </div>
    </div>
    <script>
        class Node {
            constructor(data) {
                this.data = data;
                this.next = null;
            }
        }
        let head = null;
        const listContainer = document.getElementById('listContainer');
        const valueInput = document.getElementById('valueInput');
        const indexInput = document.getElementById('indexInput');
        function updateDisplay() {
            listContainer.innerHTML = '';
            if (head === null) {
                listContainer.innerHTML = '<div class="list-empty">Linked List is empty</div>';
                return;
            }
            let current = head;
            while (current !== null) {
                const nodeDiv = document.createElement('div');
                nodeDiv.className = 'node';
                const dataBox = document.createElement('div');
                dataBox.className = 'node-box';
                dataBox.textContent = current.data;
                const pointerBox = document.createElement('div');
                pointerBox.className = 'node-pointer';
                nodeDiv.appendChild(dataBox);
                nodeDiv.appendChild(pointerBox);
                listContainer.appendChild(nodeDiv);
                current = current.next;
            }
        }
        function insertAtHead() {
            const value = valueInput.value.trim();
            if (value === '') {
                alert('Please enter a value');
                return;
            }
            const newNode = new Node(value);
            newNode.next = head;
            head = newNode;
            valueInput.value = '';
            updateDisplay();
        }
        function insertAtTail() {
            const value = valueInput.value.trim();
            if (value === '') {
                alert('Please enter a value');
                return;
            }
            const newNode = new Node(value);
            if (head === null) {
                head = newNode;
            } else {
                let current = head;
                while (current.next !== null) {
                    current = current.next;
                }
                current.next = newNode;
            }
            valueInput.value = '';
            updateDisplay();
        }
        function insertAtIndex() {
            const value = valueInput.value.trim();
            const index = parseInt(indexInput.value);
            if (value === '') {
                alert('Please enter a value');
                return;
            }
            if (isNaN(index) || index < 0) {
                alert('Please enter a valid index');
                return;
            }
            if (index === 0) {
                insertAtHead();
                return;
            }
            const newNode = new Node(value);
            let current = head;
            for (let i = 0; i < index - 1; i++) {
                if (current === null) {
                    alert('Index out of bounds');
                    return;
                }
                current = current.next;
            }
            if (current === null) {
                alert('Index out of bounds');
                return;
            }
            newNode.next = current.next;
            current.next = newNode;
            valueInput.value = '';
            indexInput.value = '';
            updateDisplay();
        }
        function deleteByValue() {
            const value = valueInput.value.trim();
            if (value === '') {
                alert('Please enter a value to delete');
                return;
            }
            if (head === null) {
                alert('List is empty');
                return;
            }
            if (head.data === value) {
                head = head.next;
                valueInput.value = '';
                updateDisplay();
                return;
            }
            let current = head;
            while (current.next !== null && current.next.data !== value) {
                current = current.next;
            }
            if (current.next === null) {
                alert('Value not found');
                return;
            }
            current.next = current.next.next;
            valueInput.value = '';
            updateDisplay();
        }
        function clearList() {
            head = null;
            updateDisplay();
        }
        valueInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                insertAtTail();
            }
        });
        updateDisplay();
    </script>
</body>
</html>"""


def get_default_visualizer(name: str) -> Optional[Dict[str, str]]:
    """
    Get a default visualizer by name.
    
    Args:
        name: Name of the data structure (case-insensitive).
        
    Returns:
        Dictionary with description and visualizer code, or None if not found.
    """
    name_lower = name.lower()
    
    if "stack" in name_lower:
        return {
            "name": "Stack",
            "description": "Interactive Stack visualizer demonstrating LIFO (Last In, First Out) operations",
            "visualizer_code": STACK_VISUALIZER
        }
    elif "queue" in name_lower:
        return {
            "name": "Queue",
            "description": "Interactive Queue visualizer demonstrating FIFO (First In, First Out) operations",
            "visualizer_code": QUEUE_VISUALIZER
        }
    # Specific Linked List Types (Check these BEFORE "linked list")
    # Specific Linked List Types (Check these BEFORE "linked list")
    # specific types must check before general "doubly" or "circular" if they overlap strings
    if "circular doubly" in name_lower:
        return {"name": "Circular Doubly Linked List", "description": "CDLL Visualizer", "visualizer_code": CIRCULAR_DOUBLY_LINKED_LIST_VISUALIZER}
    elif "doubly" in name_lower and "linked" in name_lower:
        return {"name": "Doubly Linked List", "description": "Doubly Linked List Visualizer", "visualizer_code": DOUBLY_LINKED_LIST_VISUALIZER}
    elif "circular" in name_lower and "linked" in name_lower:
        return {"name": "Circular Linked List", "description": "Circular Linked List Visualizer", "visualizer_code": CIRCULAR_LINKED_LIST_VISUALIZER}
    elif "skip" in name_lower:
        return {"name": "Skip List", "description": "Skip List Visualizer", "visualizer_code": SKIP_LIST_VISUALIZER}
    elif "unrolled" in name_lower:
        return {"name": "Unrolled Linked List", "description": "Unrolled LL Visualizer", "visualizer_code": UNROLLED_LINKED_LIST_VISUALIZER}
    elif "xor" in name_lower:
        return {"name": "XOR Linked List", "description": "XOR Linked List Visualizer", "visualizer_code": XOR_LINKED_LIST_VISUALIZER}
    
    # Generic Linked List (Fallback for "linked list" or "singly linked list")
    elif "linked list" in name_lower:
        return {
            "name": "Singly Linked List",
            "description": "Interactive Singly Linked List visualizer",
            "visualizer_code": LINKED_LIST_VISUALIZER
        }
    
    # Arrays
    elif "dynamic" in name_lower and "array" in name_lower:
        return {"name": "Dynamic Array", "description": "Dynamic Array (Vector)", "visualizer_code": DYNAMIC_ARRAY_VISUALIZER}
    elif "sparse" in name_lower:
        return {"name": "Sparse Array", "description": "Sparse Array", "visualizer_code": SPARSE_ARRAY_VISUALIZER}
    elif "jagged" in name_lower:
        return {"name": "Jagged Array", "description": "Jagged Array", "visualizer_code": JAGGED_ARRAY_VISUALIZER}
    elif "circular array" in name_lower:
        return {"name": "Circular Array", "description": "Circular Array/Buffer", "visualizer_code": CIRCULAR_ARRAY_VISUALIZER}
    elif "array" in name_lower:
        return {"name": "Array", "description": "Basic Array Visualizer", "visualizer_code": ARRAY_VISUALIZER}
    
    # Trees
    elif "bst" in name_lower or "binary search tree" in name_lower:
        return {"name": "Binary Search Tree", "description": "BST Visualizer", "visualizer_code": BST_VISUALIZER}
    elif "avl" in name_lower:
        return {"name": "AVL Tree", "description": "AVL Tree Visualizer", "visualizer_code": AVL_TREE_VISUALIZER}
    elif "red-black" in name_lower:
        return {"name": "Red-Black Tree", "description": "RB Tree Visualizer", "visualizer_code": RED_BLACK_TREE_VISUALIZER}
    elif "splay" in name_lower:
        return {"name": "Splay Tree", "description": "Splay Tree Visualizer", "visualizer_code": SPLAY_TREE_VISUALIZER}
    elif "treap" in name_lower:
        return {"name": "Treap", "description": "Treap Visualizer", "visualizer_code": TREAP_VISUALIZER}
    elif "scapegoat" in name_lower:
        return {"name": "Scapegoat Tree", "description": "Scapegoat Tree Visualizer", "visualizer_code": SCAPEGOAT_TREE_VISUALIZER}
    elif "b+" in name_lower or "b plus" in name_lower:
        return {"name": "B+ Tree", "description": "B+ Tree Visualizer", "visualizer_code": B_PLUS_TREE_VISUALIZER}
    elif "b*" in name_lower or "b star" in name_lower:
        return {"name": "B* Tree", "description": "B* Tree Visualizer", "visualizer_code": B_STAR_TREE_VISUALIZER}
    elif "b-tree" in name_lower or "b tree" in name_lower:
        return {"name": "B-Tree", "description": "B-Tree Visualizer", "visualizer_code": B_TREE_VISUALIZER}
    elif "binary tree" in name_lower:
        # Fallback for generic binary tree
        return {"name": "Binary Tree", "description": "General Binary Tree", "visualizer_code": BST_VISUALIZER}
    elif "general tree" in name_lower or "n-ary" in name_lower:
        return {"name": "General Tree", "description": "N-ary Tree Visualizer", "visualizer_code": GENERAL_TREE_VISUALIZER}

    # Heaps
    elif "min heap" in name_lower:
        return {"name": "Min Heap", "description": "Min Heap Visualizer", "visualizer_code": HEAP_VISUALIZER} # Note: Add script to auto-set mode?
    elif "max heap" in name_lower:
        return {"name": "Max Heap", "description": "Max Heap Visualizer", "visualizer_code": HEAP_VISUALIZER}
    elif "fibonacci" in name_lower:
        return {"name": "Fibonacci Heap", "description": "Fibonacci Heap", "visualizer_code": FIBONACCI_HEAP_VISUALIZER}
    elif "binomial" in name_lower:
        return {"name": "Binomial Heap", "description": "Binomial Heap", "visualizer_code": BINOMIAL_HEAP_VISUALIZER}
    elif "pairing" in name_lower:
        return {"name": "Pairing Heap", "description": "Pairing Heap", "visualizer_code": PAIRING_HEAP_VISUALIZER}
    
    # Graphs
    # Catch-all for graphs, we can customize description based on request, but code is same
    elif "graph" in name_lower or "adjacency" in name_lower or "edge list" in name_lower:
        mode_desc = "Unified Graph Visualizer"
        if "directed" in name_lower: mode_desc += " (Directed Mode)"
        if "weighted" in name_lower: mode_desc += " (Weighted Mode)"
        return {"name": "Graph", "description": mode_desc, "visualizer_code": UNIFIED_GRAPH_VISUALIZER}
    
    return None
