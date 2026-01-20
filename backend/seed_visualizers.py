import logging
from app.services.rag_service import rag_service

# Sample HTML/CSS/JS for Bubble Sort
bubble_sort_html = """
<div id="visualization-container" style="display: flex; justify-content: center; align-items: end; height: 300px; gap: 5px;"></div>
<button onclick="startSort()">Start Bubble Sort</button>
<div id="status"></div>
"""

bubble_sort_css = """
.bar {
    width: 20px;
    background-color: #3498db;
    transition: height 0.3s, background-color 0.3s;
}
.sorted { background-color: #2ecc71; }
.comparing { background-color: #e74c3c; }
"""

bubble_sort_js = """
const container = document.getElementById('visualization-container');
const status = document.getElementById('status');
let array = Array.from({length: 15}, () => Math.floor(Math.random() * 250) + 10);

function render() {
    container.innerHTML = '';
    array.forEach(val => {
        const bar = document.createElement('div');
        bar.className = 'bar';
        bar.style.height = val + 'px';
        container.appendChild(bar);
    });
}

async function startSort() {
    const bars = document.getElementsByClassName('bar');
    for (let i = 0; i < array.length; i++) {
        for (let j = 0; j < array.length - i - 1; j++) {
            bars[j].classList.add('comparing');
            bars[j+1].classList.add('comparing');
            
            if (array[j] > array[j+1]) {
                await new Promise(r => setTimeout(r, 100));
                let temp = array[j];
                array[j] = array[j+1];
                array[j+1] = temp;
                bars[j].style.height = array[j] + 'px';
                bars[j+1].style.height = array[j+1] + 'px';
            }
            
            bars[j].classList.remove('comparing');
            bars[j+1].classList.remove('comparing');
        }
        bars[array.length - i - 1].classList.add('sorted');
    }
    status.innerText = 'Sorted!';
}

render();
"""

def seed():
    print("Seeding RAG with Visualization Code...")
    
    # Construct the document content ensuring it contains the explicit code blocks
    # which the extraction logic in chat.py looks for (```html etc) OR
    # just plain text that startwith/contains keywords?
    # actually chat.py fallback logic looks for ```code``` IN THE LLM RESPONSE.
    # But for RAG, it looks for `doc.startswith("{")` or `"class "` or `"def "`.
    # Wait, the current chat.py logic for RAG is:
    # `if doc.startswith("{") or "class " in doc or "def " in doc:`
    # This is for Python/JSON. 
    # BUT, the generic fallback generates HTML.
    
    # Implementation Plan:
    # 1. We want the RAG to return the HTML/CSS/JS code.
    # 2. We need to update chat.py to also recognize HTML/CSS/JS in RAG docs.
    # 3. Then we seed this content.
    
    
    # ---------------------------------------------------------
    # Stack Visualization
    # ---------------------------------------------------------
    stack_html = """
    <div id="stack-container" style="display: flex; flex-direction: column-reverse; width: 100px; min-height: 200px; border: 2px solid #333; border-top: none; margin: 20px auto; padding: 5px;"></div>
    <div style="text-align: center; gap: 10px; display: flex; justify-content: center;">
        <input type="text" id="stackInput" placeholder="Value" style="width: 60px; padding: 5px;">
        <button onclick="push()">Push</button>
        <button onclick="pop()">Pop</button>
        <button onclick="peek()">Peek</button>
    </div>
    <div id="message" style="text-align: center; margin-top: 10px; height: 20px; color: #555;"></div>
    """
    
    stack_css = """
    .stack-item {
        width: 90%;
        height: 30px;
        background-color: #3498db;
        color: white;
        margin: 2px auto;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 4px;
        animation: slideIn 0.3s ease-out;
    }
    @keyframes slideIn {
        from { transform: translateY(-20px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    .popping {
        animation: fadeOut 0.3s ease-out forwards;
    }
    @keyframes fadeOut {
        to { transform: translateY(-20px); opacity: 0; }
    }
    """
    
    stack_js = """
    const stackContainer = document.getElementById('stack-container');
    const message = document.getElementById('message');
    const input = document.getElementById('stackInput');
    const stack = [];
    
    function render() {
        stackContainer.innerHTML = '';
        stack.forEach(val => {
            const item = document.createElement('div');
            item.className = 'stack-item';
            item.innerText = val;
            stackContainer.appendChild(item);
        });
    }
    
    function push() {
        const val = input.value;
        if (!val) return;
        if (stack.length >= 6) {
            msg("Stack Overflow!");
            return;
        }
        stack.push(val);
        input.value = '';
        render();
        msg(`Pushed ${val}`);
    }
    
    async function pop() {
        if (stack.length === 0) {
            msg("Stack Underflow!");
            return;
        }
        const val = stack[stack.length - 1];
        
        // Visual effect for popping (optional simple implementation without async for now to match raw HTML style)
        // But let's try to grab the last child
        if (stackContainer.lastChild) {
            stackContainer.lastChild.classList.add('popping');
            await new Promise(r => setTimeout(r, 300));
        }
        
        stack.pop();
        render();
        msg(`Popped ${val}`);
    }
    
    function peek() {
        if (stack.length === 0) {
            msg("Stack is Empty");
        } else {
            msg(`Top is ${stack[stack.length - 1]}`);
        }
    }
    
    function msg(text) {
        message.innerText = text;
        setTimeout(() => message.innerText = '', 2000);
    }
    """
    
    bubble_content = f"""
    Here is the interactive visualization for Bubble Sort.
    
    ```html
    {bubble_sort_html}
    ```
    
    ```css
    {bubble_sort_css}
    ```
    
    ```javascript
    {bubble_sort_js}
    ```
    """
    
    stack_content = f"""
    Here is the interactive visualization for a Stack data structure.
    
    ```html
    {stack_html}
    ```
    
    ```css
    {stack_css}
    ```
    
    ```javascript
    {stack_js}
    ```
    """
    
    print("Adding documents...")

    # ---------------------------------------------------------
    # Linked List Visualization
    # ---------------------------------------------------------
    ll_html = """
    <div id="ll-container" style="display: flex; align-items: center; gap: 10px; padding: 20px; overflow-x: auto;"></div>
    <div style="margin-top: 20px; display: flex; gap: 10px; justify-content: center;">
        <input type="number" id="llInput" placeholder="Value" style="width: 60px; padding: 5px;">
        <button onclick="appendNode()">Append</button>
        <button onclick="prependNode()">Prepend</button>
        <button onclick="removeFirst()">Remove First</button>
    </div>
    <div id="ll-message" style="text-align: center; margin-top: 10px; color: #555; height: 20px;"></div>
    """

    ll_css = """
    .node {
        display: flex;
        align-items: center;
        animation: fadeIn 0.5s;
    }
    .node-content {
        min-width: 40px;
        height: 40px;
        background: #3498db;
        color: white;
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        font-weight: bold;
        position: relative;
    }
    .arrow {
        font-size: 24px;
        color: #555;
        margin: 0 5px;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateX(-10px); }
        to { opacity: 1; transform: translateX(0); }
    }
    """

    ll_js = """
    const container = document.getElementById('ll-container');
    const msgBox = document.getElementById('ll-message');
    let list = [];

    function render() {
        container.innerHTML = '';
        list.forEach((val, index) => {
            const node = document.createElement('div');
            node.className = 'node';
            
            const content = document.createElement('div');
            content.className = 'node-content';
            content.innerText = val;
            node.appendChild(content);

            if (index < list.length - 1) {
                const arrow = document.createElement('span');
                arrow.className = 'arrow';
                arrow.innerHTML = '&#8594;';
                node.appendChild(arrow);
            }
            
            container.appendChild(node);
        });
        if (list.length === 0) {
            container.innerHTML = '<div style="color: #aaa; font-style: italic;">Empty List</div>';
        }
    }

    function appendNode() {
        const val = document.getElementById('llInput').value;
        if (!val) return;
        list.push(val);
        document.getElementById('llInput').value = '';
        render();
        msg("Appended " + val);
    }

    function prependNode() {
        const val = document.getElementById('llInput').value;
        if (!val) return;
        list.unshift(val);
        document.getElementById('llInput').value = '';
        render();
        msg("Prepended " + val);
    }

    function removeFirst() {
        if (list.length === 0) {
            msg("List is empty!");
            return;
        }
        const val = list.shift();
        render();
        msg("Removed " + val);
    }

    function msg(txt) {
        msgBox.innerText = txt;
        setTimeout(() => msgBox.innerText = '', 2000);
    }
    render();
    """

    # ---------------------------------------------------------
    # Doubly Linked List Visualization
    # ---------------------------------------------------------
    dll_html = """
    <div id="dll-container" style="display: flex; align-items: center; gap: 5px; padding: 20px; overflow-x: auto;"></div>
    <div style="margin-top: 20px; display: flex; gap: 10px; justify-content: center;">
        <input type="number" id="dllInput" placeholder="Value" style="width: 60px; padding: 5px;">
        <button onclick="dllAppend()">Append</button>
        <button onclick="dllRemoveLast()">Remove Last</button>
    </div>
    """

    dll_css = """
    .d-node {
        display: flex;
        align-items: center;
        animation: scaleIn 0.3s;
    }
    .d-content {
        width: 50px;
        height: 30px;
        background: #9b59b6;
        color: white;
        display: flex;
        justify-content: center;
        align-items: center;
        border: 2px solid #8e44ad;
        border-radius: 4px;
    }
    .d-arrows {
        font-size: 20px;
        color: #555;
        margin: 0 5px;
        letter-spacing: -2px;
    }
    @keyframes scaleIn {
        from { transform: scale(0.5); opacity: 0; }
        to { transform: scale(1); opacity: 1; }
    }
    """

    dll_js = """
    const dContainer = document.getElementById('dll-container');
    let dll = [];

    function renderDLL() {
        dContainer.innerHTML = '';
        dll.forEach((val, index) => {
            const node = document.createElement('div');
            node.className = 'd-node';
            
            const content = document.createElement('div');
            content.className = 'd-content';
            content.innerText = val;
            node.appendChild(content);

            if (index < dll.length - 1) {
                const arrows = document.createElement('span');
                arrows.className = 'd-arrows';
                arrows.innerHTML = '&#8646;'; // Left-Right Arrow
                node.appendChild(arrows);
            }
            dContainer.appendChild(node);
        });
        if (dll.length === 0) dContainer.innerHTML = 'Empty';
    }

    function dllAppend() {
        const val = document.getElementById('dllInput').value;
        if (!val) return;
        dll.push(val);
        document.getElementById('dllInput').value = '';
        renderDLL();
    }
    
    function dllRemoveLast() {
        if(dll.length === 0) return;
        dll.pop();
        renderDLL();
    }
    renderDLL();
    """

    # ---------------------------------------------------------
    # Queue Visualization
    # ---------------------------------------------------------
    queue_html = """
    <div style="display: flex; align-items: center; gap: 10px;">
        <div style="font-weight: bold; color: #555;">Front</div>
        <div id="q-container" style="display: flex; gap: 5px; padding: 10px; border: 2px dashed #ccc; min-height: 50px; min-width: 200px; align-items: center;"></div>
        <div style="font-weight: bold; color: #555;">Rear</div>
    </div>
    <div style="margin-top: 20px; display: flex; gap: 10px; justify-content: center;">
        <input type="text" id="qInput" placeholder="Item" style="width: 80px; padding: 5px;">
        <button onclick="enqueue()">Enqueue</button>
        <button onclick="dequeue()">Dequeue</button>
    </div>
    <div id="q-msg" style="text-align: center; margin-top: 10px; color: #555;"></div>
    """
    
    queue_css = """
    .q-item {
        padding: 10px 15px;
        background: #e67e22;
        color: white;
        border-radius: 4px;
        animation: slideLeft 0.3s;
    }
    @keyframes slideLeft {
        from { transform: translateX(20px); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    .dequeuing {
        animation: fadeOutUp 0.3s forwards;
    }
    @keyframes fadeOutUp {
        to { transform: translateY(-20px); opacity: 0; }
    }
    """
    
    queue_js = """
    const qContainer = document.getElementById('q-container');
    const qMsg = document.getElementById('q-msg');
    let queue = [];

    function renderQ() {
        qContainer.innerHTML = '';
        queue.forEach(val => {
            const item = document.createElement('div');
            item.className = 'q-item';
            item.innerText = val;
            qContainer.appendChild(item);
        });
        if(queue.length === 0) qContainer.innerHTML = '<span style="color:#ccc">Empty</span>';
    }

    function enqueue() {
        const val = document.getElementById('qInput').value;
        if(!val) return;
        queue.push(val);
        document.getElementById('qInput').value = '';
        renderQ();
        qMsg.innerText = `Enqueued ${val}`;
    }

    async function dequeue() {
        if(queue.length === 0) {
            qMsg.innerText = "Queue Underflow";
            return;
        }
        if(qContainer.firstChild) {
            // Visual effect
            qContainer.firstChild.classList.add('dequeuing');
            await new Promise(r => setTimeout(r, 300));
        }
        const val = queue.shift();
        renderQ();
        qMsg.innerText = `Dequeued ${val}`;
    }
    renderQ();
    """

    # ---------------------------------------------------------
    # Binary Search Tree (BST)
    # ---------------------------------------------------------
    bst_html = """
    <canvas id="bstCanvas" width="600" height="300" style="border:1px solid #eee; display:block; margin: 0 auto;"></canvas>
    <div style="margin-top: 15px; display: flex; gap: 10px; justify-content: center;">
        <input type="number" id="bstInput" placeholder="Num" style="width: 60px;">
        <button onclick="bstInsert()">Insert</button>
        <button onclick="bstClear()">Clear</button>
    </div>
    """

    bst_css = """
    /* Canvas used for rendering */
    """

    bst_js = """
    const canvas = document.getElementById('bstCanvas');
    const ctx = canvas.getContext('2d');
    
    class Node {
        constructor(value) {
            this.value = parseInt(value);
            this.left = null;
            this.right = null;
            this.x = 0;
            this.y = 0;
        }
    }
    
    let root = null;

    function insertNode(node, value) {
        if (!node) return new Node(value);
        if (value < node.value) node.left = insertNode(node.left, value);
        else if (value > node.value) node.right = insertNode(node.right, value);
        return node;
    }

    function bstInsert() {
        const val = document.getElementById('bstInput').value;
        if(!val) return;
        root = insertNode(root, parseInt(val));
        document.getElementById('bstInput').value = '';
        drawTree();
    }
    
    function bstClear() {
        root = null;
        drawTree();
    }

    function drawTree() {
        ctx.clearRect(0,0, canvas.width, canvas.height);
        if(!root) return;
        
        // Calculate positions (simple naive approach)
        const depthHeight = 50;
        
        function setCoords(node, x, y, offset) {
            if(!node) return;
            node.x = x;
            node.y = y;
            setCoords(node.left, x - offset, y + depthHeight, offset / 1.8);
            setCoords(node.right, x + offset, y + depthHeight, offset / 1.8);
        }
        
        setCoords(root, canvas.width / 2, 40, 120);
        
        function drawLines(node) {
            if(!node) return;
            if(node.left) {
                ctx.beginPath();
                ctx.moveTo(node.x, node.y);
                ctx.lineTo(node.left.x, node.left.y);
                ctx.stroke();
                drawLines(node.left);
            }
            if(node.right) {
                ctx.beginPath();
                ctx.moveTo(node.x, node.y);
                ctx.lineTo(node.right.x, node.right.y);
                ctx.stroke();
                drawLines(node.right);
            }
        }
        
        function drawNodes(node) {
            if(!node) return;
            ctx.beginPath();
            ctx.arc(node.x, node.y, 15, 0, 2 * Math.PI);
            ctx.fillStyle = "#27ae60";
            ctx.fill();
            ctx.stroke();
            
            ctx.fillStyle = "white";
            ctx.font = "12px Arial";
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";
            ctx.fillText(node.value, node.x, node.y);
            
            drawNodes(node.left);
            drawNodes(node.right);
        }
        
        ctx.strokeStyle = "#555";
        drawLines(root);
        drawNodes(root);
    }
    // Init with some data
    [10, 5, 15, 3, 7, 12, 18].forEach(v => root = insertNode(root, v));
    drawTree();
    """

    # ---------------------------------------------------------
    # Graph Visualization
    # ---------------------------------------------------------
    graph_html = """
    <div id="graph-area" style="width: 100%; height: 300px; border: 1px solid #ddd; position: relative; overflow: hidden; background: #fafafa;"></div>
    <div style="margin-top: 10px; text-align: center;">
        <button onclick="addRandomNode()">Add Node</button>
        <button onclick="addRandomEdge()">Add Random Edge</button>
        <button onclick="resetGraph()">Reset</button>
    </div>
    """
    
    graph_css = """
    .g-node {
        width: 30px;
        height: 30px;
        background: #e74c3c;
        color: white;
        border-radius: 50%;
        position: absolute;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 12px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        transition: all 0.3s;
        z-index: 2;
    }
    .g-edge {
        position: absolute;
        height: 2px;
        background: #aaa;
        transform-origin: 0 50%;
        z-index: 1;
    }
    """
    
    graph_js = """
    const area = document.getElementById('graph-area');
    let nodes = [];
    let edges = [];
    let nodeIdCounter = 1;

    function addRandomNode() {
        if(nodes.length >= 10) return;
        const id = nodeIdCounter++;
        const x = Math.random() * (area.clientWidth - 40) + 20;
        const y = Math.random() * (area.clientHeight - 40) + 20;
        
        const node = { id, x, y };
        nodes.push(node);
        renderGraph();
    }
    
    function addRandomEdge() {
        if(nodes.length < 2) return;
        const src = nodes[Math.floor(Math.random() * nodes.length)];
        const dest = nodes[Math.floor(Math.random() * nodes.length)];
        
        if(src === dest) return;
        // Check if edge exists
        const exists = edges.find(e => (e.s === src.id && e.d === dest.id) || (e.s === dest.id && e.d === src.id));
        if(!exists) {
            edges.push({ s: src.id, d: dest.id });
            renderGraph();
        }
    }

    function resetGraph() {
        nodes = [];
        edges = [];
        nodeIdCounter = 1;
        renderGraph();
    }

    function renderGraph() {
        area.innerHTML = '';
        
        // Render Edges
        edges.forEach(e => {
            const n1 = nodes.find(n => n.id === e.s);
            const n2 = nodes.find(n => n.id === e.d);
            if(n1 && n2) {
                const dx = n2.x - n1.x;
                const dy = n2.y - n1.y;
                const dist = Math.sqrt(dx*dx + dy*dy);
                const angle = Math.atan2(dy, dx) * 180 / Math.PI;
                
                const line = document.createElement('div');
                line.className = 'g-edge';
                line.style.width = dist + 'px';
                line.style.left = (n1.x + 15) + 'px'; // +15 for center of 30px node
                line.style.top = (n1.y + 15) + 'px';
                line.style.transform = `rotate(${angle}deg)`;
                area.appendChild(line);
            }
        });

        // Render Nodes
        nodes.forEach(n => {
            const el = document.createElement('div');
            el.className = 'g-node';
            el.style.left = n.x + 'px';
            el.style.top = n.y + 'px';
            el.innerText = n.id;
            area.appendChild(el);
        });
    }
    
    // Init
    addRandomNode(); addRandomNode(); addRandomNode();
    addRandomEdge();
    """

    content_templates = {
        "linked_list": [ll_html, ll_css, ll_js, "Linked List"],
        "doubly_linked_list": [dll_html, dll_css, dll_js, "Doubly Linked List"],
        "queue": [queue_html, queue_css, queue_js, "Queue"],
        "bst": [bst_html, bst_css, bst_js, "Binary Search Tree"],
        "graph": [graph_html, graph_css, graph_js, "Graph"]
    }
    
    docs = [bubble_content, stack_content]
    metas = [
        {"type": "visualization", "algo": "bubble_sort"},
        {"type": "visualization", "algo": "stack"}
    ]
    ids_list = ["bubble_sort_vis", "stack_vis"]
    
    for key, (html, css, js, name) in content_templates.items():
        doc = f"""
        Here is the interactive visualization for {name}.
        
        ```html
        {html}
        ```
        
        ```css
        {css}
        ```
        
        ```javascript
        {js}
        ```
        """
        docs.append(doc)
        metas.append({"type": "visualization", "algo": key})
        ids_list.append(f"{key}_vis")

    print("Adding documents...")

    rag_service.add_documents(
        documents=docs,
        metadatas=metas,
        ids=ids_list
    )
    print("Seeded Visualizations: Bubble Sort, Stack, Linked List, DLL, Queue, BST, Graph.")

if __name__ == "__main__":
    seed()
