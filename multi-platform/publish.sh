#!/bin/bash
# ═══════════════════════════════════════════════════════════════════
# Multi-Platform Portfolio Publisher
# ═══════════════════════════════════════════════════════════════════
# Publishes your latest project to multiple platforms.
#
# Usage:
#   ./publish.sh <project_dir> [platforms]
#
# Platforms:
#   --devto     → dev.to (via API)
#   --hashnode  → hashnode (via API)
#   --peerlist  → peerlist (manual link generation)
#   --forgto    → forg.to profile update
#   --all       → all of the above
#   --social    → X/Twitter + LinkedIn posts
#
# Prerequisites:
#   - DEVTO_API_KEY env var
#   - HASHNODE_TOKEN env var
#   - gh CLI for GitHub
# ═══════════════════════════════════════════════════════════════════

set -euo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

log()  { echo -e "${GREEN}[✓]${NC} $1"; }
warn() { echo -e "${CYAN}[→]${NC} $1"; }
err()  { echo -e "${RED}[✗]${NC} $1"; }

PROJECT_DIR="${1:-}"
PLATFORM="${2:---all}"

if [ -z "$PROJECT_DIR" ]; then
    echo "Usage: ./publish.sh <project_dir> [--all|--devto|--hashnode|--social]"
    exit 1
fi

if [ ! -d "$PROJECT_DIR" ]; then
    err "Project directory not found: $PROJECT_DIR"
    exit 1
fi

# Read project info
README_PATH="$PROJECT_DIR/README.md"
if [ -f "$README_PATH" ]; then
    TITLE=$(head -1 "$README_PATH" | sed 's/^# //')
    DESC=$(sed -n '3p' "$README_PATH" | sed 's/^> //')
else
    TITLE=$(basename "$PROJECT_DIR")
    DESC="Daily code project"
fi

log "Publishing: $TITLE"

# ── dev.to ─────────────────────────────────────────────────────────────────
publish_devto() {
    warn "Publishing to dev.to..."

    if [ -z "${DEVTO_API_KEY:-}" ]; then
        err "DEVTO_API_KEY not set. Get one at https://dev.to/settings/extensions"
        return 1
    fi

    # Generate article content from README
    BODY=$(cat "$README_PATH" | sed 's/^/    /')
    CODE_BLOCK=""

    # Find main code file
    MAIN_PY=$(find "$PROJECT_DIR" -name "*.py" -not -name "test_*" | head -1)
    if [ -n "$MAIN_PY" ]; then
        CODE_BLOCK="\n## Code\n\n\`\`\`python\n$(cat "$MAIN_PY" | head -80)\n\`\`\`\n"
    fi

    # Create article via dev.to API
    curl -s -X POST "https://dev.to/api/articles" \
        -H "Content-Type: application/json" \
        -H "api-key: $DEVTO_API_KEY" \
        -d "$(cat <<EOF
{
    "article": {
        "title": "$TITLE — Daily Code Project",
        "description": "$DESC",
        "body_markdown": "$BODY$CODE_BLOCK\n\n---\n*Part of my [Daily Code Series](https://github.com/$(git config user.name)/daily-code). Ship every day! 🚀*",
        "published": true,
        "tags": ["python", "programming", "tutorial", "opensource"],
        "canonical_url": ""
    }
}
EOF
)" | python3 -m json.tool 2>/dev/null || err "dev.to publish failed"
    log "dev.to article created!"
}

# ── Hashnode ───────────────────────────────────────────────────────────────
publish_hashnode() {
    warn "Publishing to Hashnode..."

    if [ -z "${HASHNODE_TOKEN:-}" ]; then
        err "HASHNODE_TOKEN not set. Get one at https://hashnode.com/settings/developer"
        return 1
    fi

    BODY=$(cat "$README_PATH")

    # Hashnode GraphQL mutation
    MUTATION=$(cat <<GQL
mutation {
    createPublicationStory(
        input: {
            title: "$TITLE",
            contentMarkdown: "$(echo "$BODY" | sed 's/"/\\"/g' | tr '\n' ' ')",
            tags: [],
            isPartOfPublication: { publicationId: "YOUR_PUBLICATION_ID" }
        }
    ) {
        post { slug url }
    }
}
GQL
)

    curl -s -X POST "https://gql.hashnode.com" \
        -H "Content-Type: application/json" \
        -H "Authorization: $HASHNODE_TOKEN" \
        -d "{\"query\": \"$(echo $MUTATION | sed 's/"/\\"/g')\"}" \
        | python3 -m json.tool 2>/dev/null || err "Hashnode publish failed"
    log "Hashnode post created!"
}

# ── Social Posts Generator ─────────────────────────────────────────────────
generate_social_posts() {
    warn "Generating social media posts..."

    GITHUB_URL="https://github.com/$(git config user.name 2>/dev/null || echo "USERNAME")/daily-code"

    POSTS_DIR="$PROJECT_DIR/social-posts"
    mkdir -p "$POSTS_DIR"

    # X/Twitter post (< 280 chars)
    cat > "$POSTS_DIR/twitter.txt" <<TW
🚀 Daily Code #$(date +%j): $TITLE

$DESC

🔗 $GITHUB_URL

#buildinpublic #100DaysOfCode #python
TW

    # LinkedIn post (longer form)
    cat > "$POSTS_DIR/linkedin.txt" <<LI
🚀 Daily Code Project — Day $(date +%j)

Today I built: **$TITLE**

$DESC

This is part of my challenge to ship one complete mini-project every single day. No skipped days, no placeholder commits — real, working code.

🔗 GitHub: $GITHUB_URL
💼 Portfolio: https://forg.to/@$(git config user.name 2>/dev/null || echo "USERNAME")

#buildinpublic #python #softwareengineering #dailycode
LI

    # Bluesky post
    cat > "$POSTS_DIR/bluesky.txt" <<BS
🚀 Daily Code: $TITLE ✨

$DESC

$GITHUB_URL
BS

    log "Social posts generated in $POSTS_DIR/"
    echo ""
    echo "  ─── Twitter/X ───"
    cat "$POSTS_DIR/twitter.txt"
    echo ""
    echo "  ─── LinkedIn ───"
    cat "$POSTS_DIR/linkedin.txt"
    echo ""
    echo "  ─── Bluesky ───"
    cat "$POSTS_DIR/bluesky.txt"
}

# ── forg.to Profile Update ─────────────────────────────────────────────────
publish_forgto() {
    warn "forg.to is an aggregator — it auto-pulls from GitHub."
    log "Ensure your forg.to profile is linked to your GitHub: https://forg.to/settings"
    log "Your latest commits will appear automatically."
}

# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

case "$PLATFORM" in
    --all)
        publish_devto
        publish_hashnode
        generate_social_posts
        publish_forgto
        ;;
    --devto)
        publish_devto
        ;;
    --hashnode)
        publish_hashnode
        ;;
    --social)
        generate_social_posts
        ;;
    --forgto)
        publish_forgto
        ;;
    *)
        echo "Unknown platform: $PLATFORM"
        echo "Options: --all, --devto, --hashnode, --social, --forgto"
        exit 1
        ;;
esac

echo ""
log "All done! 🎉"
