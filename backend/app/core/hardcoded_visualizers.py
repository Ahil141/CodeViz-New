"""
Hardcoded visualizers for common data structures.
Used as reliable fallbacks when the AI-generated HTML crashes or is unavailable.
HTML style matches the training data in train_data_final.jsonl.
"""

_STACK_HTML = """<!DOCTYPE html>
<html>
<head>
<style>
    body { font-family: sans-serif; text-align: center; background: #fffcf0; margin: 0; padding: 10px; }
    h1 { font-size: 1.4em; margin-bottom: 8px; }
    .controls { margin-bottom: 10px; }
    input { padding: 6px 10px; border: 1px solid #ccc; border-radius: 4px; width: 120px; }
    button { padding: 6px 14px; margin: 0 4px; border: none; border-radius: 4px; background: #4f46e5; color: #fff; cursor: pointer; font-size: 0.9em; }
    button:hover { background: #4338ca; }
    #stack-container {
        display: flex;
        flex-direction: column-reverse;
        align-items: center;
        min-height: 300px;
        border: 2px solid #4f46e5;
        border-radius: 0 0 8px 8px;
        width: 200px;
        margin: 10px auto 0;
        padding: 8px;
        background: #fff;
        position: relative;
    }
    .stack-item {
        width: 180px;
        padding: 10px 0;
        background: #ffcc00;
        border: 1px solid #e6b800;
        border-radius: 4px;
        margin: 3px 0;
        font-weight: bold;
        font-size: 1em;
        animation: slideIn 0.2s ease;
    }
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(-10px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    #empty-label {
        color: #aaa;
        position: absolute;
        bottom: 50%;
        transform: translateY(50%);
        font-size: 0.9em;
    }
    #status { margin-top: 10px; color: #555; font-size: 0.9em; min-height: 20px; }
</style>
</head>
<body>
    <h1>Stack (LIFO)</h1>
    <div class="controls">
        <input id="val" type="text" placeholder="Value">
        <button onclick="push()">Push</button>
        <button onclick="pop()">Pop</button>
        <button onclick="peek()">Peek</button>
    </div>
    <div id="stack-container">
        <span id="empty-label">Stack is empty</span>
    </div>
    <div id="status"></div>

    <script>
        let stack = [];

        function updateDisplay() {
            const container = document.getElementById('stack-container');
            const emptyLabel = document.getElementById('empty-label');
            // Remove all items
            const items = container.querySelectorAll('.stack-item');
            items.forEach(i => i.remove());

            if (stack.length === 0) {
                emptyLabel.style.display = 'block';
            } else {
                emptyLabel.style.display = 'none';
                stack.forEach(function(val) {
                    const div = document.createElement('div');
                    div.className = 'stack-item';
                    div.textContent = val;
                    container.appendChild(div);
                });
            }
        }

        function setStatus(msg) {
            document.getElementById('status').textContent = msg;
        }

        function push() {
            const input = document.getElementById('val');
            const v = input.value.trim();
            if (!v) { setStatus('Please enter a value.'); return; }
            stack.push(v);
            input.value = '';
            updateDisplay();
            setStatus('Pushed: ' + v + '  |  Size: ' + stack.length);
        }

        function pop() {
            if (stack.length === 0) { setStatus('Stack is empty — nothing to pop.'); return; }
            const v = stack.pop();
            updateDisplay();
            setStatus('Popped: ' + v + '  |  Size: ' + stack.length);
        }

        function peek() {
            if (stack.length === 0) { setStatus('Stack is empty — nothing to peek.'); return; }
            setStatus('Top element: ' + stack[stack.length - 1]);
        }

        updateDisplay();
    </script>
</body>
</html>"""

_QUEUE_HTML = """<!DOCTYPE html>
<html>
<head>
<style>
    body { font-family: sans-serif; text-align: center; background: #fffcf0; margin: 0; padding: 10px; }
    h1 { font-size: 1.4em; margin-bottom: 8px; }
    .controls { margin-bottom: 10px; }
    input { padding: 6px 10px; border: 1px solid #ccc; border-radius: 4px; width: 120px; }
    button { padding: 6px 14px; margin: 0 4px; border: none; border-radius: 4px; background: #059669; color: #fff; cursor: pointer; font-size: 0.9em; }
    button:hover { background: #047857; }
    #queue-wrapper {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 14px;
    }
    #labels {
        display: flex;
        width: 520px;
        justify-content: space-between;
        font-size: 0.8em;
        color: #666;
        margin-bottom: 2px;
        padding: 0 4px;
    }
    #queue-container {
        display: flex;
        flex-direction: row;
        align-items: center;
        min-width: 520px;
        min-height: 60px;
        border: 2px solid #059669;
        border-radius: 8px;
        padding: 8px;
        background: #fff;
        gap: 6px;
    }
    .queue-item {
        min-width: 60px;
        padding: 12px 8px;
        background: #ffcc00;
        border: 1px solid #e6b800;
        border-radius: 4px;
        font-weight: bold;
        font-size: 1em;
        text-align: center;
        animation: slideIn 0.2s ease;
    }
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(10px); }
        to   { opacity: 1; transform: translateX(0); }
    }
    #empty-label { color: #aaa; font-size: 0.9em; }
    #status { margin-top: 10px; color: #555; font-size: 0.9em; min-height: 20px; }
</style>
</head>
<body>
    <h1>Queue (FIFO)</h1>
    <div class="controls">
        <input id="val" type="text" placeholder="Value">
        <button onclick="enqueue()">Enqueue</button>
        <button onclick="dequeue()">Dequeue</button>
        <button onclick="front()">Front</button>
    </div>
    <div id="queue-wrapper">
        <div id="labels"><span>&#8592; Dequeue (front)</span><span>Enqueue (rear) &#8594;</span></div>
        <div id="queue-container">
            <span id="empty-label">Queue is empty</span>
        </div>
    </div>
    <div id="status"></div>

    <script>
        let queue = [];

        function updateDisplay() {
            const container = document.getElementById('queue-container');
            const emptyLabel = document.getElementById('empty-label');
            const items = container.querySelectorAll('.queue-item');
            items.forEach(i => i.remove());

            if (queue.length === 0) {
                emptyLabel.style.display = 'inline';
            } else {
                emptyLabel.style.display = 'none';
                queue.forEach(function(val) {
                    const div = document.createElement('div');
                    div.className = 'queue-item';
                    div.textContent = val;
                    container.appendChild(div);
                });
            }
        }

        function setStatus(msg) {
            document.getElementById('status').textContent = msg;
        }

        function enqueue() {
            const input = document.getElementById('val');
            const v = input.value.trim();
            if (!v) { setStatus('Please enter a value.'); return; }
            queue.push(v);
            input.value = '';
            updateDisplay();
            setStatus('Enqueued: ' + v + '  |  Size: ' + queue.length);
        }

        function dequeue() {
            if (queue.length === 0) { setStatus('Queue is empty — nothing to dequeue.'); return; }
            const v = queue.shift();
            updateDisplay();
            setStatus('Dequeued: ' + v + '  |  Size: ' + queue.length);
        }

        function front() {
            if (queue.length === 0) { setStatus('Queue is empty.'); return; }
            setStatus('Front element: ' + queue[0]);
        }

        updateDisplay();
    </script>
</body>
</html>"""

_LINKED_LIST_HTML = """<!DOCTYPE html>
<html>
<head>
<style>
    body { font-family: sans-serif; text-align: center; background: #fffcf0; margin: 0; padding: 10px; }
    h1 { font-size: 1.4em; margin-bottom: 8px; }
    .controls { margin-bottom: 10px; }
    input { padding: 6px 10px; border: 1px solid #ccc; border-radius: 4px; width: 120px; }
    button { padding: 6px 14px; margin: 0 4px; border: none; border-radius: 4px; background: #7c3aed; color: #fff; cursor: pointer; font-size: 0.9em; }
    button:hover { background: #6d28d9; }
    canvas { background: #fff; border: 1px solid #ccc; border-radius: 8px; margin-top: 10px; }
    #status { margin-top: 8px; color: #555; font-size: 0.9em; min-height: 20px; }
</style>
</head>
<body>
    <h1>Singly Linked List</h1>
    <div class="controls">
        <input id="val" type="text" placeholder="Value">
        <button onclick="insertHead()">Insert Head</button>
        <button onclick="insertTail()">Insert Tail</button>
        <button onclick="deleteHead()">Delete Head</button>
    </div>
    <canvas id="c" width="780" height="120"></canvas>
    <div id="status"></div>

    <script>
        let list = [];
        const ctx = document.getElementById('c').getContext('2d');

        function setStatus(msg) { document.getElementById('status').textContent = msg; }

        function insertHead() {
            const v = document.getElementById('val').value.trim();
            if (!v) { setStatus('Please enter a value.'); return; }
            list.unshift(v);
            document.getElementById('val').value = '';
            render();
            setStatus('Inserted ' + v + ' at head.');
        }

        function insertTail() {
            const v = document.getElementById('val').value.trim();
            if (!v) { setStatus('Please enter a value.'); return; }
            list.push(v);
            document.getElementById('val').value = '';
            render();
            setStatus('Inserted ' + v + ' at tail.');
        }

        function deleteHead() {
            if (list.length === 0) { setStatus('List is empty.'); return; }
            const v = list.shift();
            render();
            setStatus('Deleted head: ' + v);
        }

        function render() {
            ctx.clearRect(0, 0, 780, 120);
            if (list.length === 0) {
                ctx.fillStyle = '#aaa';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.font = '14px sans-serif';
                ctx.fillText('List is empty', 390, 60);
                return;
            }
            const nodeW = 70, nodeH = 40, arrowW = 30;
            const totalW = list.length * nodeW + (list.length - 1) * arrowW;
            let startX = Math.max(10, (780 - totalW) / 2);
            const y = 40;

            list.forEach(function(val, i) {
                const x = startX + i * (nodeW + arrowW);
                // Node box
                ctx.strokeStyle = '#7c3aed';
                ctx.lineWidth = 2;
                ctx.fillStyle = '#ffcc00';
                ctx.beginPath();
                ctx.roundRect(x, y, nodeW, nodeH, 6);
                ctx.fill();
                ctx.stroke();
                // Value
                ctx.fillStyle = '#000';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.font = 'bold 14px sans-serif';
                ctx.fillText(String(val), x + nodeW / 2, y + nodeH / 2);
                // Arrow to next
                if (i < list.length - 1) {
                    const ax = x + nodeW, ay = y + nodeH / 2;
                    ctx.beginPath();
                    ctx.moveTo(ax, ay);
                    ctx.lineTo(ax + arrowW - 8, ay);
                    ctx.strokeStyle = '#555';
                    ctx.lineWidth = 1.5;
                    ctx.stroke();
                    // Arrowhead
                    ctx.beginPath();
                    ctx.moveTo(ax + arrowW - 8, ay);
                    ctx.lineTo(ax + arrowW - 14, ay - 5);
                    ctx.lineTo(ax + arrowW - 14, ay + 5);
                    ctx.closePath();
                    ctx.fillStyle = '#555';
                    ctx.fill();
                } else {
                    // NULL pointer
                    ctx.fillStyle = '#aaa';
                    ctx.font = '11px sans-serif';
                    ctx.textAlign = 'left';
                    ctx.fillText('NULL', x + nodeW + 5, y + nodeH / 2 + 1);
                }
            });
        }

        render();
    </script>
</body>
</html>"""

_HEAP_HTML = """<!DOCTYPE html>
<html>
<head>
<style>
    body { font-family: sans-serif; text-align: center; }
    canvas { background: #fffcf0; border: 1px solid #ccc; }
</style>
</head>
<body>
    <h1>Binary Heap (Priority Queue)</h1>
    <div>
        <button onclick="setMode('min')">Min Heap Mode</button>
        <button onclick="setMode('max')">Max Heap Mode</button>
        <span id="mode-label" style="font-weight:bold; margin-left:10px;">Current: Min Heap</span>
    </div>
    <br>
    <input id="val" type="number" placeholder="Number">
    <button onclick="insert()">Insert</button>
    <button onclick="extract()">Extract Root</button>
    <br><br>
    <canvas id="c" width="800" height="500"></canvas>
    <script>
        let heap = [];
        let isMin = true;
        const ctx = document.getElementById('c').getContext('2d');

        function setMode(m) {
            isMin = (m === 'min');
            document.getElementById('mode-label').textContent = "Current: " + (isMin ? "Min Heap" : "Max Heap");
            heap = []; render();
        }

        function cmp(a, b) { return isMin ? a < b : a > b; }

        function insert() {
            const v = parseInt(document.getElementById('val').value);
            if(isNaN(v)) return;
            heap.push(v);
            bubbleUp(heap.length - 1);
            document.getElementById('val').value = '';
            render();
        }

        function extract() {
            if(heap.length === 0) return;
            const root = heap[0];
            const end = heap.pop();
            if(heap.length > 0) { heap[0] = end; bubbleDown(0); }
            alert("Extracted: " + root);
            render();
        }

        function bubbleUp(n) {
            let element = heap[n];
            while(n > 0) {
                let pIdx = Math.floor((n + 1) / 2) - 1;
                let parent = heap[pIdx];
                if(cmp(element, parent)) { heap[pIdx] = element; heap[n] = parent; n = pIdx; }
                else break;
            }
        }

        function bubbleDown(n) {
            const len = heap.length;
            const element = heap[n];
            while(true) {
                let lChildIdx = 2*n+1, rChildIdx = 2*n+2, lChild, rChild, swapIdx = null;
                if(lChildIdx < len) { lChild = heap[lChildIdx]; if(cmp(lChild, element)) swapIdx = lChildIdx; }
                if(rChildIdx < len) { rChild = heap[rChildIdx]; if(cmp(rChild, (swapIdx === null ? element : lChild))) swapIdx = rChildIdx; }
                if(swapIdx === null) break;
                heap[n] = heap[swapIdx]; heap[swapIdx] = element; n = swapIdx;
            }
        }

        function drawNode(idx, x, y, offset) {
            if(idx >= heap.length) return;
            if(2*idx+1 < heap.length) {
                ctx.beginPath(); ctx.moveTo(x, y+20); ctx.lineTo(x-offset, y+80-20); ctx.stroke();
                drawNode(2*idx+1, x-offset, y+80, offset/2);
            }
            if(2*idx+2 < heap.length) {
                ctx.beginPath(); ctx.moveTo(x, y+20); ctx.lineTo(x+offset, y+80-20); ctx.stroke();
                drawNode(2*idx+2, x+offset, y+80, offset/2);
            }
            ctx.beginPath(); ctx.arc(x, y, 20, 0, Math.PI*2);
            ctx.fillStyle = '#ffcc00'; ctx.fill(); ctx.stroke();
            ctx.fillStyle = 'black'; ctx.textAlign='center'; ctx.textBaseline='middle';
            ctx.fillText(heap[idx], x, y);
        }

        function render() { ctx.clearRect(0,0,800,500); drawNode(0, 400, 40, 200); }
    </script>
</body>
</html>"""

_BINARY_TREE_HTML = """<!DOCTYPE html>
<html>
<head>
<style>
    body { font-family: sans-serif; text-align: center; background: #fffcf0; margin: 0; padding: 10px; }
    h1 { font-size: 1.4em; margin-bottom: 8px; }
    .controls { margin-bottom: 10px; }
    input { padding: 6px 10px; border: 1px solid #ccc; border-radius: 4px; width: 100px; }
    button { padding: 6px 14px; margin: 0 4px; border: none; border-radius: 4px; background: #dc2626; color: #fff; cursor: pointer; font-size: 0.9em; }
    button:hover { background: #b91c1c; }
    canvas { background: #fff; border: 1px solid #ccc; border-radius: 8px; }
    #status { margin-top: 8px; color: #555; font-size: 0.9em; min-height: 20px; }
</style>
</head>
<body>
    <h1>Binary Search Tree</h1>
    <div class="controls">
        <input id="val" type="number" placeholder="Number">
        <button onclick="insertNode()">Insert</button>
        <button onclick="clearTree()">Clear</button>
    </div>
    <canvas id="c" width="780" height="400"></canvas>
    <div id="status"></div>

    <script>
        let root = null;
        const ctx = document.getElementById('c').getContext('2d');

        function Node(v) { this.val = v; this.left = null; this.right = null; }

        function insert(node, v) {
            if (!node) return new Node(v);
            if (v < node.val) node.left = insert(node.left, v);
            else if (v > node.val) node.right = insert(node.right, v);
            return node;
        }

        function insertNode() {
            const v = parseInt(document.getElementById('val').value);
            if (isNaN(v)) { document.getElementById('status').textContent = 'Enter a number.'; return; }
            root = insert(root, v);
            document.getElementById('val').value = '';
            document.getElementById('status').textContent = 'Inserted: ' + v;
            render();
        }

        function clearTree() { root = null; render(); document.getElementById('status').textContent = 'Tree cleared.'; }

        function drawTree(node, x, y, offset) {
            if (!node) return;
            if (node.left) {
                ctx.beginPath(); ctx.moveTo(x, y+18); ctx.lineTo(x-offset, y+70-18);
                ctx.strokeStyle='#666'; ctx.lineWidth=1.5; ctx.stroke();
                drawTree(node.left, x-offset, y+70, offset*0.55);
            }
            if (node.right) {
                ctx.beginPath(); ctx.moveTo(x, y+18); ctx.lineTo(x+offset, y+70-18);
                ctx.strokeStyle='#666'; ctx.lineWidth=1.5; ctx.stroke();
                drawTree(node.right, x+offset, y+70, offset*0.55);
            }
            ctx.beginPath(); ctx.arc(x, y, 18, 0, Math.PI*2);
            ctx.fillStyle='#ffcc00'; ctx.fill();
            ctx.strokeStyle='#dc2626'; ctx.lineWidth=2; ctx.stroke();
            ctx.fillStyle='#000'; ctx.textAlign='center'; ctx.textBaseline='middle';
            ctx.font='bold 13px sans-serif';
            ctx.fillText(node.val, x, y);
        }

        function render() {
            ctx.clearRect(0, 0, 780, 400);
            if (!root) {
                ctx.fillStyle='#aaa'; ctx.font='14px sans-serif';
                ctx.textAlign='center'; ctx.textBaseline='middle';
                ctx.fillText('Tree is empty — insert a number', 390, 200);
                return;
            }
            drawTree(root, 390, 30, 180);
        }

        render();
    </script>
</body>
</html>"""

# ─────────────────────────────────────────────────────────────────────────────
# Main export: keyword → {"html": "..."}
# Keys are lowercase. The chat endpoint will check if any key is a substring
# of the lowercased user query.
# ─────────────────────────────────────────────────────────────────────────────
HARDCODED_VISUALIZERS: dict[str, dict] = {
    "stack":        {"html": _STACK_HTML},
    "queue":        {"html": _QUEUE_HTML},
    "linked list":  {"html": _LINKED_LIST_HTML},
    "linkedlist":   {"html": _LINKED_LIST_HTML},
    "heap":         {"html": _HEAP_HTML},
    "binary tree":  {"html": _BINARY_TREE_HTML},
    "bst":          {"html": _BINARY_TREE_HTML},
    "binary search tree": {"html": _BINARY_TREE_HTML},
}
