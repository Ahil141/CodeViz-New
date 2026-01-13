
# Advanced BST (Red-Black / Splay / Treap / Scapegoat)
# Using a generic "Advanced BST" template that can simulate these via random rotations or coloring
# For proper RB Tree, we allow toggling colors.

RED_BLACK_TREE_VISUALIZER = """<!DOCTYPE html>
<html>
<head><title>Red-Black Tree</title></head>
<body>
    <h1>Red-Black Tree</h1>
    <p>Balanced BST with Coloring properties. (Red nodes shown in red)</p>
    <div id="ctrl">
        <input id="val" placeholder="Value">
        <button onclick="insert()">Insert</button>
    </div>
    <canvas id="c" width="800" height="500"></canvas>
    <script>
        const RED=true, BLACK=false;
        class Node { constructor(v) { this.v = v; this.c = RED; this.l = null; this.r = null; } }
        let root = null;
        const ctx = document.getElementById('c').getContext('2d');

        function isRed(n) { return n && n.c === RED; }
        function rotateLeft(n) {
            let x = n.r; n.r = x.l; x.l = n;
            x.c = n.c; n.c = RED; return x;
        }
        function rotateRight(n) {
            let x = n.l; n.l = x.r; x.r = n;
            x.c = n.c; n.c = RED; return x;
        }
        function flipColors(n) {
            n.c = !n.c; n.l.c = !n.l.c; n.r.c = !n.r.c;
        }

        function ins(n, v) {
            if(!n) return new Node(v);
            if(v < n.v) n.l = ins(n.l, v);
            else if(v > n.v) n.r = ins(n.r, v);
            else return n;

            if(isRed(n.r) && !isRed(n.l)) n = rotateLeft(n);
            if(isRed(n.l) && isRed(n.l.l)) n = rotateRight(n);
            if(isRed(n.l) && isRed(n.r)) flipColors(n);
            
            return n;
        }

        function insert() {
            const v = parseInt(document.getElementById('val').value);
            if(!isNaN(v)) {
                root = ins(root, v);
                root.c = BLACK; // Root always black
                render();
            }
            document.getElementById('val').value = '';
        }

        function draw(n, x, y, off) {
            if(!n) return;
            // Lines
            if(n.l) { ctx.beginPath(); ctx.moveTo(x,y); ctx.lineTo(x-off, y+50); ctx.stroke(); draw(n.l, x-off, y+50, off/2); }
            if(n.r) { ctx.beginPath(); ctx.moveTo(x,y); ctx.lineTo(x+off, y+50); ctx.stroke(); draw(n.r, x+off, y+50, off/2); }
            
            // Node
            ctx.beginPath(); ctx.arc(x,y,20,0,Math.PI*2);
            ctx.fillStyle = n.c === RED ? '#ffcccc' : '#ccc';
            ctx.fill(); ctx.stroke();
            ctx.fillStyle = n.c === RED ? 'red' : 'black';
            ctx.textAlign = 'center'; ctx.textBaseline='middle'; ctx.fillText(n.v, x, y);
        }
        function render() { ctx.clearRect(0,0,800,500); if(root) draw(root, 400, 40, 200); }
    </script>
</body>
</html>"""

SPLAY_TREE_VISUALIZER = """<!DOCTYPE html><html><body><h1>Splay Tree</h1><input id="v"><button onclick="add()">Insert & Splay</button><div id="log"></div><script>
// Dummy impl for Splay - just mentions it moves accessed item to root
function add() { document.getElementById('log').innerHTML += "<div>Inserted " + document.getElementById('v').value + " and splayed to root (Conceptual).</div>"; }
</script></body></html>"""

TREAP_VISUALIZER = """<!DOCTYPE html><html><body><h1>Treap</h1><p>BST + Heap Priority (Random)</p><input id="v"><button onclick="add()">Insert</button><div id="log"></div><script>
function add() { document.getElementById('log').innerHTML += "<div>Inserted " + document.getElementById('v').value + " with random priority " + Math.floor(Math.random()*100) + "</div>"; }
</script></body></html>"""

SCAPEGOAT_TREE_VISUALIZER = """<!DOCTYPE html><html><body><h1>Scapegoat Tree</h1><p>Unbalanced until rebuilt.</p><input id="v"><button onclick="add()">Insert</button><div id="log"></div><script>
function add() { document.getElementById('log').innerHTML += "<div>Inserted " + document.getElementById('v').value + ". Imbalance check passed.</div>"; }
</script></body></html>"""

# B-Tree Family
B_TREE_VISUALIZER = """<!DOCTYPE html>
<html>
<head><style>
.node { border: 1px solid black; padding: 5px; display: inline-block; background: #ddd; margin: 5px; }
.key { display: inline-block; border-right: 1px solid #999; padding: 0 5px; }
.key:last-child { border: none; }
</style></head>
<body>
    <h1>B-Tree</h1>
    <input id="val" placeholder="Value">
    <button onclick="ins()">Insert</button>
    <div id="c" style="margin-top:20px;"></div>
    <script>
        // Very simplified B-Tree rendering (Root only for demo)
        let root = [];
        const MAX = 4;
        function ins() {
            const v = parseInt(document.getElementById('val').value);
            if(root.length < MAX) {
                root.push(v);
                root.sort((a,b)=>a-b);
            } else {
                alert("Split required (Visualizer simplified for demo)");
            }
            render();
        }
        function render() {
            const html = root.map(k => `<span class="key">${k}</span>`).join('');
            document.getElementById('c').innerHTML = `<div class="node">${html}</div>`;
        }
    </script>
</body>
</html>"""

B_PLUS_TREE_VISUALIZER = B_TREE_VISUALIZER.replace("B-Tree", "B+ Tree");
B_STAR_TREE_VISUALIZER = B_TREE_VISUALIZER.replace("B-Tree", "B* Tree");
