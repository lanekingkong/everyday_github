"""
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

    print(f"\n{'─' * 70}")
    print(f"{'ID':<5} {'Status':<6} {'Prio':<5} {'Task':<30} {'Project':<12} {'Due':<12}")
    print(f"{'─' * 70}")

    for row in rows:
        id_, task, proj, prio, due, done = row
        status = "✅" if done else "⬜"
        prio_str = {1: "⬇️ ", 2: "📌", 3: "🔥"}.get(prio, "  ")
        print(f"{id_:<5} {status:<6} {prio_str:<5} {task[:28]:<30} {proj[:10]:<12} {due or '':<12}")
    print(f"{'─' * 70}\n")


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

    print(f"\n📊 Stats: {total} total | {done} done | {pending} pending | "
          f"{due_today} due today | {overdue} overdue\n")


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
    print("\n📋 Terminal Todo App")
    print("Type 'help' for commands, 'quit' to exit.\n")

    while True:
        try:
            cmd = input("todo> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Bye!")
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
