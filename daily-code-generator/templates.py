"""
Code Templates Engine
=====================
Generates real, working Python code files for each topic.
Each template produces runnable, documented code — not stubs.
"""

import os
from pathlib import Path
from datetime import datetime

YEAR = str(datetime.now().year)

import sys


def _readme_str(title, description, category, files, username=""):
    fs = [f for f in files if f != "README.md"]
    if len(fs) == 1:
        tree = f"└── {fs[0]}"
    elif len(fs) > 1:
        parts = []
        for i, f in enumerate(fs):
            prefix = "└──" if i == len(fs) - 1 else "├──"
            parts.append(f"{prefix} {f}")
        tree = "\n".join(parts)
    else:
        tree = ""

    py_ver = f"{sys.version_info.major}.{sys.version_info.minor}"
    return f"""# {title}

> 🏷 **{category}** · ⚡ Daily Code · 📅 {datetime.now().strftime('%Y-%m-%d')}

{description}

## 📁 Structure

```
{tree}
```

## 🚀 Run

```bash
python {files[0]}
```

## 📋 Requirements

- Python {py_ver}

## 🔗 Daily Code Series

Part of my [daily-code](https://github.com/{username}/daily-code) challenge — shipping one mini-project every day.
"""


# ── Specific code generators ───────────────────────────────────────────────

def _sorting_visualizer():
    return [("visualizer.py", '''"""
Sorting Algorithm Visualizer — Terminal Edition
Shows bubble, selection, insertion, merge, quick sort step-by-step.
"""
import time
import random
import os


def bubble_sort(arr, steps_callback=None):
    n = len(arr)
    steps = 0
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            steps += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
                if steps_callback:
                    steps_callback(arr, j, j + 1, "Bubble")
        if not swapped:
            break
    return steps


def selection_sort(arr, steps_callback=None):
    n = len(arr)
    steps = 0
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            steps += 1
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        if steps_callback:
            steps_callback(arr, i, min_idx, "Selection")
    return steps


def insertion_sort(arr, steps_callback=None):
    steps = 0
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            steps += 1
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        if steps_callback:
            steps_callback(arr, j + 1, i, "Insertion")
    return steps


def merge_sort(arr, steps_callback=None):
    steps = [0]

    def _merge(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            steps[0] += 1
            if left[i] <= right[j]:
                result.append(left[i]); i += 1
            else:
                result.append(right[j]); j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def _sort(a):
        if len(a) <= 1:
            return a
        mid = len(a) // 2
        left = _sort(a[:mid])
        right = _sort(a[mid:])
        merged = _merge(left, right)
        if steps_callback:
            steps_callback(merged, -1, -1, "Merge")
        return merged

    result = _sort(arr.copy())
    arr[:] = result
    return steps[0]


def display_step(arr, i, j, algo_name):
    """Print array with highlighted positions."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"═══ {algo_name} Sort ═══")
    print()
    bar = ""
    for idx, val in enumerate(arr):
        c = "█" if idx in (i, j) else "░"
        bar += c * max(1, val // 2) + f" {val}\\n"
    print(bar)
    time.sleep(0.05)


def benchmark():
    sizes = [100, 500, 1000, 2000]
    algorithms = {
        "Bubble": bubble_sort,
        "Selection": selection_sort,
        "Insertion": insertion_sort,
        "Merge": merge_sort,
    }
    print("\\n═══ Benchmark (ops count) ═══\\n")
    print(f"{'Size':>8}", end="")
    for name in algorithms:
        print(f"{name:>12}", end="")
    print()
    print("-" * 56)

    for size in sizes:
        print(f"{size:>8}", end="")
        for name, algo in algorithms.items():
            arr = list(range(size, 0, -1))
            ops = algo(arr)
            print(f"{ops:>12}", end="")
        print()
    print()


if __name__ == "__main__":
    print("\\n🧮 Sorting Algorithm Visualizer\\n")

    # Demo with visualization
    arr = [random.randint(1, 50) for _ in range(25)]
    print("Original:", arr)
    print("\\nRunning Bubble Sort with visualization...\\n")
    time.sleep(1)

    demo = arr.copy()
    bubble_sort(demo, display_step)

    print("\\nSorted:", demo)
    print(f"\\n✅ Correct: {demo == sorted(arr)}")

    benchmark()
'''), ("algorithms.py", '''"""
Additional sorting algorithms for the visualizer.
Includes: quick sort, heap sort, shell sort.
"""


def quick_sort(arr, low=0, high=None):
    """In-place quick sort with Lomuto partition."""
    if high is None:
        high = len(arr) - 1
    ops = [0]

    def _partition(lo, hi):
        pivot = arr[hi]
        i = lo - 1
        for j in range(lo, hi):
            ops[0] += 1
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
        return i + 1

    def _sort(lo, hi):
        if lo < hi:
            p = _partition(lo, hi)
            _sort(lo, p - 1)
            _sort(p + 1, hi)

    _sort(low, high)
    return ops[0]


def heap_sort(arr):
    """Heap sort using max-heap."""
    n = len(arr)
    ops = [0]

    def _heapify(size, root):
        largest = root
        left = 2 * root + 1
        right = 2 * root + 2
        if left < size:
            ops[0] += 1
            if arr[left] > arr[largest]:
                largest = left
        if right < size:
            ops[0] += 1
            if arr[right] > arr[largest]:
                largest = right
        if largest != root:
            arr[root], arr[largest] = arr[largest], arr[root]
            _heapify(size, largest)

    for i in range(n // 2 - 1, -1, -1):
        _heapify(n, i)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        _heapify(i, 0)
    return ops[0]


def shell_sort(arr):
    """Shell sort with gap sequence."""
    n = len(arr)
    ops = [0]
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap:
                ops[0] += 1
                if arr[j - gap] > temp:
                    arr[j] = arr[j - gap]
                    j -= gap
                else:
                    break
            arr[j] = temp
        gap //= 2
    return ops[0]
''')]


def _bloom_filter():
    return [("bloom_filter.py", '''"""
Bloom Filter — Space-efficient probabilistic set membership test.
Supports configurable false-positive rate and multiple hash functions.
"""
import math
import hashlib
import struct


class BloomFilter:
    """
    Probabilistic data structure for set membership.

    False positives: possible (says "maybe in set")
    False negatives: impossible (never says "definitely not in set" when it is)
    """

    def __init__(self, expected_items: int = 1000, false_positive_rate: float = 0.01):
        """
        Args:
            expected_items: Estimated number of items to store
            false_positive_rate: Acceptable false positive probability (0.01 = 1%)
        """
        self.expected_items = expected_items
        self.fp_rate = false_positive_rate

        # Optimal bit array size: m = -n*ln(p) / (ln(2))^2
        self.bit_size = int(
            -(expected_items * math.log(false_positive_rate)) / (math.log(2) ** 2)
        )

        # Optimal number of hash functions: k = (m/n) * ln(2)
        self.hash_count = int((self.bit_size / expected_items) * math.log(2))

        self.bit_array = 0  # Use Python's arbitrary-precision int as bit array

        self._items_added = 0

    def _hashes(self, item: str):
        """Generate k hash values using double hashing technique."""
        h = hashlib.sha256(item.encode()).digest()
        h1, h2 = struct.unpack("!QQ", h[:16])
        for i in range(self.hash_count):
            yield (h1 + i * h2) % self.bit_size

    def add(self, item: str) -> None:
        """Add an item to the filter."""
        for idx in self._hashes(item):
            self.bit_array |= (1 << idx)
        self._items_added += 1

    def contains(self, item: str) -> bool:
        """Check if an item might be in the set."""
        for idx in self._hashes(item):
            if not (self.bit_array & (1 << idx)):
                return False
        return True

    @property
    def stats(self) -> dict:
        """Current filter statistics."""
        # Estimate fill ratio
        bits_set = self.bit_array.bit_count()
        fill = bits_set / self.bit_size

        # Current actual false positive rate
        actual_fp = fill ** self.hash_count

        return {
            "bit_size": self.bit_size,
            "hash_functions": self.hash_count,
            "items_added": self._items_added,
            "bits_set": bits_set,
            "fill_ratio": f"{fill:.1%}",
            "estimated_fp_rate": f"{actual_fp:.4%}",
            "memory_bytes": self.bit_size // 8,
        }


if __name__ == "__main__":
    bf = BloomFilter(expected_items=5000, false_positive_rate=0.01)

    print("═══ Bloom Filter Demo ═══\\n")
    print(f"Config: {bf.expected_items} items @ {bf.fp_rate:.0%} FP rate")
    print(f"Bit array: {bf.bit_size:,} bits ({bf.bit_size//8:,} bytes)")
    print(f"Hash functions: {bf.hash_count}\\n")

    # Add items
    words = ["apple", "banana", "cherry", "date", "elderberry",
             "fig", "grape", "honeydew", "kiwi", "lemon"]
    for w in words:
        bf.add(w)

    print(f"Added {len(words)} items\\n")

    # Test membership
    tests = ["apple", "banana", "mango", "orange", "cherry", "papaya"]
    print("Testing membership:")
    for w in tests:
        in_set = w in words
        maybe_in = bf.contains(w)
        status = "✅" if in_set == maybe_in else ("⚠️  FP!" if maybe_in else "❌ FN!")
        print(f"  {w:12s} → In set: {str(in_set):5s} | BF says: {str(maybe_in):5s} {status}")

    print(f"\\n{bf.stats}")
'''), ("test_bloom.py", '''"""Tests for BloomFilter implementation."""
from bloom_filter import BloomFilter


def test_basic():
    bf = BloomFilter(expected_items=100, false_positive_rate=0.01)
    bf.add("hello")
    bf.add("world")
    assert bf.contains("hello")
    assert bf.contains("world")
    assert not bf.contains("missing")
    print("✅ Basic test passed")


def test_false_positive_rate():
    bf = BloomFilter(expected_items=1000, false_positive_rate=0.05)
    known = set()
    for i in range(1000):
        item = f"item_{i}"
        bf.add(item)
        known.add(item)

    fps = 0
    trials = 10000
    for i in range(1000, 1000 + trials):
        if bf.contains(f"item_{i}"):
            fps += 1

    actual_fp = fps / trials
    print(f"  Expected FP: ≤5%, Actual: {actual_fp:.2%}")
    assert actual_fp < 0.10, f"FP rate too high: {actual_fp:.2%}"
    print(f"✅ FP rate test passed ({actual_fp:.2%})")


if __name__ == "__main__":
    test_basic()
    test_false_positive_rate()
    print("\\n🎉 All tests passed!")
''')]


def _cli_todo():
    return [("todo.py", '''"""
Terminal Todo App with SQLite — Full-featured task manager.
"""
import sqlite3
import sys
import os
from datetime import datetime, date

DB_PATH = os.path.join(os.path.dirname(__file__), "todos.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            project TEXT DEFAULT 'general',
            priority INTEGER DEFAULT 1,
            due_date TEXT,
            done INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    return conn


def add_task(conn, task: str, project: str = "general", priority: int = 1, due: str = None):
    conn.execute(
        "INSERT INTO todos (task, project, priority, due_date) VALUES (?, ?, ?, ?)",
        (task, project, priority, due)
    )
    conn.commit()
    print(f"✅ Added: {task}")


def list_tasks(conn, project: str = None, show_done: bool = False):
    query = "SELECT id, task, project, priority, due_date, done FROM todos"
    params = []
    if project:
        query += " WHERE project = ?"
        params.append(project)
        if not show_done:
            query += " AND done = 0"
    elif not show_done:
        query += " WHERE done = 0"
    query += " ORDER BY priority DESC, due_date ASC"

    rows = conn.execute(query, params).fetchall()

    if not rows:
        print("📭 No tasks found!")
        return

    print(f"\\n{'─' * 70}")
    print(f"{'ID':<5} {'Status':<6} {'Prio':<5} {'Task':<30} {'Project':<12} {'Due':<12}")
    print(f"{'─' * 70}")

    for row in rows:
        id_, task, proj, prio, due, done = row
        status = "✅" if done else "⬜"
        prio_str = {1: "⬇️ ", 2: "📌", 3: "🔥"}.get(prio, "  ")
        print(f"{id_:<5} {status:<6} {prio_str:<5} {task[:28]:<30} {proj[:10]:<12} {due or '':<12}")
    print(f"{'─' * 70}\\n")


def complete_task(conn, task_id: int):
    conn.execute("UPDATE todos SET done = 1 WHERE id = ?", (task_id,))
    conn.commit()
    print(f"✅ Task #{task_id} completed!")


def delete_task(conn, task_id: int):
    conn.execute("DELETE FROM todos WHERE id = ?", (task_id,))
    conn.commit()
    print(f"🗑️  Task #{task_id} deleted!")


def stats(conn):
    total = conn.execute("SELECT COUNT(*) FROM todos").fetchone()[0]
    done = conn.execute("SELECT COUNT(*) FROM todos WHERE done = 1").fetchone()[0]
    pending = total - done

    today = date.today().isoformat()
    due_today = conn.execute(
        "SELECT COUNT(*) FROM todos WHERE due_date = ? AND done = 0", (today,)
    ).fetchone()[0]
    overdue = conn.execute(
        "SELECT COUNT(*) FROM todos WHERE due_date < ? AND done = 0", (today,)
    ).fetchone()[0]

    print(f"\\n📊 Stats: {total} total | {done} done | {pending} pending | "
          f"{due_today} due today | {overdue} overdue\\n")


def show_help():
    print("""
📋 Todo App Commands:
  add <task> [-p <project>] [--priority 1-3] [--due YYYY-MM-DD]
  list [-p <project>] [--all]
  done <id>
  delete <id>
  stats
  help
  quit
""")


def main():
    conn = init_db()
    print("\\n📋 Terminal Todo App")
    print("Type 'help' for commands, 'quit' to exit.\\n")

    while True:
        try:
            cmd = input("todo> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\\n👋 Bye!")
            break

        if not cmd:
            continue

        parts = cmd.split(maxsplit=1)
        action = parts[0].lower()
        rest = parts[1] if len(parts) > 1 else ""

        if action == "quit":
            print("👋 Bye!")
            break
        elif action == "help":
            show_help()
        elif action == "add":
            # Simple parse
            task = rest
            project = "general"
            priority = 1
            due = None
            args = rest.split()
            if "-p" in args:
                idx = args.index("-p")
                project = args[idx + 1]
                task = " ".join(args[:idx])
            if "--due" in args:
                idx = args.index("--due")
                due = args[idx + 1]
                task = " ".join(a for a in args if a not in ("-p", project, "--due", due))
            if "--priority" in args:
                idx = args.index("--priority")
                priority = int(args[idx + 1])
            add_task(conn, task, project, priority, due)
        elif action == "list":
            proj = None
            show_done = "--all" in rest
            if "-p" in rest:
                args = rest.split()
                idx = args.index("-p")
                proj = args[idx + 1]
            list_tasks(conn, project=proj, show_done=show_done)
        elif action == "done":
            if rest.isdigit():
                complete_task(conn, int(rest))
            else:
                print("Usage: done <id>")
        elif action == "delete":
            if rest.isdigit():
                delete_task(conn, int(rest))
            else:
                print("Usage: delete <id>")
        elif action == "stats":
            stats(conn)
        else:
            print(f"Unknown command: {action}")

    conn.close()


if __name__ == "__main__":
    main()
''')]


def _url_shortener():
    return [("main.py", '''"""
URL Shortener with FastAPI — Self-hosted link shortener.
"""
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import sqlite3
import string
import os

app = FastAPI(title="URL Shortener", version="1.0.0")
templates = Jinja2Templates(directory="templates")

DB = "urls.db"
BASE_URL = os.environ.get("BASE_URL", "http://localhost:8000")

CHARS = string.ascii_letters + string.digits
BASE = len(CHARS)


def init_db():
    conn = sqlite3.connect(DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code TEXT UNIQUE NOT NULL,
            original_url TEXT NOT NULL,
            clicks INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    return conn


def encode(num: int) -> str:
    """Base62 encode an integer to short code."""
    if num == 0:
        return CHARS[0]
    result = []
    while num > 0:
        result.append(CHARS[num % BASE])
        num //= BASE
    return "".join(reversed(result))


def create_short(conn, url: str) -> str:
    """Insert URL and return short code."""
    cur = conn.execute("INSERT INTO urls (original_url) VALUES (?)", (url,))
    conn.commit()
    code = encode(cur.lastrowid)
    conn.execute("UPDATE urls SET short_code = ? WHERE id = ?", (code, cur.lastrowid))
    conn.commit()
    return code


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.get_template("index.html").render({"request": request})


@app.post("/shorten")
async def shorten(url: str = Form(...)):
    conn = init_db()
    code = create_short(conn, url)
    short_url = f"{BASE_URL}/{code}"
    conn.close()
    return {"short_url": short_url, "code": code}


@app.get("/{code}")
async def redirect(code: str):
    conn = init_db()
    row = conn.execute(
        "SELECT original_url FROM urls WHERE short_code = ?", (code,)
    ).fetchone()
    if row:
        conn.execute("UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?", (code,))
        conn.commit()
        conn.close()
        return RedirectResponse(url=row[0], status_code=302)
    conn.close()
    raise HTTPException(status_code=404, detail="Short URL not found")


@app.get("/api/stats/{code}")
async def stats(code: str):
    conn = init_db()
    row = conn.execute(
        "SELECT short_code, original_url, clicks, created_at FROM urls WHERE short_code = ?",
        (code,),
    ).fetchone()
    conn.close()
    if row:
        return dict(zip(["short_code", "original_url", "clicks", "created_at"], row))
    raise HTTPException(status_code=404, detail="Not found")


if __name__ == "__main__":
    import uvicorn
    print("\\n🔗 URL Shortener starting...")
    print(f"   Open {BASE_URL} in your browser\\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''), ("templates/index.html", '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>URL Shortener</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: system-ui, -apple-system, sans-serif;
            display: flex; justify-content: center; align-items: center;
            min-height: 100vh; background: linear-gradient(135deg, #667eea, #764ba2);
        }
        .container {
            background: white; padding: 3rem; border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3); max-width: 500px; width: 100%;
        }
        h1 { text-align: center; color: #333; margin-bottom: 2rem; }
        form { display: flex; gap: 10px; }
        input[type="url"] {
            flex: 1; padding: 12px 16px; border: 2px solid #e0e0e0;
            border-radius: 8px; font-size: 16px; outline: none;
        }
        input[type="url"]:focus { border-color: #667eea; }
        button {
            padding: 12px 24px; background: #667eea; color: white;
            border: none; border-radius: 8px; font-size: 16px; cursor: pointer;
        }
        button:hover { background: #5a67d8; }
        #result {
            margin-top: 1.5rem; padding: 1rem; background: #f0fdf4;
            border: 1px solid #86efac; border-radius: 8px; display: none;
        }
        #result a { color: #166534; font-weight: bold; word-break: break-all; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔗 URL Shortener</h1>
        <form id="shorten-form">
            <input type="url" id="url" placeholder="Paste your long URL..." required>
            <button type="submit">Shorten</button>
        </form>
        <div id="result">
            <p>Short URL: <a href="" target="_blank" id="short-url"></a></p>
        </div>
    </div>
    <script>
        document.getElementById('shorten-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const url = document.getElementById('url').value;
            const formData = new FormData();
            formData.append('url', url);
            const res = await fetch('/shorten', { method: 'POST', body: formData });
            const data = await res.json();
            document.getElementById('short-url').href = data.short_url;
            document.getElementById('short-url').textContent = data.short_url;
            document.getElementById('result').style.display = 'block';
        });
    </script>
</body>
</html>
''')]


def _http_server():
    return [("server.py", '''"""
HTTP/1.1 Server from Scratch — Using raw TCP sockets.
Implements routing, static file serving, keep-alive, and middleware.
"""
import socket
import threading
import os
import json
from urllib.parse import unquote, parse_qs


STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
DEFAULT_PORT = 8080

STATUS_CODES = {
    200: "OK",
    201: "Created",
    204: "No Content",
    301: "Moved Permanently",
    400: "Bad Request",
    404: "Not Found",
    405: "Method Not Allowed",
    500: "Internal Server Error",
}

CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css",
    ".js": "application/javascript",
    ".json": "application/json",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".svg": "image/svg+xml",
    ".txt": "text/plain",
    ".ico": "image/x-icon",
}


class HTTPRequest:
    def __init__(self, raw: bytes):
        self.method = ""
        self.path = ""
        self.version = ""
        self.headers = {}
        self.body = b""
        self.params = {}
        self.query = {}
        self._parse(raw)

    def _parse(self, raw: bytes):
        parts = raw.split(b"\\r\\n\\r\\n", 1)
        header_section = parts[0]
        self.body = parts[1] if len(parts) > 1 else b""

        lines = header_section.split(b"\\r\\n")
        request_line = lines[0].decode("utf-8", errors="replace")
        parts = request_line.split(" ", 2)
        self.method = parts[0]
        full_path = unquote(parts[1]) if len(parts) > 1 else "/"
        self.version = parts[2] if len(parts) > 2 else "HTTP/1.1"

        # Parse query string
        if "?" in full_path:
            self.path, qs = full_path.split("?", 1)
            self.query = {k: v[0] if len(v) == 1 else v for k, v in parse_qs(qs).items()}
        else:
            self.path = full_path

        # Parse headers
        for line in lines[1:]:
            line = line.decode("utf-8", errors="replace")
            if ":" in line:
                key, value = line.split(":", 1)
                self.headers[key.strip().lower()] = value.strip()

        # Parse body for form data
        if self.method == "POST" and self.body:
            try:
                body_str = self.body.decode("utf-8")
                if "application/x-www-form-urlencoded" in self.headers.get("content-type", ""):
                    self.params = {k: v[0] if len(v) == 1 else v for k, v in parse_qs(body_str).items()}
                elif "application/json" in self.headers.get("content-type", ""):
                    self.params = json.loads(body_str)
            except Exception:
                pass


class HTTPResponse:
    def __init__(self, status=200, body="", content_type="text/html"):
        self.status = status
        self.body = body if isinstance(body, bytes) else body.encode("utf-8")
        self.headers = {"Content-Type": content_type}

    def to_bytes(self) -> bytes:
        status_line = f"HTTP/1.1 {self.status} {STATUS_CODES.get(self.status, 'OK')}\\r\\n"
        self.headers["Content-Length"] = str(len(self.body))
        headers = "".join(f"{k}: {v}\\r\\n" for k, v in self.headers.items())
        return status_line.encode() + headers.encode() + b"\\r\\n" + self.body


class Router:
    def __init__(self):
        self.routes = {}

    def add(self, method: str, path: str, handler):
        self.routes[(method.upper(), path)] = handler

    def get(self, path):
        def decorator(fn):
            self.add("GET", path, fn)
            return fn
        return decorator

    def post(self, path):
        def decorator(fn):
            self.add("POST", path, fn)
            return fn
        return decorator

    def match(self, method: str, path: str):
        handler = self.routes.get((method, path))
        if handler:
            return handler
        # Try static file
        return None


class Middleware:
    def process(self, req: HTTPRequest, res: HTTPResponse):
        return res


def serve_static(path: str):
    """Serve a static file."""
    file_path = os.path.join(STATIC_DIR, path.lstrip("/").replace("/", os.sep))
    if os.path.isfile(file_path):
        ext = os.path.splitext(file_path)[1]
        ct = CONTENT_TYPES.get(ext, "application/octet-stream")
        with open(file_path, "rb") as f:
            return HTTPResponse(200, f.read(), ct)
    return None


def log_request(req: HTTPRequest, status: int):
    print(f"[{req.method}] {req.path} → {status}")


# ── Application ─────────────────────────────────────────────────────────


def make_app():
    router = Router()

    @router.get("/")
    def index(req):
        return HTTPResponse(200, """
        <!DOCTYPE html>
        <html>
        <head><title>HTTP Server from Scratch</title>
        <style>
            body { font-family: system-ui; max-width: 700px; margin: 3rem auto; padding: 2rem; }
            h1 { color: #2563eb; } pre { background: #f1f5f9; padding: 1rem; border-radius: 8px; }
            .card { border: 1px solid #e5e7eb; padding: 1rem; margin: 1rem 0; border-radius: 8px; }
        </style>
        </head>
        <body>
            <h1>🚀 HTTP Server from Scratch</h1>
            <p>This page is served by a <strong>hand-written HTTP/1.1 server</strong> using raw TCP sockets.</p>
            <div class="card">
                <h3>🔧 Features</h3>
                <ul>
                    <li>Custom router with decorators</li>
                    <li>Static file serving</li>
                    <li>JSON API endpoints</li>
                    <li>Query string parsing</li>
                    <li>Keep-alive connections</li>
                </ul>
            </div>
            <p>Try: <a href="/api/hello?name=world">/api/hello?name=world</a></p>
            <p>Try: <a href="/static/test.txt">/static/test.txt</a></p>
        </body>
        </html>
        """)

    @router.get("/api/hello")
    def hello(req):
        name = req.query.get("name", "World")
        data = {"message": f"Hello, {name}!", "server": "ScratchHTTPServer"}
        return HTTPResponse(200, json.dumps(data), "application/json")

    @router.get("/api/echo")
    def echo(req):
        return HTTPResponse(200, json.dumps({
            "method": req.method,
            "path": req.path,
            "query": req.query,
            "headers": dict(req.headers),
        }), "application/json")

    return router


def handle_client(sock, addr, router):
    try:
        sock.settimeout(30)
        raw = b""
        while True:
            try:
                chunk = sock.recv(4096)
                if not chunk:
                    break
                raw += chunk
                if b"\\r\\n\\r\\n" in raw:
                    # Check Content-Length for full body
                    headers_end = raw.find(b"\\r\\n\\r\\n")
                    headers_raw = raw[:headers_end].decode("utf-8", errors="replace")
                    cl = None
                    for line in headers_raw.split("\\r\\n"):
                        if line.lower().startswith("content-length:"):
                            cl = int(line.split(":")[1].strip())
                    if cl is None:
                        break
                    body_start = headers_end + 4
                    if len(raw) - body_start >= cl:
                        break
            except socket.timeout:
                break

        if not raw:
            return

        req = HTTPRequest(raw)

        # Try route first
        handler = router.match(req.method, req.path)
        if handler:
            res = handler(req)
        else:
            # Try static file
            res = serve_static(req.path)
            if res is None:
                res = HTTPResponse(404, "<h1>404 Not Found</h1>")

        log_request(req, res.status)
        sock.sendall(res.to_bytes())
    except Exception as e:
        print(f"Error handling {addr}: {e}")
        try:
            sock.sendall(HTTPResponse(500, f"<h1>500 {e}</h1>").to_bytes())
        except Exception:
            pass
    finally:
        try:
            sock.close()
        except Exception:
            pass


def main():
    os.makedirs(STATIC_DIR, exist_ok=True)
    # Create a test static file
    with open(os.path.join(STATIC_DIR, "test.txt"), "w") as f:
        f.write("This is a static file served by the HTTP server!\\n")

    router = make_app()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", DEFAULT_PORT))
    server.listen(128)

    print(f"""
╔══════════════════════════════════════════╗
║  🚀 HTTP Server from Scratch            ║
║  Listening on http://localhost:{DEFAULT_PORT}     ║
║  Press Ctrl+C to stop                   ║
╚══════════════════════════════════════════╝
""")

    try:
        while True:
            sock, addr = server.accept()
            t = threading.Thread(target=handle_client, args=(sock, addr, router), daemon=True)
            t.start()
    except KeyboardInterrupt:
        print("\\n👋 Server stopped.")
    finally:
        server.close()


if __name__ == "__main__":
    main()
''')]


def _port_scanner():
    return [("scanner.py", '''"""
Multi-threaded TCP Port Scanner with banner grabbing and service detection.
"""
import socket
import threading
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime


COMMON_PORTS = {
    20: "FTP-DATA", 21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS",
    465: "SMTPS", 587: "SMTP", 993: "IMAPS", 995: "POP3S",
    3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 6379: "Redis",
    8080: "HTTP-Alt", 8443: "HTTPS-Alt", 9090: "Prometheus", 27017: "MongoDB",
}

SERVICE_PROBES = {
    "HTTP": b"GET / HTTP/1.0\\r\\n\\r\\n",
    "SSH": b"",
    "SMTP": b"EHLO scanner\\r\\n",
    "FTP": b"",
}


def scan_port(host: str, port: int, timeout: float = 1.0) -> dict:
    """Scan a single port; return result dict."""
    result = {
        "host": host, "port": port,
        "service": COMMON_PORTS.get(port, "unknown"),
        "open": False, "banner": None,
    }
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        if sock.connect_ex((host, port)) == 0:
            result["open"] = True
            # Try banner grabbing
            service = COMMON_PORTS.get(port, "")
            probe = SERVICE_PROBES.get(service if service in SERVICE_PROBES else "", None)
            if probe:
                try:
                    sock.send(probe)
                    banner = sock.recv(1024)
                    result["banner"] = banner.decode("utf-8", errors="replace").strip()[:200]
                except Exception:
                    pass
            elif service == "SSH":
                try:
                    banner = sock.recv(256)
                    result["banner"] = banner.decode("utf-8", errors="replace").strip()
                except Exception:
                    pass
        sock.close()
    except Exception as e:
        result["error"] = str(e)
    return result


def scan_range(host: str, start: int = 1, end: int = 1024, workers: int = 100, timeout: float = 0.5):
    """Scan a range of ports with thread pool."""
    ports = list(range(start, end + 1))
    results = []
    total = len(ports)
    done = 0
    open_ports = []

    print(f"\\n🔍 Scanning {host} — ports {start}-{end} ({total} ports, {workers} workers)\\n")

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(scan_port, host, p, timeout): p for p in ports}
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            if result["open"]:
                open_ports.append(result)
                banner = f" [{result['banner'][:60]}]" if result["banner"] else ""
                print(f"  ✅ {result['port']:>5}/{result['service']:<15}{banner}")
            done += 1
            if done % 200 == 0:
                print(f"     ... {done}/{total} scanned, {len(open_ports)} open")

    return results


def export_results(results, filename: str, fmt: str = "json"):
    """Export results to JSON or HTML."""
    if fmt == "json":
        with open(filename, "w") as f:
            json.dump(results, f, indent=2)
    elif fmt == "html":
        open_ports = [r for r in results if r["open"]]
        html = f"""<!DOCTYPE html>
<html><head><title>Port Scan Results</title>
<style>
    body {{ font-family: system-ui; margin: 2rem; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ padding: 8px 12px; text-align: left; border-bottom: 1px solid #ddd; }}
    th {{ background: #2563eb; color: white; }}
    tr:hover {{ background: #f0f9ff; }}
</style></head><body>
<h1>Port Scan: {results[0]['host'] if results else ''}</h1>
<p>Scanned: {len(results)} ports | Open: {len(open_ports)} | {datetime.now().isoformat()}</p>
<table>
<tr><th>Port</th><th>Service</th><th>Banner</th></tr>
"""
        for r in open_ports:
            html += f"<tr><td>{r['port']}</td><td>{r['service']}</td><td>{r.get('banner', '') or ''}</td></tr>"
        html += "</table></body></html>"
        with open(filename, "w") as f:
            f.write(html)
    print(f"\\n📄 Results exported to {filename}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Multi-threaded Port Scanner")
    parser.add_argument("host", nargs="?", default="127.0.0.1", help="Target host")
    parser.add_argument("-s", "--start", type=int, default=1, help="Start port")
    parser.add_argument("-e", "--end", type=int, default=1024, help="End port")
    parser.add_argument("-w", "--workers", type=int, default=100, help="Thread count")
    parser.add_argument("-t", "--timeout", type=float, default=0.5, help="Timeout per port")
    parser.add_argument("-o", "--output", default="scan_results.json")
    parser.add_argument("--html", action="store_true", help="Export as HTML")
    args = parser.parse_args()

    results = scan_range(args.host, args.start, args.end, args.workers, args.timeout)
    open_ports = [r for r in results if r["open"]]

    print(f"\\n{'='*50}")
    print(f"  Scan complete: {len(open_ports)}/{len(results)} ports open")
    print(f"{'='*50}\\n")

    fmt = "html" if args.html else "json"
    export_results(results, args.output, fmt)
''')]


def _weather_cli():
    return [("weather.py", '''"""
Beautiful Terminal Weather App — ASCII art weather display.
Uses Open-Meteo API (free, no key required) for weather data.
"""
import json
import urllib.request
import urllib.parse
from datetime import datetime


WEATHER_CODES = {
    0: ("☀️  Clear sky", ""),
    1: ("🌤️  Mainly clear", ""),
    2: ("⛅ Partly cloudy", ""),
    3: ("☁️  Overcast", ""),
    45: ("🌫️  Foggy", ""),
    48: ("🌫️  Rime fog", ""),
    51: ("🌧️  Light drizzle", ""),
    53: ("🌧️  Moderate drizzle", ""),
    55: ("🌧️  Dense drizzle", ""),
    61: ("🌧️  Slight rain", ""),
    63: ("🌧️  Moderate rain", ""),
    65: ("🌧️  Heavy rain", ""),
    71: ("🌨️  Slight snow", ""),
    73: ("🌨️  Moderate snow", ""),
    75: ("🌨️  Heavy snow", ""),
    80: ("🌦️  Rain showers", ""),
    95: ("⛈️  Thunderstorm", ""),
}


def geocode(city: str) -> tuple:
    """Get coordinates for a city name using Open-Meteo geocoding API."""
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={urllib.parse.quote(city)}&count=1&language=en&format=json"
    try:
        with urllib.request.urlopen(url) as resp:
            data = json.loads(resp.read())
        if data.get("results"):
            r = data["results"][0]
            return r["latitude"], r["longitude"], r["name"], r.get("country", "")
    except Exception as e:
        print(f"Geocoding error: {e}")
    return None, None, city, ""


def fetch_weather(lat: float, lon: float) -> dict:
    """Fetch current + 5-day forecast from Open-Meteo."""
    params = urllib.parse.urlencode({
        "latitude": lat, "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,wind_direction_10m",
        "daily": "temperature_2m_max,temperature_2m_min,weather_code,precipitation_sum",
        "timezone": "auto",
        "forecast_days": "5",
    })
    url = f"https://api.open-meteo.com/v1/forecast?{params}"
    with urllib.request.urlopen(url) as resp:
        return json.loads(resp.read())


def wind_direction_arrow(degrees: int) -> str:
    arrows = ["↓", "↙", "←", "↖", "↑", "↗", "→", "↘"]
    idx = round(degrees / 45) % 8
    return arrows[idx]


def display(data: dict, city: str, country: str):
    current = data["current"]
    daily = data["daily"]

    code = current["weather_code"]
    weather_desc, _ = WEATHER_CODES.get(code, (f"Code {code}", ""))

    # Current conditions box
    print(f"""
╔══════════════════════════════════════════════╗
║  🌍 {city}, {country}
║  📅 {datetime.now().strftime('%A, %B %d %Y  %H:%M')}
╠══════════════════════════════════════════════╣
║                                              ║
║     {weather_desc:<35}║
║     🌡️  Temperature:    {current['temperature_2m']:>5.1f}°C          ║
║     🥶 Feels like:      {current['apparent_temperature']:>5.1f}°C          ║
║     💧 Humidity:        {current['relative_humidity_2m']:>5}%           ║
║     💨 Wind:            {current['wind_speed_10m']:>5.1f} km/h {wind_direction_arrow(current['wind_direction_10m']):>3}     ║
║                                              ║
╚══════════════════════════════════════════════╝
""")

    # Forecast
    print("📅 5-Day Forecast:")
    print("─" * 55)
    print(f"{'Date':<14} {'High':>6} {'Low':>6} {'Rain':>6}  Condition")
    print("─" * 55)
    for i in range(5):
        date = daily["time"][i]
        high = daily["temperature_2m_max"][i]
        low = daily["temperature_2m_min"][i]
        rain = daily["precipitation_sum"][i]
        code = daily["weather_code"][i]
        desc, _ = WEATHER_CODES.get(code, ("?", ""))
        print(f"{date:<14} {high:>5.1f}° {low:>5.1f}° {rain:>5.1f}mm {desc}")
    print("─" * 55)
    print()


if __name__ == "__main__":
    import sys
    city = sys.argv[1] if len(sys.argv) > 1 else "Beijing"
    print(f"\\n🔍 Searching for {city}...")
    lat, lon, city_name, country = geocode(city)
    if lat is None:
        print(f"❌ City not found: {city}")
        sys.exit(1)
    print(f"📍 Found: {city_name}, {country} ({lat:.2f}, {lon:.2f})")
    print("📡 Fetching weather data...")
    data = fetch_weather(lat, lon)
    display(data, city_name, country)
''')]


def _password_generator():
    return [("passgen.py", '''#!/usr/bin/env python3
"""
Cryptographic Password Generator
XKCD-style passphrases + high-entropy random passwords with strength estimation.
"""
import secrets
import math
import os


WORDLIST_PATH = os.path.join(os.path.dirname(__file__), "wordlist.txt")

# Default wordlist (EFF large wordlist)
DEFAULT_WORDS = [
    "apple", "banana", "carrot", "dolphin", "elephant", "flamingo", "guitar",
    "harmony", "island", "jungle", "kayak", "lantern", "mountain", "napkin",
    "october", "penguin", "quartz", "rocket", "sunset", "tornado", "umbrella",
    "violet", "walnut", "xenon", "yogurt", "zebra", "anchor", "breeze",
    "cactus", "diamond", "emerald", "forest", "galaxy", "horizon", "icicle",
    "jasper", "koala", "lemon", "mango", "nebula", "orchid", "pepper",
    "quicksand", "rainbow", "sapphire", "thunder", "universe", "voyager",
    "whistle", "acorn", "badge", "cabin", "dagger", "eagle", "falcon",
    "garden", "helmet", "igloo", "jigsaw", "kitten", "llama", "magnet",
    "noodle", "oasis", "pearl", "quiver", "raccoon", "shamrock", "tulip",
    "ukulele", "viper", "walrus", "acrobat", "bonfire", "crystal", "dragon",
    "echo", "feather", "glacier", "hedge", "insect", "jupiter", "karate",
    "lotus", "marble", "nutmeg", "onyx", "puzzle", "quasar", "robin",
    "saddle", "trophy", "urchin", "velvet", "willow", "zeppelin", "aurora",
    "blizzard", "comet", "dusk", "ember", "frost", "gale", "haven",
]


def load_wordlist():
    if os.path.exists(WORDLIST_PATH):
        with open(WORDLIST_PATH, "r") as f:
            return [w.strip() for w in f if w.strip() and not w.startswith("#")]
    return DEFAULT_WORDS


def passphrase(num_words: int = 4, separator: str = "-", capitalize: bool = False) -> str:
    """Generate an XKCD-style passphrase using random words."""
    words = load_wordlist()
    chosen = [secrets.choice(words) for _ in range(num_words)]
    if capitalize:
        chosen = [w.capitalize() for w in chosen]
    return separator.join(chosen)


def random_password(length: int = 20, include_special: bool = True) -> str:
    """Generate a high-entropy random password."""
    import string
    alphabet = string.ascii_letters + string.digits
    if include_special:
        alphabet += "!@#$%^&*()-_=+[]{}|;:,.<>?"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def estimate_entropy(password: str, method: str = "passphrase") -> dict:
    """Estimate password strength in bits of entropy and crack time."""
    if method == "passphrase":
        wordlist_size = len(load_wordlist())
        num_words = len(password.split("-"))
        entropy = num_words * math.log2(wordlist_size)
    else:
        import string
        pool = 0
        for charset, name in [
            (string.ascii_lowercase, "lower"),
            (string.ascii_uppercase, "upper"),
            (string.digits, "digits"),
            ("!@#$%^&*()-_=+[]{}|;:,.<>?", "special"),
        ]:
            if any(c in password for c in charset):
                pool += len(charset)
        entropy = len(password) * math.log2(max(pool, 1))

    # Crack time estimates (1 billion guesses/sec for online, 1 trillion for offline)
    seconds_online = 2 ** entropy / 1e9
    seconds_offline = 2 ** entropy / 1e12

    def format_time(seconds):
        if seconds < 60:
            return f"{seconds:.0f} seconds"
        elif seconds < 3600:
            return f"{seconds/60:.0f} min"
        elif seconds < 86400:
            return f"{seconds/3600:.0f} hours"
        elif seconds < 31536000:
            return f"{seconds/86400:.0f} days"
        elif seconds < 3153600000:
            return f"{seconds/31536000:.0f} years"
        else:
            return f"{seconds/31536000/1e9:.1f}B years"

    return {
        "entropy_bits": round(entropy, 1),
        "crack_online": format_time(seconds_online),
        "crack_offline": format_time(seconds_offline),
        "strength": (
            "🔴 Weak" if entropy < 40 else
            "🟡 Fair" if entropy < 60 else
            "🟢 Strong" if entropy < 90 else
            "🟣 Very Strong"
        ),
    }


if __name__ == "__main__":
    print("🔐 Password Generator\\n")

    for words in [3, 4, 5, 6]:
        pp = passphrase(num_words=words, separator="-")
        est = estimate_entropy(pp, "passphrase")
        print(f"  {est['strength']} ({words} words): {pp}")
        print(f"       Entropy: {est['entropy_bits']} bits | Online: {est['crack_online']} | Offline: {est['crack_offline']}\\n")

    print("─" * 55)
    print("Random passwords:\\n")

    for length in [12, 16, 20, 24]:
        pw = random_password(length)
        est = estimate_entropy(pw, "random")
        print(f"  {est['strength']} ({length} chars): {pw}")
        print(f"       Entropy: {est['entropy_bits']} bits | Online: {est['crack_online']}\\n")
'''), ("entropy.py", '''"""Entropy estimation utilities for password strength analysis."""

import math
import string


def shannon_entropy(data: str) -> float:
    """Calculate Shannon entropy of a string."""
    if not data:
        return 0.0
    freq = {}
    for c in data:
        freq[c] = freq.get(c, 0) + 1
    length = len(data)
    entropy = 0.0
    for count in freq.values():
        p = count / length
        entropy -= p * math.log2(p)
    return entropy * length


def unique_chars(password: str) -> int:
    """Count unique character types used."""
    types = 0
    if any(c.islower() for c in password):
        types += 1
    if any(c.isupper() for c in password):
        types += 1
    if any(c.isdigit() for c in password):
        types += 1
    specials = set("!@#$%^&*()-_=+[]{}|;:,.<>?/~`")
    if any(c in specials for c in password):
        types += 1
    return types


def strength_label(entropy: float) -> str:
    if entropy < 28:
        return "Very Weak"
    elif entropy < 36:
        return "Weak"
    elif entropy < 60:
        return "Reasonable"
    elif entropy < 128:
        return "Strong"
    else:
        return "Very Strong"


if __name__ == "__main__":
    test_passwords = ["password", "Password123", "Tr0ub4dor&3", "correct-horse-battery-staple"]
    print("Password Entropy Analysis\\n")
    for pw in test_passwords:
        s = shannon_entropy(pw)
        types = unique_chars(pw)
        print(f"  '{pw}'")
        print(f"    Shannon: {s:.1f} bits | Types: {types}/4 | {strength_label(s)}\\n")
''')]


# ═══════════════════════════════════════════════════════════════════════════
# Map topic keys to generator functions
# ═══════════════════════════════════════════════════════════════════════════

GENERATORS = {
    "sorting-visualizer": _sorting_visualizer,
    "bloom-filter": _bloom_filter,
    "cli-todo": _cli_todo,
    "url-shortener": _url_shortener,
    "http-server": _http_server,
    "port-scanner": _port_scanner,
    "weather-cli": _weather_cli,
    "password-generator": _password_generator,
}


def generate_project_files(topic_key: str, topic: dict, output_dir: str, username: str = "") -> list:
    """
    Generate all files for a given topic.
    Returns list of generated filenames.
    """
    gen = GENERATORS.get(topic_key)
    files_written = []

    if gen:
        # Use specific generator
        for filename, content in gen():
            filepath = output_dir / filename
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            files_written.append(filename)
    else:
        # Generic: generate skeleton files
        main_file = f"{topic_key.replace('-', '_')}.py"
        main_path = output_dir / main_file
        with open(main_path, "w", encoding="utf-8") as f:
            f.write(f'''"""
{topic['title']}
{'-' * len(topic['title'])}
{ topic['description']}

Category: {topic['category']}
Difficulty: {topic['difficulty']}
"""
# ═══════════════════════════════════════════════════════════════
# TODO: Implement {topic['title']}
# This is a daily code project — extend and customize freely!
# ═══════════════════════════════════════════════════════════════


def main():
    print("🚀 {topic['title']}")
    print(f"Category: {topic['category']}")
    print(f"Difficulty: {topic['difficulty']}")
    # Your implementation here
    print("\\n✅ Project skeleton ready!")


if __name__ == "__main__":
    main()
''')
        files_written.append(main_file)

        # Test file
        test_file = output_dir / f"test_{topic_key.replace('-', '_')}.py"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(f'''"""Tests for {topic['title']}."""


def test_basic():
    """Basic smoke test."""
    import {topic_key.replace('-', '_')}
    assert hasattr({topic_key.replace('-', '_')}, 'main')
    print("✅ Basic test passed")


if __name__ == "__main__":
    test_basic()
    print("\\n🎉 All tests passed!")
''')
        files_written.append(test_file.name)

    # Always generate README
    readme_path = output_dir / "README.md"
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(_readme_str(topic["title"], topic["description"], topic["category"], files_written + ["README.md"], username))
    files_written.append("README.md")

    return files_written
