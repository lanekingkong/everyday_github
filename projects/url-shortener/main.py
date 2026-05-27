"""
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
    print("\n🔗 URL Shortener starting...")
    print(f"   Open {BASE_URL} in your browser\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
