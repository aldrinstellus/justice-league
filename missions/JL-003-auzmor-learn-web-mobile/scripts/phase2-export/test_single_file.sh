#!/bin/bash
#
# Test Single File Export (Phase 2A Validation)
# ==============================================
#
# Tests export script on one file before running full 182-file export.
#
# Usage:
#   ./test_single_file.sh
#
# Requirements:
#   - FIGMA_ACCESS_TOKEN environment variable set
#   - Python 3 with requests library
#
# Expected Output:
#   test-exports/001-Firefight-2023-Q4-Homeward-Bound-Unlock-Assessments/
#   ├── page-01-[PageName]/
#   │   ├── page-01-overview.png
#   │   ├── sections/ (if sections exist)
#   │   │   └── section-01-[Name]/
#   │   │       ├── section-overview.png
#   │   │       └── frames/
#   │   │           └── frame-001-[Name].png
#   │   └── frames/ (direct frames)
#   │       └── frame-001-[Name].png
#   └── file-info.json
#
# Created: 2025-11-03 (Oracle)
#

set -e  # Exit on error

# Configuration
TEST_FILE_KEY="cuTXuQCQo5J5X0Xp9ifWUH"
TEST_FILE_NAME="(Firefight) 2023 Q4 - Homeward Bound || Unlock Assessments"
TEST_OUTPUT_DIR="../../test-exports"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "════════════════════════════════════════════════════════════════════════════════"
echo "  JL-003 Phase 2A: Single File Export Test"
echo "════════════════════════════════════════════════════════════════════════════════"
echo ""

# Check environment
if [ -z "$FIGMA_ACCESS_TOKEN" ]; then
    echo -e "${RED}❌ Error: FIGMA_ACCESS_TOKEN environment variable not set${NC}"
    echo ""
    echo "Set token with:"
    echo "  export FIGMA_ACCESS_TOKEN='figd_...'"
    echo ""
    exit 1
fi

echo -e "${GREEN}✅ FIGMA_ACCESS_TOKEN is set${NC}"
echo ""

# Clean previous test output
if [ -d "$TEST_OUTPUT_DIR" ]; then
    echo -e "${YELLOW}🧹 Cleaning previous test output...${NC}"
    rm -rf "$TEST_OUTPUT_DIR"
fi

echo ""
echo "📦 Test File Info:"
echo "   File Key: $TEST_FILE_KEY"
echo "   File Name: $TEST_FILE_NAME"
echo "   Output: $TEST_OUTPUT_DIR"
echo ""
echo "⏳ Starting export (this may take 2-5 minutes)..."
echo ""

# Run export
python3 export_with_sections.py \
  --file-key "$TEST_FILE_KEY" \
  --file-name "$TEST_FILE_NAME" \
  --file-number 1 \
  --output-dir "$TEST_OUTPUT_DIR"

EXIT_CODE=$?

echo ""
echo "════════════════════════════════════════════════════════════════════════════════"

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ Test Export Complete!${NC}"
    echo ""
    echo "📂 Output Directory:"
    echo "   $(cd "$TEST_OUTPUT_DIR" && pwd)"
    echo ""
    echo "📋 Validation Checklist:"
    echo "   [ ] Check folder structure matches spec"
    echo "   [ ] Verify page overview PNGs exist"
    echo "   [ ] Check section handling (if sections exist)"
    echo "   [ ] Validate frame PNGs in correct folders"
    echo "   [ ] Review file-info.json metadata"
    echo ""
    echo "🔍 Quick Verification:"
    echo "   # View directory structure"
    echo "   tree $TEST_OUTPUT_DIR"
    echo ""
    echo "   # Check metadata"
    echo "   cat $TEST_OUTPUT_DIR/001-*/file-info.json | jq ."
    echo ""
    echo "   # Count exported files"
    echo "   find $TEST_OUTPUT_DIR -name '*.png' | wc -l"
    echo ""
    echo "✅ If test looks good, proceed with full export:"
    echo "   python3 export_with_sections.py --all --output-dir ../../exports/figma-files/"
else
    echo -e "${RED}❌ Test Export Failed!${NC}"
    echo ""
    echo "Check error messages above for details."
    echo ""
    exit 1
fi

echo "════════════════════════════════════════════════════════════════════════════════"
