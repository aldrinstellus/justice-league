# 🚨 Quick Recovery Guide - Oracle Cost Tracking

**If the system breaks, follow these steps in order:**

---

## Step 1: Verify Core Files

```bash
cd /Users/admin/Documents/claudecode/internal/automation/aldo-vision
ls -lh oracle_cost_tracker.py quicksilver_with_oracle.sh ORACLE_COST_TRACKING.md
```

**Expected**: All 3 files exist

**If missing**: Check savepoint and restore:
```bash
cat SAVEPOINT-ORACLE-COST-TRACKING-2025-11-03.md
# Files are embedded in savepoint - extract and recreate if needed
```

---

## Step 2: Run Verification

```bash
./verify_oracle_system.sh
```

**Expected**: 6/7 tests pass (FIGMA_ACCESS_TOKEN warning is OK)

**If <6 tests pass**: Fix issues shown in output

---

## Step 3: Set Environment Token

```bash
export FIGMA_ACCESS_TOKEN='figd_your_token_here'
```

**Or add to `.env` file**:
```bash
echo "FIGMA_ACCESS_TOKEN='figd_your_token_here'" >> .env
```

---

## Step 4: Test Pre-Flight

```bash
python3 oracle_cost_tracker.py DGSQki23ijUtNhN3pck2Oc pre-flight
```

**Expected**: Shows file structure + cost estimate

**If fails**: Check error message and fix (token, permissions, etc.)

---

## Step 5: Test Full Workflow

```bash
./quicksilver_with_oracle.sh DGSQki23ijUtNhN3pck2Oc
```

**Expected**: 
1. Pre-flight analysis displays
2. Prompts for confirmation
3. Exports successfully
4. Post-flight analysis displays
5. Reports generated

---

## Common Issues

### "Figma token not found"
```bash
export FIGMA_ACCESS_TOKEN='figd_your_token_here'
```

### "Permission denied"
```bash
chmod +x quicksilver_with_oracle.sh verify_oracle_system.sh
```

### "Python module not found"
```bash
pip install requests pandas
```

### "Pre-flight data not found"
```bash
# Always run pre-flight before post-flight
python3 oracle_cost_tracker.py FILE_KEY pre-flight
# Then export
# Then post-flight
```

---

## Nuclear Option: Complete Restore

If everything is broken:

```bash
# 1. Check savepoint exists
cat SAVEPOINT-ORACLE-COST-TRACKING-2025-11-03.md

# 2. Verify file locations
cd /Users/admin/Documents/claudecode/internal/automation/aldo-vision

# 3. Check git status
git status

# 4. If files are corrupted, restore from git:
git checkout oracle_cost_tracker.py
git checkout quicksilver_with_oracle.sh
git checkout ORACLE_COST_TRACKING.md

# 5. Re-run verification
./verify_oracle_system.sh
```

---

## Contact

**System**: Oracle Cost Tracking v1.0.0  
**Savepoint**: 2025-11-03  
**Documentation**: ORACLE_COST_TRACKING.md  
**Verification**: verify_oracle_system.sh
