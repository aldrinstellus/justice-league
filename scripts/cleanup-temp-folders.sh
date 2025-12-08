#!/bin/bash
# ============================================================================
# JUSTICE LEAGUE TEMP FOLDER CLEANUP SCRIPT
# ============================================================================
# Safe to run anytime - temp folders are truly temporary
#
# Usage:
#   ./cleanup-temp-folders.sh       # Dry run (preview)
#   ./cleanup-temp-folders.sh -f    # Force delete
#
# ============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Temp folder patterns to check
TEMP_PATTERNS=(
    "/private/tmp/jl-*"
    "/private/tmp/justice-league-*"
    "/tmp/jl-*"
    "/tmp/justice-league-*"
)

# Parse arguments
DRY_RUN=true
[[ "$1" == "-f" || "$1" == "--force" ]] && DRY_RUN=false

echo ""
echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}  🧹 Justice League Temp Folder Cleanup${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""

if [[ "$DRY_RUN" == "true" ]]; then
    echo -e "${YELLOW}MODE: DRY RUN (use -f to delete)${NC}"
else
    echo -e "${RED}MODE: FORCE DELETE${NC}"
fi
echo ""

TOTAL_SIZE=0
FOLDERS_FOUND=0
FOLDERS_SAFE=0
FOLDERS_UNSAFE=0

# Find and process all matching folders
for pattern in "${TEMP_PATTERNS[@]}"; do
    for folder in $pattern; do
        if [[ -d "$folder" ]]; then
            FOLDERS_FOUND=$((FOLDERS_FOUND + 1))
            SIZE=$(du -sh "$folder" 2>/dev/null | cut -f1)

            # Check for git repos with uncommitted/unpushed work
            if [[ -d "$folder/.git" ]]; then
                cd "$folder"
                UNCOMMITTED=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
                UNPUSHED=$(git log origin/main..HEAD --oneline 2>/dev/null | wc -l | tr -d ' ')
                cd - > /dev/null

                if [[ "$UNCOMMITTED" -gt 0 ]] || [[ "$UNPUSHED" -gt 0 ]]; then
                    FOLDERS_UNSAFE=$((FOLDERS_UNSAFE + 1))
                    echo -e "${RED}⚠️  $folder ($SIZE)${NC}"
                    echo -e "   ${RED}HAS UNCOMMITTED/UNPUSHED WORK!${NC}"
                    echo -e "   → Uncommitted files: $UNCOMMITTED"
                    echo -e "   → Unpushed commits: $UNPUSHED"
                    echo -e "   → Action: ${YELLOW}cd $folder && git push${NC}"
                    echo ""
                    continue
                fi
            fi

            # Safe to delete
            FOLDERS_SAFE=$((FOLDERS_SAFE + 1))
            echo -e "${GREEN}✅ $folder ($SIZE)${NC}"
            echo -e "   Safe to delete"

            if [[ "$DRY_RUN" == "false" ]]; then
                rm -rf "$folder"
                echo -e "   ${GREEN}→ DELETED${NC}"
            fi
            echo ""
        fi
    done
done

# Summary
echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}  SUMMARY${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""
echo -e "Folders found:     $FOLDERS_FOUND"
echo -e "${GREEN}Safe to delete:    $FOLDERS_SAFE${NC}"
echo -e "${RED}Unsafe (has work): $FOLDERS_UNSAFE${NC}"
echo ""

if [[ "$FOLDERS_FOUND" -eq 0 ]]; then
    echo -e "${GREEN}✨ No temp folders found. Already clean!${NC}"
elif [[ "$DRY_RUN" == "true" ]]; then
    echo -e "${YELLOW}DRY RUN complete. No files deleted.${NC}"
    echo -e "Run with ${BLUE}-f${NC} to delete safe folders."
else
    echo -e "${GREEN}Cleanup complete!${NC}"
fi
echo ""
