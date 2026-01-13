
# Min/Max Heap Visualizer
HEAP_VISUALIZER = """<!DOCTYPE html>
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

        function swap(i, j) { [heap[i], heap[j]] = [heap[j], heap[i]]; }
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
            if(heap.length > 0) {
                heap[0] = end;
                bubbleDown(0);
            }
            alert("Extracted: " + root);
            render();
        }

        function bubbleUp(n) {
            let element = heap[n];
            while(n > 0) {
                let pIdx = Math.floor((n + 1) / 2) - 1;
                let parent = heap[pIdx];
                if(cmp(element, parent)) {
                    heap[pIdx] = element;
                    heap[n] = parent;
                    n = pIdx;
                } else break;
            }
        }

        function bubbleDown(n) {
            const len = heap.length;
            const element = heap[n];
            while(true) {
                let lChildIdx = 2 * n + 1;
                let rChildIdx = 2 * n + 2;
                let lChild, rChild;
                let swapIdx = null;

                if(lChildIdx < len) {
                    lChild = heap[lChildIdx];
                    if(cmp(lChild, element)) swapIdx = lChildIdx;
                }
                if(rChildIdx < len) {
                    rChild = heap[rChildIdx];
                    if(cmp(rChild, (swapIdx === null ? element : lChild))) swapIdx = rChildIdx;
                }
                
                if(swapIdx === null) break;
                heap[n] = heap[swapIdx];
                heap[swapIdx] = element;
                n = swapIdx;
            }
        }

        function drawNode(idx, x, y, offset) {
            if(idx >= heap.length) return;
            
            // Draw lines to children
            if(2*idx+1 < heap.length) {
                ctx.beginPath(); ctx.moveTo(x, y+20); ctx.lineTo(x-offset, y+80-20); ctx.stroke();
                drawNode(2*idx+1, x-offset, y+80, offset/2);
            }
            if(2*idx+2 < heap.length) {
                ctx.beginPath(); ctx.moveTo(x, y+20); ctx.lineTo(x+offset, y+80-20); ctx.stroke();
                drawNode(2*idx+2, x+offset, y+80, offset/2);
            }

            // Draw Node
            ctx.beginPath();
            ctx.arc(x, y, 20, 0, Math.PI*2);
            ctx.fillStyle = '#ffcc00'; ctx.fill(); ctx.stroke();
            ctx.fillStyle = 'black'; ctx.textAlign='center'; ctx.textBaseline='middle';
            ctx.fillText(heap[idx], x, y);
        }

        function render() {
            ctx.clearRect(0,0,800,500);
            drawNode(0, 400, 40, 200);
        }
    </script>
</body>
</html>"""

# Advanced Heaps (Fibonacci/Binomial/Pairing) - Simplified visualization for these complex structures
# Just showing a textual/tree representation stating the structure type
ADVANCED_HEAP_VISUALIZER_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<style>
    body { font-family: sans-serif; padding: 20px; }
    .tree-root { border: 2px solid #333; padding: 10px; margin: 10px; display: inline-block; background: #e0e0e0; }
    .tree-child { margin-left: 20px; border-left: 1px dashed #666; padding-left: 10px; }
</style>
</head>
<body>
    <h1 id="title">Heap</h1>
    <p>Visualizing structure of roots and children.</p>
    <input id="val" placeholder="Value">
    <button onclick="insert()">Insert</button>
    <div id="container"></div>
    <script>
        const TYPE = "__TYPE__";
        document.getElementById('title').textContent = TYPE;
        
        let roots = [];
        
        function insert() {
            const v = document.getElementById('val').value;
            if(!v) return;
            // Simple generic forest logic for demo
            roots.push({ val: v, children: [] });
            // For Fibonacci/Binomial, we would normally merge trees here
            // We simplify by just adding roots to look like a forest (valid for Fib heap before consolidate)
            render();
            document.getElementById('val').value = '';
        }

        function renderNode(n) {
            let html = `<div class="tree-root">Key: ${n.val}`;
            if(n.children.length > 0) {
                 n.children.forEach(c => html += `<div class="tree-child">${renderNode(c)}</div>`);
            }
            html += "</div>";
            return html;
        }

        function render() {
            const c = document.getElementById('container');
            c.innerHTML = roots.map(renderNode).join('');
        }
    </script>
</body>
</html>"""

FIBONACCI_HEAP_VISUALIZER = ADVANCED_HEAP_VISUALIZER_TEMPLATE.replace("__TYPE__", "Fibonacci Heap");
BINOMIAL_HEAP_VISUALIZER = ADVANCED_HEAP_VISUALIZER_TEMPLATE.replace("__TYPE__", "Binomial Heap");
PAIRING_HEAP_VISUALIZER = ADVANCED_HEAP_VISUALIZER_TEMPLATE.replace("__TYPE__", "Pairing Heap");
