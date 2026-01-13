
# Basic Array Visualizer
ARRAY_VISUALIZER = """<!DOCTYPE html>
<html>
<head>
<title>Array</title>
<style>
    body { font-family: sans-serif; padding: 20px; text-align: center; }
    .array-container { display: flex; justify-content: center; margin-top: 50px; flex-wrap: wrap; gap: 5px; }
    .cell { 
        width: 60px; height: 60px; border: 2px solid #333; 
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        background: skyblue; position: relative;
    }
    .index { position: absolute; top: -25px; font-size: 12px; color: #555; }
    .val { font-weight: bold; font-size: 18px; }
</style>
</head>
<body>
    <h1>Array Visualizer</h1>
    <p>Contiguous Memory allocation</p>
    <div>
        <input id="size" type="number" placeholder="Size" value="5">
        <button onclick="create()">Create Array</button>
        <span style="margin: 0 10px">|</span>
        <input id="idx" type="number" placeholder="Index" style="width:60px">
        <input id="val" placeholder="Value" style="width:80px">
        <button onclick="update()">Update</button>
    </div>
    <div id="container" class="array-container"></div>
    <script>
        let arr = [];
        
        function create() {
            const s = parseInt(document.getElementById('size').value) || 5;
            arr = new Array(s).fill(0);
            render();
        }
        
        function update() {
            const i = parseInt(document.getElementById('idx').value);
            const v = document.getElementById('val').value;
            if(i >= 0 && i < arr.length) {
                arr[i] = v;
                render();
            } else {
                alert("Index out of bounds");
            }
        }
        
        function render() {
            const c = document.getElementById('container');
            c.innerHTML = '';
            arr.forEach((val, i) => {
                const div = document.createElement('div');
                div.className = 'cell';
                div.innerHTML = `<span class="index">${i}</span><span class="val">${val}</span>`;
                c.appendChild(div);
            });
        }
        create();
    </script>
</body>
</html>"""

# Dynamic Array (Visualizes capacity vs size)
DYNAMIC_ARRAY_VISUALIZER = """<!DOCTYPE html>
<html>
<head>
    <title>Dynamic Array</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        .memory-block { border: 2px solid #666; padding: 10px; display: inline-flex; gap: 2px; background: #eee; }
        .cell { width: 50px; height: 50px; background: white; border: 1px solid #999; display: flex; align-items: center; justify-content: center; font-weight: bold; }
        .cell.used { background: #4caf50; color: white; }
        .info { margin: 20px 0; font-size: 18px; }
    </style>
</head>
<body>
    <h1>Dynamic Array (Vector/ArrayList)</h1>
    <div class="info">
        Size: <span id="size">0</span> | Capacity: <span id="cap">2</span>
    </div>
    <div>
        <input id="val" placeholder="Value">
        <button onclick="push()">Push</button>
    </div>
    <br>
    <div id="container" class="memory-block"></div>
    <script>
        let data = [];
        let capacity = 2;
        
        function render() {
            const c = document.getElementById('container');
            c.innerHTML = '';
            document.getElementById('size').textContent = data.length;
            document.getElementById('cap').textContent = capacity;
            
            for(let i=0; i<capacity; i++) {
                const div = document.createElement('div');
                div.className = 'cell';
                if(i < data.length) {
                    div.className += ' used';
                    div.textContent = data[i];
                }
                c.appendChild(div);
            }
        }
        
        function push() {
            const v = document.getElementById('val').value;
            if(!v) return;
            
            if(data.length === capacity) {
                capacity *= 2; // Resize
                alert("Resizing! New Capacity: " + capacity);
            }
            
            data.push(v);
            render();
            document.getElementById('val').value = '';
        }
        render();
    </script>
</body>
</html>"""

# Sparse Array
SPARSE_ARRAY_VISUALIZER = """<!DOCTYPE html>
<html>
<head>
<style>
    body { font-family: monospace; }
    .entry { border: 1px solid #333; padding: 5px; margin: 5px; width: 200px; display: flex; justify-content: space-between; }
</style>
</head>
<body>
    <h1>Sparse Array</h1>
    <p>Only stores non-default values. Implementation usually via Map or Linked List.</p>
    <input id="idx" placeholder="Index (e.g. 1000)" type="number">
    <input id="val" placeholder="Value">
    <button onclick="set()">Set</button>
    <div id="list" style="margin-top:20px;"></div>
    <script>
        let store = {};
        
        function render() {
            const l = document.getElementById('list');
            l.innerHTML = '';
            Object.keys(store).sort((a,b)=>a-b).forEach(k => {
                l.innerHTML += `<div class="entry"><span>Index [${k}]</span> <span>-></span> <span>${store[k]}</span></div>`;
            });
        }
        
        function set() {
            const i = document.getElementById('idx').value;
            const v = document.getElementById('val').value;
            if(i && v) {
                store[i] = v;
                render();
            }
        }
    </script>
</body>
</html>"""

# Jagged Array
JAGGED_ARRAY_VISUALIZER = """<!DOCTYPE html>
<html>
<head>
<style>
    body { font-family: sans-serif; padding: 20px;}
    .row { display: flex; margin-bottom: 10px; align-items: center; }
    .row-label { width: 50px; font-weight: bold; }
    .cell { width: 40px; height: 40px; background: orange; margin-right: 2px; display: flex; align-items: center; justify-content: center; color: white; border: 1px solid #cc7a00; }
</style>
</head>
<body>
    <h1>Jagged Array</h1>
    <p>Array of Arrays of different sizes.</p>
    <button onclick="addRow()">Add Row</button>
    <div id="container" style="margin-top:20px;"></div>
    <script>
        let rows = [];
        
        function addRow() {
            // Random length between 1 and 8
            const len = Math.floor(Math.random() * 8) + 1;
            const row = new Array(len).fill(0).map(() => Math.floor(Math.random()*10));
            rows.push(row);
            render();
        }
        
        function render() {
            const c = document.getElementById('container');
            c.innerHTML = '';
            rows.forEach((r, i) => {
                const rDiv = document.createElement('div');
                rDiv.className = 'row';
                let html = `<div class="row-label">R${i}</div>`;
                r.forEach(val => {
                    html += `<div class="cell">${val}</div>`;
                });
                rDiv.innerHTML = html;
                c.appendChild(rDiv);
            });
        }
        addRow(); addRow();
    </script>
</body>
</html>"""

# Circular Array
CIRCULAR_ARRAY_VISUALIZER = """<!DOCTYPE html>
<html>
<!-- Similar to Circular Queue logic generally -->
<head>
<style>
    body { font-family: sans-serif; text-align: center; }
    .cir-container { position: relative; width: 300px; height: 300px; margin: 20px auto; border: 2px dashed #ccc; border-radius: 50%; }
    .cell { position: absolute; width: 50px; height: 50px; background: #ddd; display: flex; align-items: center; justify-content: center; border-radius: 50%; }
</style>
</head>
<body>
    <h1>Circular Array / Buffer</h1>
    <button onclick="writeVal()">Write Next</button>
    <div class="cir-container" id="c"></div>
    <script>
        const size = 8;
        let arr = new Array(size).fill(null);
        let ptr = 0;
        
        function render() {
            const c = document.getElementById('c');
            c.innerHTML = '';
            const r = 120;
            const cx = 150, cy = 150;
            
            for(let i=0; i<size; i++) {
                const angle = (i / size) * Math.PI * 2 - Math.PI/2;
                const x = cx + Math.cos(angle) * r - 25;
                const y = cy + Math.sin(angle) * r - 25;
                
                const div = document.createElement('div');
                div.className = 'cell';
                div.style.left = x+'px';
                div.style.top = y+'px';
                div.textContent = arr[i] === null ? '-' : arr[i];
                
                if(i === ptr) div.style.border = "3px solid red";
                
                c.appendChild(div);
            }
        }
        
        function writeVal() {
            arr[ptr] = Math.floor(Math.random()*100);
            ptr = (ptr + 1) % size;
            render();
        }
        render();
    </script>
</body>
</html>"""
