# ═══════════════════════════════════════════════════════════════
# 自动化商业版图 · 完整操作手册
# Automated Portfolio Business Blueprint
# ═══════════════════════════════════════════════════════════════
#
# 目标：利用自动化工具，每天生成并发布一个真实的代码项目，
#       同步到多个开发者平台，积累作品集和个人品牌。

# ═══════════════════════════════════════════════════════════════
# 📋 第一步：一次性初始化设置
# ═══════════════════════════════════════════════════════════════

# 1. 在 GitHub 创建两个仓库：
#    - daily-code          （存放每日生成的代码项目）
#    - <你的用户名>         （GitHub Profile README 仓库）

# 2. 配置 Git
git config --global user.name "你的名字"
git config --global user.email "你的邮箱@example.com"

# 3. 复制本项目到你的工作目录
#    (已在 C:\Users\29712\dev-portfolio-automation\)

# 4. 将 daily-code-generator 推送到你的 daily-code 仓库
#    cd dev-portfolio-automation
#    git init
#    git add .
#    git commit -m "Initial: dev portfolio automation system"
#    git remote add origin https://github.com/<你的用户名>/daily-code.git
#    git push -u origin main

# 5. 配置 GitHub Actions Secrets（在仓库 Settings > Secrets > Actions）：
#    - GIT_USER_NAME: 你的 Git 用户名
#    - GIT_USER_EMAIL: 你的 Git 邮箱

# 6. 在各平台创建账号并获取 API Token：
#    - dev.to:    https://dev.to/settings/extensions → DEVTO_API_KEY
#    - Hashnode:  https://hashnode.com/settings/developer → HASHNODE_TOKEN
#    - forg.to:   https://forg.to → 连接 GitHub 即可自动聚合
#    - Peerlist:  https://peerlist.io → 注册并填写资料

# ═══════════════════════════════════════════════════════════════
# 📅 第二步：自动化流水线（无需人工干预）
# ═══════════════════════════════════════════════════════════════

# GitHub Actions 会每天自动：
# 1. 07:37 UTC 触发 daily-project.yml
# 2. 运行 generate.py → 选择一个主题 → 生成完整代码 → 创建 README
# 3. 自动 commit + push 到 daily-code 仓库
# 4. GitHub 绿墙自动更新

# ═══════════════════════════════════════════════════════════════
# 🚀 第三步：手动发布到各平台（每天 5 分钟）
# ═══════════════════════════════════════════════════════════════

# 发布今天生成的项目到所有平台：
cd dev-portfolio-automation
bash multi-platform/publish.sh daily-output/<今天生成的项目> --all

# 或分平台发布：
bash multi-platform/publish.sh daily-output/<项目> --devto
bash multi-platform/publish.sh daily-output/<项目> --hashnode
bash multi-platform/publish.sh daily-output/<项目> --social

# ═══════════════════════════════════════════════════════════════
# 📊 第四步：发布到 Product Hunt 等平台（每周/每月精选）
# ═══════════════════════════════════════════════════════════════

# 当你有较成熟的项目时，发布到：
# - Product Hunt: https://www.producthunt.com/launches/new
# - Indie Hackers: https://www.indiehackers.com/
# - BetaList: https://betalist.com/
# - Hacker News (Show HN): https://news.ycombinator.com/
# - Peerlist: https://peerlist.io/
# - Uneed: https://uneed.best/
# - MicroLaunch: https://microlaunch.net/

# ═══════════════════════════════════════════════════════════════
# 💰 第五步：变现路径（当作品集足够丰富后）
# ═══════════════════════════════════════════════════════════════

# 路径 A：接单/自由职业
# - 在作品集中标注 "Available for hire"
# - 平台：Upwork, Toptal, Freelancer, 程序员客栈, 猪八戒
# - 用你的 daily-code 作为能力证明

# 路径 B：内容创作变现
# - 将每日项目写成教程发表在 dev.to / Hashnode → 吸引流量
# - 开启 dev.to 赞助、Hashnode 付费订阅
# - YouTube/B站：录制每日项目的构建过程

# 路径 C：SaaS 产品化
# - 从 daily-code 中挑选有价值的项目进行深度开发
# - 部署为 SaaS 服务（Vercel/Railway/Fly.io 免费额度起步）
# - 在 Product Hunt 上发布 → 获取早期用户

# 路径 D：开源赞助
# - GitHub Sponsors: 好的 daily-code 项目可以吸引赞助
# - Open Collective: 为你的开源项目接受捐赠
# - Polar.sh: 开源项目的付费 issue

# 路径 E：求职跳槽
# - 365 天不间断的代码产出是最好的简历
# - 在简历上写 "365 consecutive days of shipping"
# - forg.to 个人主页作为作品集链接发给 HR

# ═══════════════════════════════════════════════════════════════
# 📅 第六步：月度/季度复利活动
# ═══════════════════════════════════════════════════════════════

# 每月：
# - 挑选本月最佳项目，深度打磨后发布到 Product Hunt
# - 写一篇月度总结博客（"这个月我学到了什么"）
# - 在 Reddit (r/programming, r/Python) 分享最有价值的项目

# 每季度：
# - 整理一个 "季度精选合集" 
# - 投稿到技术周刊（Python Weekly, JavaScript Weekly 等）
# - 参加 Hackathon，用 daily-code 中的项目作为基础

# ═══════════════════════════════════════════════════════════════
# 📈 关键指标追踪
# ═══════════════════════════════════════════════════════════════

# GitHub:
# - 连续提交天数 (streak)
# - Star 数量增长
# - Fork 数量

# dev.to:
# - 文章阅读量、点赞、评论
# - 粉丝增长

# 变现:
# - 接单收入
# - 赞助收入
# - SaaS MRR
