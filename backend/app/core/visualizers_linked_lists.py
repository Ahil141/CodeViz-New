
# Doubly Linked List Visualizer
DOUBLY_LINKED_LIST_VISUALIZER = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Doubly Linked List Visualizer</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Segoe UI', sans-serif; background: #f0f2f5; padding: 20px; display: flex; flex-direction: column; align-items: center; min-height: 100vh; }
        .controls { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 30px; display: flex; gap: 10px; flex-wrap: wrap; justify-content: center; }
        input { padding: 10px; border: 1px solid #ddd; border-radius: 6px; font-size: 16px; width: 150px; }
        button { padding: 10px 20px; border: none; border-radius: 6px; background: #3b82f6; color: white; cursor: pointer; font-size: 16px; transition: all 0.2s; }
        button:hover { background: #2563eb; }
        .list-container { display: flex; align-items: center; gap: 0; padding: 40px; overflow-x: auto; max-width: 100%; min-height: 200px; background: white; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
        .node { display: flex; align-items: center; animation: popIn 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
        .node-content { display: flex; flex-direction: column; background: linear-gradient(135deg, #6366f1, #8b5cf6); border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .data { padding: 15px 25px; color: white; font-weight: bold; font-size: 18px; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.2); }
        .pointers { display: flex; background: rgba(0,0,0,0.2); }
        .ptr { padding: 5px 10px; font-size: 12px; color: rgba(255,255,255,0.8); width: 50%; text-align: center; }
        .ptr:first-child { border-right: 1px solid rgba(255,255,255,0.1); }
        .arrows { display: flex; flex-direction: column; gap: 5px; margin: 0 10px; color: #64748b; font-weight: bold; font-size: 20px; }
        .arrow-right { transform: scaleX(1); }
        .arrow-left { transform: scaleX(-1); }
        .null-node { font-family: monospace; color: #94a3b8; font-weight: bold; background: #e2e8f0; padding: 10px 15px; border-radius: 6px; }
        @keyframes popIn { from { opacity: 0; transform: scale(0.5); } to { opacity: 1; transform: scale(1); } }
    </style>
</head>
<body>
    <h1>Doubly Linked List</h1>
    <div class="controls">
        <input type="text" id="val" placeholder="Value">
        <button onclick="insertHead()">Insert Head</button>
        <button onclick="insertTail()">Insert Tail</button>
        <button onclick="deleteHead()">Delete Head</button>
        <button onclick="deleteTail()">Delete Tail</button>
    </div>
    <div class="list-container" id="container"></div>

    <script>
        // Simple Doubly Linked List Logic
        let head = null;
        let tail = null;
        
        // Helper to generate ID
        const uuid = () => Math.random().toString(36).substr(2, 9);

        function render() {
            const container = document.getElementById('container');
            container.innerHTML = '';
            
            // Render Null at start
            container.innerHTML += '<div class="null-node">NULL</div>';
            container.innerHTML += '<div class="arrows"><span class="arrow-right">→</span><span class="arrow-left">→</span></div>';
            
            let curr = head;
            while (curr) {
                const nodeHtml = `
                    <div class="node">
                        <div class="node-content">
                            <div class="data">${curr.val}</div>
                            <div class="pointers">
                                <div class="ptr">Prev</div>
                                <div class="ptr">Next</div>
                            </div>
                        </div>
                    </div>
                `;
                container.innerHTML += nodeHtml;
                
                // Add arrows
                container.innerHTML += '<div class="arrows"><span class="arrow-right">→</span><span class="arrow-left">→</span></div>';
                
                curr = curr.next;
            }
            
            // Render Null at end
            container.innerHTML += '<div class="null-node">NULL</div>';
        }

        function insertHead() {
            const val = document.getElementById('val').value.trim();
            if (!val) return;
            const newNode = { val, prev: null, next: null, id: uuid() };
            if (!head) {
                head = tail = newNode;
            } else {
                newNode.next = head;
                head.prev = newNode;
                head = newNode;
            }
            document.getElementById('val').value = '';
            render();
        }

        function insertTail() {
            const val = document.getElementById('val').value.trim();
            if (!val) return;
            const newNode = { val, prev: null, next: null, id: uuid() };
            if (!tail) {
                head = tail = newNode;
            } else {
                tail.next = newNode;
                newNode.prev = tail;
                tail = newNode;
            }
            document.getElementById('val').value = '';
            render();
        }

        function deleteHead() {
            if (!head) return;
            if (head === tail) {
                head = tail = null;
            } else {
                head = head.next;
                head.prev = null;
            }
            render();
        }

        function deleteTail() {
            if (!tail) return;
            if (head === tail) {
                head = tail = null;
            } else {
                tail = tail.prev;
                tail.next = null;
            }
            render();
        }
        
        render();
    </script>
</body>
</html>
"""

# Circular Linked List Visualizer
CIRCULAR_LINKED_LIST_VISUALIZER = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Circular Linked List Visualizer</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'Segoe UI', sans-serif; background: #fff1f2; padding: 20px; display: flex; flex-direction: column; align-items: center; min-height: 100vh; }
        .controls { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 50px; display: flex; gap: 10px; }
        input { padding: 10px; border: 1px solid #ddd; border-radius: 6px; }
        button { padding: 10px 20px; background: #e11d48; color: white; border: none; border-radius: 6px; cursor: pointer; }
        .circle-container { position: relative; width: 400px; height: 400px; margin-top: 20px; }
        .node { position: absolute; width: 80px; height: 80px; background: radial-gradient(circle at 30% 30%, #fb7185, #e11d48); border-radius: 50%; color: white; display: flex; align-items: center; justify-content: center; font-weight: bold; box-shadow: 0 5px 15px rgba(225, 29, 72, 0.4); transition: all 0.5s ease; border: 2px solid white; }
        .connection { position: absolute; height: 2px; background: #e11d48; transform-origin: 0% 50%; z-index: -1; }
        .connection::after { content: '►'; position: absolute; right: -5px; top: -7px; color: #e11d48; font-size: 14px; }
        .empty-msg { position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: #999; }
    </style>
</head>
<body>
    <h1>Circular Linked List</h1>
    <div class="controls">
        <input type="text" id="val" placeholder="Value">
        <button onclick="insert()">Insert</button>
        <button onclick="remove()">Delete Front</button>
    </div>
    <div class="circle-container" id="container"></div>

    <script>
        let nodes = [];
        
        function render() {
            const container = document.getElementById('container');
            container.innerHTML = '';
            if (nodes.length === 0) {
                container.innerHTML = '<div class="empty-msg">List is Empty</div>';
                return;
            }
            
            const radius = 150;
            const cx = 200, cy = 200;
            const angleStep = (2 * Math.PI) / nodes.length;
            
            // Draw connections first
            nodes.forEach((_, i) => {
                const angle = i * angleStep - Math.PI/2;
                const nextAngle = ((i + 1) % nodes.length) * angleStep - Math.PI/2;
                
                const x1 = cx + Math.cos(angle) * (radius - 40); // inner radius
                const y1 = cy + Math.sin(angle) * (radius - 40);
                const x2 = cx + Math.cos(nextAngle) * (radius - 40);
                const y2 = cy + Math.sin(nextAngle) * (radius - 40);
                
                // Simplified SVG or standard div line logic would go here. 
                // For this pure CSS circle demo, we'll just position arrows roughly or skip exact lines.
                // Let's use SVG for lines for better circular visual.
            });

            // Re-doing container to use SVG for lines
            let svgHtml = `<svg width="100%" height="100%" style="position:absolute; top:0; left:0; z-index:0;">`;
            
            nodes.forEach((n, i) => {
                const angle = i * angleStep - Math.PI/2; // Start from top
                const nextAngle = ((i + 1) % nodes.length) * angleStep - Math.PI/2;
                
                const x1 = cx + Math.cos(angle) * radius;
                const y1 = cy + Math.sin(angle) * radius;
                const x2 = cx + Math.cos(nextAngle) * radius;
                const y2 = cy + Math.sin(nextAngle) * radius;
                
                // Draw arrow path
                // Using quadratic curve for smoother connection? Straight lines are fine for polygon shape
                svgHtml += `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="#e11d48" stroke-width="2" marker-end="url(#head)" />`;
            });
            
            svgHtml += `<defs><marker id="head" orient="auto" markerWidth="6" markerHeight="6" refX="25" refY="3"><path d="M0,0 V6 L6,3 Z" fill="#e11d48"/></marker></defs></svg>`;
            container.innerHTML += svgHtml;

            // Draw nodes
            nodes.forEach((n, i) => {
                const angle = i * angleStep - Math.PI/2;
                const x = cx + Math.cos(angle) * radius - 40; // center offset
                const y = cy + Math.sin(angle) * radius - 40;
                
                const div = document.createElement('div');
                div.className = 'node';
                div.textContent = n;
                div.style.left = x + 'px';
                div.style.top = y + 'px';
                container.appendChild(div);
            });
        }

        function insert() {
            const val = document.getElementById('val').value.trim();
            if (!val) return;
            nodes.push(val);
            document.getElementById('val').value = '';
            render();
        }

        function remove() {
            if (nodes.length > 0) nodes.shift();
            render();
        }
        
        render();
    </script>
</body>
</html>
"""

# Circular Doubly Linked List Visualizer
CIRCULAR_DOUBLY_LINKED_LIST_VISUALIZER = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Circular Doubly Linked List</title>
    <!-- Simplified variation of Circular with double arrows -->
    <style>
        /* Styles similar to Circular but with double arrows visual indications */
        body { font-family: sans-serif; text-align: center; padding: 20px; }
        .controls { margin-bottom: 20px; }
        input, button { padding: 10px; font-size: 16px; margin: 5px; }
        #canvas { border: 1px solid #ddd; background: #fafafa; }
    </style>
</head>
<body>
    <h1>Circular Doubly Linked List</h1>
    <div class="controls">
        <input id="val" placeholder="Value">
        <button onclick="add()">Add Node</button>
        <button onclick="del()">Delete Last</button>
    </div>
    <canvas id="canvas" width="600" height="400"></canvas>
    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        let data = [];

        function render() {
            ctx.clearRect(0,0,600,400);
            if(data.length === 0) {
                ctx.fillText("Empty List", 280, 200);
                return;
            }
            
            const cx = 300, cy = 200, r = 120;
            const step = (Math.PI*2)/data.length;
            
            // Draw Links
            ctx.beginPath();
            ctx.strokeStyle = '#007bff';
            ctx.lineWidth = 2;
            for(let i=0; i<data.length; i++) {
                const angle = i*step;
                const nextAngle = ((i+1)%data.length)*step;
                const x1 = cx + Math.cos(angle)*r;
                const y1 = cy + Math.sin(angle)*r;
                const x2 = cx + Math.cos(nextAngle)*r;
                const y2 = cy + Math.sin(nextAngle)*r;
                ctx.moveTo(x1, y1);
                ctx.lineTo(x2, y2);
            }
            ctx.stroke();

            // Draw Nodes
            for(let i=0; i<data.length; i++) {
                const angle = i*step;
                const x = cx + Math.cos(angle)*r;
                const y = cy + Math.sin(angle)*r;
                
                ctx.beginPath();
                ctx.arc(x, y, 25, 0, Math.PI*2);
                ctx.fillStyle = 'white';
                ctx.fill();
                ctx.stroke();
                
                ctx.fillStyle = 'black';
                ctx.font = '14px Arial';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(data[i], x, y);
            }
            
            ctx.fillStyle = '#666';
            ctx.fillText("Arrows imply both directions (Next & Prev)", 300, 380);
        }

        function add() {
            const v = document.getElementById('val').value;
            if(v) { data.push(v); document.getElementById('val').value=''; render(); }
        }
        function del() {
            data.pop(); render();
        }
        render();
    </script>
</body>
</html>"""

# Skip List Visualizer
SKIP_LIST_VISUALIZER = """<!DOCTYPE html>
<html>
<head>
    <title>Skip List Logic</title>
    <style>
        body { padding: 20px; font-family: sans-serif; }
        .level { display: flex; align-items: center; margin-bottom: 20px; position: relative; }
        .level-label { width: 60px; font-weight: bold; }
        .node { 
            width: 50px; height: 50px; border: 2px solid #333; 
            margin-right: 20px; display: flex; align-items: center; 
            justify-content: center; background: white; z-index: 2;
        }
        .line { position: absolute; height: 2px; background: #999; z-index: 1; width: 100%; top: 25px; }
        .col-lines { position:absolute; border-left: 2px dashed #ddd; }
    </style>
</head>
<body>
    <h1>Skip List</h1>
    <div style="margin-bottom:20px;">
        <input id="val" type="number" placeholder="Number">
        <button onclick="insert()">Insert</button>
        <button onclick="reset()">Clear</button>
    </div>
    <div id="container"></div>
    <script>
        let head = { val: -Infinity, next: [], bottom: null }; 
        // Logic simplified: We'll just visualize a static-like structure for demo
        // Implementing full probabilistic skip list in vanilla JS for visualization is complex,
        // we will simulate levels.
        
        let values = [];

        function render() {
            // Sort values
            const sorted = [...values].sort((a,b)=>a-b);
            const container = document.getElementById('container');
            container.innerHTML = '';
            
            // Generate random levels for each value
            // (Deterministic for visual stability in this demo)
            const levels = sorted.map(v => {
                let l = 1;
                while(Math.random() > 0.5 && l < 4) l++;
                return { v, l };
            });
            
            const maxLvl = levels.length ? Math.max(...levels.map(x=>x.l)) : 1;
            
            for(let i = maxLvl; i >= 1; i--) {
                const lvlDiv = document.createElement('div');
                lvlDiv.className = 'level';
                lvlDiv.innerHTML = `<div class="level-label">L${i}</div><div class="line"></div>`;
                
                // Head
                lvlDiv.innerHTML += `<div class="node" style="background:#eee;">HEAD</div>`;
                
                // Items that exist at this level
                levels.forEach(item => {
                    if(item.l >= i) {
                        lvlDiv.innerHTML += `<div class="node">${item.v}</div>`;
                    } else {
                        // Spacer
                        lvlDiv.innerHTML += `<div class="node" style="border:none; background:transparent;"></div>`;
                    }
                });
                
                // Tail
                lvlDiv.innerHTML += `<div class="node" style="background:#eee;">NIL</div>`;
                
                container.appendChild(lvlDiv);
            }
        }

        function insert() {
            const v = parseInt(document.getElementById('val').value);
            if(!isNaN(v) && !values.includes(v)) {
                values.push(v);
                render();
            }
            document.getElementById('val').value = '';
        }
        function reset() { values = []; render(); }
        render();
    </script>
</body>
</html>"""

# Unrolled Linked List
UNROLLED_LINKED_LIST_VISUALIZER = """<!DOCTYPE html>
<html>
<head>
<title>Unrolled LL</title>
<style>
    body { font-family: monospace; padding: 20px; }
    .node { 
        border: 2px solid #000; padding: 10px; margin: 10px; 
        display: inline-block; vertical-align: top; width: 120px;
        background: #f0f0f0; border-radius: 5px;
    }
    .array-slot { border: 1px solid #aaa; padding: 5px; background: white; text-align: center; margin-bottom: 2px;}
    .next-ptr { margin-top: 5px; font-size: 12px; text-align: center; color: red; }
    .arrow { display: inline-block; padding: 30px 5px; vertical-align: top; color: blue; font-size: 20px; }
</style>
</head>
<body>
    <h1>Unrolled Linked List</h1>
    <p>Each node holds an array of up to 4 elements.</p>
    <div style="margin-bottom:10px;">
        <input id="val" placeholder="Value">
        <button onclick="add()">Add</button>
    </div>
    <div id="container"></div>
    <script>
        const capacity = 4;
        let nodes = [ [] ]; // Array of arrays

        function render() {
            const c = document.getElementById('container');
            c.innerHTML = '';
            
            nodes.forEach((nodeArr, idx) => {
                const div = document.createElement('div');
                div.className = 'node';
                
                // Render slots
                let html = '';
                for(let i=0; i<capacity; i++) {
                    const val = nodeArr[i] !== undefined ? nodeArr[i] : '-';
                    html += `<div class="array-slot">${val}</div>`;
                }
                html += `<div class="next-ptr">Next: ${idx < nodes.length-1 ? 'Node '+(idx+1) : 'NULL'}</div>`;
                div.innerHTML = html;
                c.appendChild(div);
                
                if(idx < nodes.length-1) {
                    const arrow = document.createElement('div');
                    arrow.className = 'arrow';
                    arrow.textContent = '->';
                    c.appendChild(arrow);
                }
            });
        }

        function add() {
            const v = document.getElementById('val').value;
            if(!v) return;
            
            // Find last node
            let last = nodes[nodes.length-1];
            if(last.length < capacity) {
                last.push(v);
            } else {
                nodes.push([v]);
            }
            render();
            document.getElementById('val').value = '';
        }
        render();
    </script>
</body>
</html>"""

# XOR Linked List
XOR_LINKED_LIST_VISUALIZER = """<!DOCTYPE html>
<html>
<head>
<style>
    body { font-family: 'Courier New', monospace; padding: 20px; background: #222; color: #0f0; }
    .node { 
        border: 1px solid #0f0; padding: 10px; display: inline-block; 
        margin: 10px; width: 140px; text-align: center;
        box-shadow: 0 0 10px #0f0;
    }
    .field { margin: 5px 0; border-bottom: 1px dashed #0a0; padding: 2px;}
    .addr { color: #ff0; font-size: 11px; }
    .xor-val { color: #0ff; font-size: 11px; }
    .arrow { display: inline-block; color: white; padding: 30px 0; }
</style>
</head>
<body>
    <h1>XOR Linked List (Simulation)</h1>
    <p>Memory Efficient: Stores XOR of Prev and Next addresses</p>
    <input id="val" placeholder="Value" style="background:#000; border:1px solid #0f0; color:#0f0; padding:5px;">
    <button onclick="add()" style="background:#000; border:1px solid #0f0; color:#0f0;">Simulate Memory</button>
    
    <div id="container" style="margin-top:20px; white-space:nowrap; overflow:auto;"></div>
    
    <script>
        let nodes = [];
        
        function memAddr(idx) { return 1000 + idx*4; } // Fake address
        
        function render() {
            const c = document.getElementById('container');
            c.innerHTML = '';
            
            nodes.forEach((val, i) => {
                const prevAddr = i > 0 ? memAddr(i-1) : 0;
                const nextAddr = i < nodes.length-1 ? memAddr(i+1) : 0;
                const xorVal = prevAddr ^ nextAddr;
                
                const html = `
                <div class="node">
                    <div class="field addr">Addr: 0x${memAddr(i).toString(16)}</div>
                    <div class="field" style="font-size:20px; font-weight:bold;">${val}</div>
                    <div class="field xor-val">npx: 0x${xorVal.toString(16)}</div>
                    <div style="font-size:10px; color:#888;">(0x${prevAddr.toString(16)} ^ 0x${nextAddr.toString(16)})</div>
                </div>`;
                c.innerHTML += html;
                
                if(i < nodes.length - 1) {
                    c.innerHTML += `<div class="arrow"><-></div>`;
                }
            });
        }

        function add() {
            const v = document.getElementById('val').value;
            if(v) {
                nodes.push(v);
                render();
                document.getElementById('val').value='';
            }
        }
    </script>
</body>
</html>"""
