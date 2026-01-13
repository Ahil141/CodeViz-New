
# General Tree Visualizer (Flexible N-ary)
GENERAL_TREE_VISUALIZER = """<!DOCTYPE html>
<html>
<head>
<style>
    body { font-family: sans-serif; text-align: center; }
    .tree ul { padding-top: 20px; position: relative; transition: all 0.5s; }
    .tree li { float: left; text-align: center; list-style-type: none; position: relative; padding: 20px 5px 0 5px; transition: all 0.5s; }
    .tree li::before, .tree li::after { content: ''; position: absolute; top: 0; right: 50%; border-top: 1px solid #ccc; width: 50%; height: 20px; }
    .tree li::after { right: auto; left: 50%; border-left: 1px solid #ccc; }
    .tree li:only-child::after, .tree li:only-child::before { display: none; }
    .tree li:only-child { padding-top: 0; }
    .tree li:first-child::before, .tree li:last-child::after { border: 0 none; }
    .tree li:last-child::before { border-right: 1px solid #ccc; border-radius: 0 5px 0 0; }
    .tree li:first-child::after { border-radius: 5px 0 0 0; }
    .tree ul ul::before { content: ''; position: absolute; top: 0; left: 50%; border-left: 1px solid #ccc; width: 0; height: 20px; }
    .tree li a { border: 1px solid #ccc; padding: 5px 10px; text-decoration: none; color: #666; font-family: arial, verdana, tahoma; font-size: 11px; display: inline-block; border-radius: 5px; transition: all 0.5s; background: white; }
    .tree li a:hover, .tree li a:hover+ul li a { background: #c8e4f8; color: #000; border: 1px solid #94a0b4; }
</style>
</head>
<body>
    <h1>General / N-ary Tree</h1>
    <div class="tree" id="tree">
        <!-- Rendered via CSS Tree Logic -->
    </div>
    <div style="margin-top:20px;">
        <button onclick="reset()">Reset Random</button>
    </div>
    <script>
        function generateRandomTree(depth) {
            if(depth === 0) return null;
            const val = Math.floor(Math.random()*100);
            const node = { val, children: [] };
            const numChildren = Math.floor(Math.random() * 3); // 0-2 children
            for(let i=0; i<numChildren; i++) {
                const child = generateRandomTree(depth - 1);
                if(child) node.children.push(child);
            }
            return node;
        }

        function renderNode(node) {
            if(!node) return '';
            let html = `<li><a href="#">${node.val}</a>`;
            if(node.children.length > 0) {
                html += '<ul>';
                node.children.forEach(c => html += renderNode(c));
                html += '</ul>';
            }
            html += '</li>';
            return html;
        }

        function reset() {
            const root = generateRandomTree(4);
            document.getElementById('tree').innerHTML = `<ul>${renderNode(root)}</ul>`;
        }
        reset();
    </script>
</body>
</html>"""

# Binary Search Tree
BST_VISUALIZER = """<!DOCTYPE html>
<html>
<head>
<style>
    body { font-family: sans-serif; text-align: center; }
    canvas { border: 1px solid #eee; }
</style>
</head>
<body>
    <h1>Binary Search Tree (BST)</h1>
    <input id="val" type="number" placeholder="Value">
    <button onclick="add()">Insert</button>
    <br><br>
    <canvas id="c" width="800" height="500"></canvas>
    <script>
        class Node {
            constructor(val) { this.val = val; this.left = null; this.right = null; this.x = 0; this.y = 0; }
        }
        let root = null;
        const ctx = document.getElementById('c').getContext('2d');

        function insert(node, val) {
            if(!node) return new Node(val);
            if(val < node.val) node.left = insert(node.left, val);
            else if(val > node.val) node.right = insert(node.right, val);
            return node;
        }

        function add() {
            const v = parseInt(document.getElementById('val').value);
            if(!isNaN(v)) { root = insert(root, v); render(); }
            document.getElementById('val').value = '';
        }

        function drawNode(node, x, y, offset) {
            if(!node) return;
            node.x = x; node.y = y;
            
            ctx.beginPath();
            ctx.arc(x, y, 20, 0, Math.PI*2);
            ctx.fillStyle = 'white'; ctx.fill(); ctx.stroke();
            ctx.fillStyle = 'black'; ctx.textAlign = 'center'; ctx.textBaseline='middle';
            ctx.fillText(node.val, x, y);

            if(node.left) {
                ctx.moveTo(x, y+20); ctx.lineTo(x-offset, y+60-20); ctx.stroke();
                drawNode(node.left, x-offset, y+60, offset/2);
            }
            if(node.right) {
                ctx.moveTo(x, y+20); ctx.lineTo(x+offset, y+60-20); ctx.stroke();
                drawNode(node.right, x+offset, y+60, offset/2);
            }
        }

        function render() {
            ctx.clearRect(0,0,800,500);
            if(root) drawNode(root, 400, 40, 200);
        }
    </script>
</body>
</html>"""

# AVL Tree (Uses same renderer as BST but logic differs to self-balance)
# For brevity, implementing a visual wrapper that simulates behavior or standard BST with note.
# Actually, let's implement true AVL rotation logic for "WOW" factor.
AVL_TREE_VISUALIZER = """<!DOCTYPE html>
<html>
<head><title>AVL Tree</title></head>
<body>
    <h1>AVL Tree (Self-Balancing)</h1>
    <p>Automatically balances height difference.</p>
    <input id="val" type="number">
    <button onclick="add()">Insert</button>
    <div id="msg" style="color:blue; height:20px;"></div>
    <canvas id="c" width="800" height="500" style="border:1px solid #ccc;"></canvas>
    <script>
        // Minified AVL Logic
        class Node { constructor(v) { this.v = v; this.h = 1; this.l = null; this.r = null; } }
        let root = null;
        const ctx = document.getElementById('c').getContext('2d');

        function h(n) { return n ? n.h : 0; }
        function bal(n) { return n ? h(n.l) - h(n.r) : 0; }
        function up(n) { n.h = 1 + Math.max(h(n.l), h(n.r)); return n; }
        
        function rotR(y) {
            let x = y.l; let T2 = x.r;
            x.r = y; y.l = T2;
            up(y); up(x); return x;
        }
        function rotL(x) {
            let y = x.r; let T2 = y.l;
            y.l = x; x.r = T2;
            up(x); up(y); return y;
        }

        function ins(n, v) {
            if(!n) return new Node(v);
            if(v < n.v) n.l = ins(n.l, v);
            else if(v > n.v) n.r = ins(n.r, v);
            else return n; // No duplicates
            
            up(n);
            let b = bal(n);
            
            // LL
            if(b > 1 && v < n.l.v) return rotR(n);
            // RR
            if(b < -1 && v > n.r.v) return rotL(n);
            // LR
            if(b > 1 && v > n.l.v) { n.l = rotL(n.l); return rotR(n); }
            // RL
            if(b < -1 && v < n.r.v) { n.r = rotR(n.r); return rotL(n); }
            
            return n;
        }

        function add() {
            const v = parseInt(document.getElementById('val').value);
            if(!isNaN(v)) { root = ins(root, v); render(); }
            document.getElementById('val').value = '';
        }

        function draw(n, x, y, off) {
            if(!n) return;
            ctx.beginPath(); ctx.arc(x,y,20,0,7); ctx.stroke();
            ctx.fillText(n.v, x-5, y+5);
            if(n.l) { ctx.moveTo(x,y+20); ctx.lineTo(x-off,y+60); ctx.stroke(); draw(n.l, x-off, y+60, off/2); }
            if(n.r) { ctx.moveTo(x,y+20); ctx.lineTo(x+off,y+60); ctx.stroke(); draw(n.r, x+off, y+60, off/2); }
        }
        function render() { ctx.clearRect(0,0,800,500); if(root) draw(root, 400, 40, 200); }
    </script>
</body>
</html>"""
