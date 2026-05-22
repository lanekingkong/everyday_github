#!/usr/bin/env python3
"""
Daily Code Project Generator
=============================
Automatically creates a complete, working mini-project each day,
commits it, and pushes to GitHub.

Strategy:
- Rotates through categories to keep variety
- Generates real, runnable code (not placeholder stubs)
- Each project has its own README
- Respects weekends (lighter projects only)
"""

import os
import sys
import json
import random
import hashlib
from datetime import datetime, date
from pathlib import Path

from topics import TOPICS
from templates import generate_project_files

# === CONFIGURATION ===
REPO_ROOT = Path(__file__).parent.parent  # everyday_github
OUTPUT_DIR = REPO_ROOT / "projects"
PROJECT_INDEX = OUTPUT_DIR / "projects.json"
LOG_FILE = OUTPUT_DIR / "generator.log"

# GitHub config — set via env vars or git config
GIT_USER_NAME = os.environ.get("GIT_USER_NAME", "Daily Code Bot")
GIT_USER_EMAIL = os.environ.get("GIT_USER_EMAIL", "daily-bot@users.noreply.github.com")
GITHUB_USERNAME = os.environ.get("GITHUB_USERNAME", "lanekingkong")


def log(msg: str) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    try:
        print(line)
    except UnicodeEncodeError:
        print(line.encode("ascii", errors="replace").decode("ascii"))
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def load_index() -> dict:
    if PROJECT_INDEX.exists():
        with open(PROJECT_INDEX, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"projects": [], "last_date": None, "category_counts": {}}


def save_index(index: dict) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(PROJECT_INDEX, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)


def is_weekend() -> bool:
    return date.today().weekday() >= 5


def pick_topic(index: dict) -> str:
    """Pick next topic with smart rotation across categories."""
    projects_done = index["projects"]
    category_counts = index.get("category_counts", {})

    # Build weighted pool: prefer categories we haven't done recently
    available = list(TOPICS.keys())
    random.shuffle(available)

    if is_weekend():
        # Lighter topics on weekends (beginner difficulty)
        available = [k for k in available if TOPICS[k]["difficulty"] == "beginner"]
        if not available:
            available = list(TOPICS.keys())

    # Avoid repeating recent 15 projects
    recent = set(projects_done[-15:]) if projects_done else set()
    candidates = [k for k in available if k not in recent]

    if not candidates:
        candidates = available

    # Prefer categories with lowest count
    def category_score(topic_key: str) -> int:
        cat = TOPICS[topic_key]["category"]
        return category_counts.get(cat, 0)

    candidates.sort(key=category_score)

    # Pick from top 5 lowest-count categories (adds variety)
    pool = candidates[:max(5, len(candidates) // 3)]
    chosen = random.choice(pool)

    return chosen


def make_commit_message(topic_key: str) -> str:
    topic = TOPICS[topic_key]
    emoji_map = {
        "Algorithms": "🧮",
        "Data Structures": "📊",
        "System Design": "🏗️",
        "Utilities": "🔧",
        "Mini Apps": "📱",
        "Web Scraping": "🕷️",
        "API Wrappers": "🔌",
        "DevOps": "⚙️",
        "Data Science": "📈",
        "Games": "🎮",
        "Networking": "🌐",
        "Databases": "🗄️",
    }
    emoji = emoji_map.get(topic["category"], "💻")
    return f"{emoji} Daily: {topic['title']} [{topic['category']}]"


def run():
    log("=" * 50)
    log("Daily Code Generator starting...")

    today = date.today().isoformat()
    index = load_index()

    if index.get("last_date") == today:
        log(f"Already generated today ({today}). Skipping.")
        return

    # Pick topic
    topic_key = pick_topic(index)
    topic = TOPICS[topic_key]
    log(f"Selected topic: {topic_key} — {topic['title']} [{topic['category']}]")

    # Create project directory
    project_dir = OUTPUT_DIR / topic_key
    project_dir.mkdir(parents=True, exist_ok=True)

    # Generate files
    try:
        files_generated = generate_project_files(topic_key, topic, project_dir, GITHUB_USERNAME)
        log(f"Generated {len(files_generated)} files: {', '.join(files_generated)}")
    except Exception as e:
        log(f"ERROR generating files: {e}")
        raise

    # Update index
    index["projects"].append(topic_key)
    index["last_date"] = today
    cat = topic["category"]
    index["category_counts"][cat] = index["category_counts"].get(cat, 0) + 1
    save_index(index)

    # Prepare git commit info
    commit_msg = make_commit_message(topic_key)

    # Write git commit info for GitHub Actions to use
    commit_info = {
        "topic_key": topic_key,
        "commit_message": commit_msg,
        "date": today,
        "project_dir": str(project_dir),
    }
    commit_info_path = OUTPUT_DIR / "commit_info.json"
    with open(commit_info_path, "w") as f:
        json.dump(commit_info, f, indent=2)

    log(f"Done! Topic: {topic_key}, Commit msg: {commit_msg}")
    log("=" * 50)

    # Print summary
    try:
        print(f"\n{'='*50}")
        print(f"  Today's Project: {topic['title']}")
        print(f"  Category:        {topic['category']}")
        print(f"  Difficulty:      {topic['difficulty']}")
        print(f"  Language:        {topic['language']}")
        print(f"  Files:           {', '.join(files_generated)}")
        print(f"  Output:          {project_dir}")
        print(f"  Total projects:  {len(index['projects'])}")
        print(f"{'='*50}\n")
    except UnicodeEncodeError:
        pass


if __name__ == "__main__":
    run()
