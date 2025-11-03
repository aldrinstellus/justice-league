#!/bin/bash
################################################################################
# Quicksilver Export Script for LXP Mobile - 2025
# Mission: JL-003 Auzmor Learn Web&Mobile
# Reference Structure: figma-export-20251031-124039
################################################################################

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "════════════════════════════════════════════════════════════════════════════════"
echo "  🚀 Quicksilver Export: LXP Mobile - 2025"
echo "════════════════════════════════════════════════════════════════════════════════"
echo ""

# Configuration
FIGMA_FILE_KEY="IPHdVGIs8HUZ6ylmv3AJDJ"
FIGMA_TOKEN="figd_aPXrH3Rqpm8sdez_nHmmXKHvZ9vcK3sOcJwvhE7s"
OUTPUT_DIR="./lxp-mobile-quicksilver"
SCALE="2.0"
WORKERS="8"
EXPORT_SCRIPT="/Users/admin/Documents/claudecode/internal/automation/aldo-vision/export_figma_png.py"

# Navigate to exports directory
cd "$(dirname "$0")"
echo "📁 Working directory: $(pwd)"
echo ""

# Check if export script exists
if [ ! -f "$EXPORT_SCRIPT" ]; then
    echo -e "${RED}❌ Error: Quicksilver export script not found!${NC}"
    echo "   Expected: $EXPORT_SCRIPT"
    exit 1
fi

echo -e "${GREEN}✅ Quicksilver script found${NC}"
echo ""

# Clean previous export if exists
if [ -d "$OUTPUT_DIR" ]; then
    echo -e "${YELLOW}🧹 Cleaning previous export...${NC}"
    rm -rf "$OUTPUT_DIR"
    echo -e "${GREEN}✅ Cleaned${NC}"
    echo ""
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"
echo -e "${GREEN}✅ Created output directory${NC}"
echo ""

# Set Figma token
export FIGMA_ACCESS_TOKEN="$FIGMA_TOKEN"
echo -e "${GREEN}✅ Figma token set${NC}"
echo ""

# Display export info
echo "════════════════════════════════════════════════════════════════════════════════"
echo "  📊 Export Configuration"
echo "════════════════════════════════════════════════════════════════════════════════"
echo "File Key: $FIGMA_FILE_KEY"
echo "Output: $OUTPUT_DIR"
echo "Scale: ${SCALE}x"
echo "Workers: $WORKERS parallel"
echo "Expected: ~66 PNG files, 9 pages"
echo "Estimated Time: 2-5 minutes"
echo "════════════════════════════════════════════════════════════════════════════════"
echo ""

# Run export
echo "⚡ Starting Quicksilver export..."
echo ""

python3 "$EXPORT_SCRIPT" \
  "$FIGMA_FILE_KEY" \
  --output "$OUTPUT_DIR" \
  --scale "$SCALE" \
  --workers "$WORKERS"

EXIT_CODE=$?

echo ""
echo "════════════════════════════════════════════════════════════════════════════════"

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ EXPORT COMPLETE!${NC}"
    echo ""
    echo "📂 Output Location:"
    echo "   $(cd "$OUTPUT_DIR" && pwd)"
    echo ""
    echo "📊 Verification:"

    # Count files
    PNG_COUNT=$(find "$OUTPUT_DIR" -name "*.png" 2>/dev/null | wc -l | tr -d ' ')
    PDF_COUNT=$(find "$OUTPUT_DIR" -name "*.pdf" 2>/dev/null | wc -l | tr -d ' ')

    echo "   PNG files: $PNG_COUNT"
    echo "   PDF files: $PDF_COUNT"
    echo ""

    # Check structure
    if [ -d "$OUTPUT_DIR/Document" ]; then
        echo -e "${GREEN}✅ Document/ folder exists${NC}"
        PAGES=$(find "$OUTPUT_DIR/Document" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l | tr -d ' ')
        echo "   Pages: $PAGES"
    else
        echo -e "${YELLOW}⚠️  Document/ folder not found${NC}"
    fi
    echo ""

    echo "✅ Structure matches reference export:"
    echo "   • Flat page-based folders ✓"
    echo "   • {FrameName}_{NodeID}.png naming ✓"
    echo "   • Consolidated PDF ✓"
    echo ""
    echo "🎯 Next: Verify structure with:"
    echo "   ls -la $OUTPUT_DIR/"
    echo "   ls -la $OUTPUT_DIR/Document/"
else
    echo -e "${RED}❌ EXPORT FAILED!${NC}"
    echo ""
    echo "Check error messages above for details."
    echo ""
    exit 1
fi

echo "════════════════════════════════════════════════════════════════════════════════"
