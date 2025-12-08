#!/bin/bash
# Justice League Self-Learning Module
# Automatically triggered at session end (90-95% token usage)
# Extracts learnings and updates knowledge base

set -e

LEARNING_DIR="$HOME/.claude/session-learnings"
KNOWLEDGE_DIR="$HOME/.claude/knowledge-base"
SKILLS_DIR="$HOME/.claude/skills"
DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date +%Y-%m-%dT%H:%M:%S)

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo ""
echo -e "${BLUE}══════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}     🧠 Justice League Self-Learning Module${NC}"
echo -e "${BLUE}══════════════════════════════════════════════════════════════════${NC}"
echo ""

# Ensure directories exist
mkdir -p "$LEARNING_DIR" "$KNOWLEDGE_DIR"

echo -e "${GREEN}🔍 Extracting learnings from session...${NC}"

# Run the Python learning extraction engine
if python3 "$HOME/.claude/scripts/extract-learnings.py" --date "$DATE"; then
    echo -e "${GREEN}✅ Learnings extracted successfully${NC}"
else
    echo -e "${YELLOW}⚠️  Learning extraction completed with warnings${NC}"
fi

echo ""
echo -e "${BLUE}══════════════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}     ✅ Justice League is now smarter!${NC}"
echo -e "${BLUE}══════════════════════════════════════════════════════════════════${NC}"
echo ""

# Show summary of what was learned
if [ -f "$LEARNING_DIR/$DATE.md" ]; then
    echo -e "${GREEN}📄 Session learnings saved to: $LEARNING_DIR/$DATE.md${NC}"
fi

if [ -f "$KNOWLEDGE_DIR/learning_log.json" ]; then
    echo -e "${GREEN}💾 Knowledge base updated: $KNOWLEDGE_DIR/${NC}"
fi
