#!/bin/bash
# Oracle Cost Tracking System Verification Script
# Verifies all components are in place and working

echo "🔮 Oracle Cost Tracking System Verification"
echo "============================================"
echo ""

PASS=0
FAIL=0

# Test 1: Check core files exist
echo "Test 1: Core files exist..."
if [ -f "oracle_cost_tracker.py" ] && [ -f "quicksilver_with_oracle.sh" ] && [ -f "ORACLE_COST_TRACKING.md" ]; then
    echo "✅ All core files present"
    ((PASS++))
else
    echo "❌ Missing core files"
    ((FAIL++))
fi

# Test 2: Check file permissions
echo "Test 2: File permissions..."
if [ -x "quicksilver_with_oracle.sh" ]; then
    echo "✅ Scripts are executable"
    ((PASS++))
else
    echo "❌ Scripts not executable (run: chmod +x *.sh)"
    ((FAIL++))
fi

# Test 3: Check Python syntax
echo "Test 3: Python syntax..."
if python3 -m py_compile oracle_cost_tracker.py 2>/dev/null; then
    echo "✅ Python script has valid syntax"
    ((PASS++))
else
    echo "❌ Python syntax errors"
    ((FAIL++))
fi

# Test 4: Check environment
echo "Test 4: Environment variables..."
if [ -n "$FIGMA_ACCESS_TOKEN" ]; then
    echo "✅ FIGMA_ACCESS_TOKEN is set"
    ((PASS++))
else
    echo "⚠️  FIGMA_ACCESS_TOKEN not set (required for Figma API)"
    echo "   Set with: export FIGMA_ACCESS_TOKEN='your_token'"
    ((FAIL++))
fi

# Test 5: Check Python dependencies
echo "Test 5: Python dependencies..."
if python3 -c "import requests" 2>/dev/null; then
    echo "✅ requests library installed"
    ((PASS++))
else
    echo "⚠️  requests library not found"
    echo "   Install with: pip install requests"
    ((FAIL++))
fi

# Test 6: Check savepoint
echo "Test 6: Savepoint document..."
if [ -f "SAVEPOINT-ORACLE-COST-TRACKING-2025-11-03.md" ]; then
    echo "✅ Savepoint document exists"
    ((PASS++))
else
    echo "❌ Savepoint document missing"
    ((FAIL++))
fi

# Test 7: Check Quicksilver integration
echo "Test 7: Quicksilver integration..."
if [ -f "export_figma_png.py" ]; then
    echo "✅ Quicksilver export script found"
    ((PASS++))
else
    echo "⚠️  Quicksilver export script not found"
    echo "   Oracle cost tracking requires export_figma_png.py"
    ((FAIL++))
fi

echo ""
echo "============================================"
echo "Results: $PASS passed, $FAIL failed"
echo ""

if [ $FAIL -eq 0 ]; then
    echo "✅ System verification PASSED"
    echo "   Oracle Cost Tracking is ready to use"
    echo ""
    echo "Quick start:"
    echo "  ./quicksilver_with_oracle.sh <FILE_KEY>"
    exit 0
else
    echo "❌ System verification FAILED"
    echo "   Please fix the issues above before using"
    echo ""
    echo "For help, see: ORACLE_COST_TRACKING.md"
    exit 1
fi
