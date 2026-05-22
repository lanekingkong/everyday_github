#!/usr/bin/env python3
"""
Multi-Platform Setup Helper
============================
Guides you through setting up accounts and API tokens for all platforms.
Run this script to configure your publishing pipeline.

Usage:
    python setup-platforms.py
"""

import os
import json
import sys
from pathlib import Path

CONFIG_FILE = Path(__file__).parent.parent / ".platform-config.json"

PLATFORMS = {
    "dev.to": {
        "url": "https://dev.to/settings/extensions",
        "env_var": "DEVTO_API_KEY",
        "instruction": """
🔗 dev.to API Key
──────────────────────────────
1. 打开: https://dev.to/settings/extensions
2. 向下滚动到 "DEV API Keys"
3. 输入描述名称 (如 "daily-code-bot")
4. 点击 "Generate API Key"
5. 复制生成的 Token 并粘贴到下面
        """,
    },
    "hashnode": {
        "url": "https://hashnode.com/settings/developer",
        "env_var": "HASHNODE_TOKEN",
        "instruction": """
📝 Hashnode Personal Access Token
──────────────────────────────────
1. 打开: https://hashnode.com/settings/developer
2. 点击 "Generate Token"
3. 点击眼睛图标 显示并复制 Token
4. 粘贴到下面
        """,
    },
    "hashnode_publication": {
        "url": "https://hashnode.com/dashboard",
        "env_var": "HASHNODE_PUBLICATION_ID",
        "instruction": """
📰 Hashnode Publication ID
────────────────────────────
1. 在 Hashnode 创建 Blog (如已创建则跳过)
2. 进入 Blog Dashboard
3. URL 类似于: https://hashnode.com/{PUB_ID}/dashboard
4. 复制 {PUB_ID} 部分并粘贴到下面
        """,
    },
    "forg.to": {
        "url": "https://forg.to",
        "env_var": None,
        "instruction": """
🌐 forg.to Profile
───────────────────
1. 打开: https://forg.to
2. 用 GitHub 账号登录 (OAuth 连接)
3. 你的资料库会自动从 GitHub 拉取项目
4. profile URL: https://forg.to/@lanekingkong
        """,
    },
    "peerlist": {
        "url": "https://peerlist.io",
        "env_var": None,
        "instruction": """
💼 Peerlist Profile
────────────────────
1. 打开: https://peerlist.io
2. 用 GitHub 注册/登录
3. 填写个人信息 (作品集会自动同步 GitHub repos)
4. profile URL: https://peerlist.io/lanekingkong
        """,
    },
}


def main():
    print("""
╔══════════════════════════════════════════════╗
║  🔧 多平台发布配置助手                        ║
╚══════════════════════════════════════════════╝

此脚本将帮助你配置所有开发者平台的 API Token。
这些 Token 用于自动化发布每日代码项目。

""")

    config = {}
    if CONFIG_FILE.exists():
        config = json.loads(CONFIG_FILE.read_text())
        print("📂 已找到已有配置\n")

    for name, info in PLATFORMS.items():
        print(f"\n{'─' * 50}")
        print(info["instruction"])

        if info["env_var"] is None:
            input("按 Enter 确认已完成...")
            continue

        existing = config.get(info["env_var"], "")
        masked = f"(已配置: ...{existing[-4:]})" if existing else "(未配置)"

        value = input(f"\n👉 {info['env_var']} {masked}: ").strip()

        if value:
            config[info["env_var"]] = value
            print(f"   ✅ {name} Token 已保存")
        elif existing:
            print(f"   ⚪ 保留已有配置")
        else:
            print(f"   ⚠️  跳过 (稍后可手动设置)")

    # Save config
    CONFIG_FILE.write_text(json.dumps(config, indent=2, ensure_ascii=False))
    print(f"\n✅ 配置已保存到: {CONFIG_FILE}")

    # Print export commands
    print(f"\n{'='*50}")
    print("📋 环境变量设置命令 (添加到 ~/.bashrc 或 ~/.zshrc):\n")
    for key, value in config.items():
        print(f'export {key}="{value}"')

    print(f"\n{'='*50}")
    print("""
🚀 配置完成后的使用方式:

  # 一键发布当天项目到所有平台:
  bash multi-platform/publish.sh projects/<项目> --all

  # 只发布到 dev.to:
  bash multi-platform/publish.sh projects/<项目> --devto

  # 只生成社交媒体帖子:
  bash multi-platform/publish.sh projects/<项目> --social
""")


if __name__ == "__main__":
    main()
