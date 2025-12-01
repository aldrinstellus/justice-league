#!/bin/bash

# Token Estimation Calculator for Claude Code Sessions
# Estimates token usage to optimize context window usage

set -euo pipefail

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Token estimation constants (1 token ≈ 4 characters)
CHARS_PER_TOKEN=4
TOKEN_LIMIT=200000

echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     Claude Code Token Estimation Calculator        ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
echo ""

# Function to estimate tokens from characters
estimate_tokens() {
    local chars=$1
    echo $(( chars / CHARS_PER_TOKEN ))
}

# Function to format numbers with commas
format_number() {
    printf "%'d" $1
}

# Calculate CLAUDE.md size
CLAUDE_MD_PATH="$HOME/.claude/CLAUDE.md"
if [ -f "$CLAUDE_MD_PATH" ]; then
    CLAUDE_MD_CHARS=$(wc -c < "$CLAUDE_MD_PATH")
    CLAUDE_MD_TOKENS=$(estimate_tokens $CLAUDE_MD_CHARS)
    echo -e "${GREEN}✓${NC} Global CLAUDE.md: $(format_number $CLAUDE_MD_CHARS) chars ≈ $(format_number $CLAUDE_MD_TOKENS) tokens"
else
    CLAUDE_MD_CHARS=0
    CLAUDE_MD_TOKENS=0
    echo -e "${YELLOW}⚠${NC} Global CLAUDE.md not found"
fi

# Calculate project CLAUDE.md size (if in project)
PROJECT_CLAUDE_MD="./CLAUDE.md"
if [ -f "$PROJECT_CLAUDE_MD" ]; then
    PROJECT_CLAUDE_CHARS=$(wc -c < "$PROJECT_CLAUDE_MD")
    PROJECT_CLAUDE_TOKENS=$(estimate_tokens $PROJECT_CLAUDE_CHARS)
    echo -e "${GREEN}✓${NC} Project CLAUDE.md: $(format_number $PROJECT_CLAUDE_CHARS) chars ≈ $(format_number $PROJECT_CLAUDE_TOKENS) tokens"
else
    PROJECT_CLAUDE_CHARS=0
    PROJECT_CLAUDE_TOKENS=0
fi

# Calculate agent definitions (average)
AGENTS_DIR="$HOME/.claude/agents"
if [ -d "$AGENTS_DIR" ]; then
    AGENT_COUNT=$(ls -1 "$AGENTS_DIR"/*.md 2>/dev/null | wc -l | tr -d ' ')
    if [ "$AGENT_COUNT" -gt 0 ]; then
        AGENTS_CHARS=$(cat "$AGENTS_DIR"/*.md 2>/dev/null | wc -c | tr -d ' ')
        AVG_AGENT_CHARS=$(( AGENTS_CHARS / AGENT_COUNT ))
        AVG_AGENT_TOKENS=$(estimate_tokens $AVG_AGENT_CHARS)
        echo -e "${GREEN}✓${NC} Agent definitions: $AGENT_COUNT agents, avg $(format_number $AVG_AGENT_CHARS) chars ≈ $(format_number $AVG_AGENT_TOKENS) tokens each"
    else
        AGENT_COUNT=0
        AVG_AGENT_TOKENS=0
    fi
else
    AGENT_COUNT=0
    AVG_AGENT_TOKENS=0
    echo -e "${YELLOW}⚠${NC} No agent definitions found"
fi

# Calculate skills (if any are auto-activated)
SKILLS_DIR="$HOME/.claude/skills"
if [ -d "$SKILLS_DIR" ]; then
    SKILL_COUNT=$(ls -1 "$SKILLS_DIR"/*/SKILL.md 2>/dev/null | wc -l | tr -d ' ')
    if [ "$SKILL_COUNT" -gt 0 ]; then
        SKILLS_CHARS=$(cat "$SKILLS_DIR"/*/SKILL.md 2>/dev/null | wc -c | tr -d ' ')
        AVG_SKILL_CHARS=$(( SKILLS_CHARS / SKILL_COUNT ))
        AVG_SKILL_TOKENS=$(estimate_tokens $AVG_SKILL_CHARS)
        echo -e "${GREEN}✓${NC} Skills: $SKILL_COUNT skills, avg $(format_number $AVG_SKILL_CHARS) chars ≈ $(format_number $AVG_SKILL_TOKENS) tokens each"
    else
        SKILL_COUNT=0
        AVG_SKILL_TOKENS=0
    fi
else
    SKILL_COUNT=0
    AVG_SKILL_TOKENS=0
fi

echo ""
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}           Conversation Scenarios                    ${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Base context (always loaded)
BASE_TOKENS=$(( CLAUDE_MD_TOKENS + PROJECT_CLAUDE_TOKENS ))

echo -e "${YELLOW}Scenario 1: Simple Question (No agents, no skills)${NC}"
SIMPLE_TOKENS=$BASE_TOKENS
SIMPLE_USER_TOKENS=500  # Short question
SIMPLE_RESPONSE_TOKENS=2000  # Brief answer
SIMPLE_TOTAL=$(( SIMPLE_TOKENS + SIMPLE_USER_TOKENS + SIMPLE_RESPONSE_TOKENS ))
SIMPLE_REMAINING=$(( TOKEN_LIMIT - SIMPLE_TOTAL ))
SIMPLE_PERCENT=$(( SIMPLE_TOTAL * 100 / TOKEN_LIMIT ))

echo "  Base context: $(format_number $BASE_TOKENS) tokens"
echo "  User message: $(format_number $SIMPLE_USER_TOKENS) tokens"
echo "  Response:     $(format_number $SIMPLE_RESPONSE_TOKENS) tokens"
echo -e "  ${GREEN}Total:${NC}        $(format_number $SIMPLE_TOTAL) tokens (${SIMPLE_PERCENT}%)"
echo -e "  ${GREEN}Remaining:${NC}    $(format_number $SIMPLE_REMAINING) tokens"
echo ""

echo -e "${YELLOW}Scenario 2: Single Agent Deployment${NC}"
AGENT_TOKENS=$BASE_TOKENS
AGENT_USER_TOKENS=1000  # Medium question
AGENT_CONTEXT_TOKENS=$AVG_AGENT_TOKENS  # One agent loaded
AGENT_RESPONSE_TOKENS=10000  # Detailed answer from agent
AGENT_TOTAL=$(( AGENT_TOKENS + AGENT_USER_TOKENS + AGENT_CONTEXT_TOKENS + AGENT_RESPONSE_TOKENS ))
AGENT_REMAINING=$(( TOKEN_LIMIT - AGENT_TOTAL ))
AGENT_PERCENT=$(( AGENT_TOTAL * 100 / TOKEN_LIMIT ))

echo "  Base context: $(format_number $BASE_TOKENS) tokens"
echo "  Agent loaded: $(format_number $AGENT_CONTEXT_TOKENS) tokens"
echo "  User message: $(format_number $AGENT_USER_TOKENS) tokens"
echo "  Response:     $(format_number $AGENT_RESPONSE_TOKENS) tokens"
echo -e "  ${GREEN}Total:${NC}        $(format_number $AGENT_TOTAL) tokens (${AGENT_PERCENT}%)"
echo -e "  ${GREEN}Remaining:${NC}    $(format_number $AGENT_REMAINING) tokens"
echo ""

echo -e "${YELLOW}Scenario 3: Justice League (3 agents + 1 skill)${NC}"
JL_TOKENS=$BASE_TOKENS
JL_USER_TOKENS=1500  # Complex request
JL_AGENTS_TOKENS=$(( AVG_AGENT_TOKENS * 3 ))  # 3 agents deployed
JL_SKILL_TOKENS=$AVG_SKILL_TOKENS  # 1 skill auto-activated
JL_RESPONSE_TOKENS=25000  # Comprehensive answer from multiple agents
JL_TOTAL=$(( JL_TOKENS + JL_USER_TOKENS + JL_AGENTS_TOKENS + JL_SKILL_TOKENS + JL_RESPONSE_TOKENS ))
JL_REMAINING=$(( TOKEN_LIMIT - JL_TOTAL ))
JL_PERCENT=$(( JL_TOTAL * 100 / TOKEN_LIMIT ))

echo "  Base context: $(format_number $BASE_TOKENS) tokens"
echo "  3 agents:     $(format_number $JL_AGENTS_TOKENS) tokens"
echo "  1 skill:      $(format_number $JL_SKILL_TOKENS) tokens"
echo "  User message: $(format_number $JL_USER_TOKENS) tokens"
echo "  Response:     $(format_number $JL_RESPONSE_TOKENS) tokens"
echo -e "  ${GREEN}Total:${NC}        $(format_number $JL_TOTAL) tokens (${JL_PERCENT}%)"
echo -e "  ${GREEN}Remaining:${NC}    $(format_number $JL_REMAINING) tokens"
echo ""

# Recommendations
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}           Optimization Recommendations              ${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check CLAUDE.md size
CLAUDE_MD_TARGET=30000
if [ $CLAUDE_MD_CHARS -gt 40000 ]; then
    echo -e "${RED}⚠ CRITICAL:${NC} Global CLAUDE.md exceeds 40k chars ($(format_number $CLAUDE_MD_CHARS))"
    echo "  → Move detailed content to reference files"
    echo "  → Target: <30k chars (currently $(( (CLAUDE_MD_CHARS - CLAUDE_MD_TARGET) / 1000 ))k over)"
elif [ $CLAUDE_MD_CHARS -gt $CLAUDE_MD_TARGET ]; then
    echo -e "${YELLOW}⚠ WARNING:${NC} Global CLAUDE.md approaching limit ($(format_number $CLAUDE_MD_CHARS) chars)"
    echo "  → Consider moving non-essential content to references"
else
    echo -e "${GREEN}✓${NC} Global CLAUDE.md size optimal (<30k chars)"
fi

# Check project CLAUDE.md size
if [ $PROJECT_CLAUDE_CHARS -gt 20000 ]; then
    echo -e "${YELLOW}⚠ WARNING:${NC} Project CLAUDE.md is large ($(format_number $PROJECT_CLAUDE_CHARS) chars)"
    echo "  → Consider splitting into smaller focused files"
fi

# Check skill count
if [ $SKILL_COUNT -gt 3 ]; then
    echo -e "${YELLOW}⚠ INFO:${NC} $SKILL_COUNT skills installed (can auto-activate)"
    echo "  → Each activated skill adds ~$(format_number $AVG_SKILL_TOKENS) tokens"
    echo "  → Use specific activation keywords to control when skills load"
fi

# Provide conversation limit estimate
MAX_CONVERSATIONS=$(( TOKEN_LIMIT / JL_TOTAL ))
echo ""
echo -e "${GREEN}✓${NC} Estimated capacity: ~$MAX_CONVERSATIONS Justice League deployments per session"
echo -e "${GREEN}✓${NC} Trigger /savepoint at 180K-190K tokens (90-95%)"

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Token Optimization Guide                          ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════╝${NC}"
echo ""
echo "1. Keep global CLAUDE.md < 30k chars (currently $(format_number $CLAUDE_MD_CHARS))"
echo "2. Use reference files for detailed content (loaded on-demand)"
echo "3. Skills auto-activate based on keywords (be specific)"
echo "4. Agents only loaded when explicitly invoked via Task tool"
echo "5. Create /savepoint at 180K-190K tokens to preserve work"
echo ""
