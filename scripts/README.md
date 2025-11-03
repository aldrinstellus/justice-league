# Justice League Simple Cost Tracking Scripts

Simple Python scripts for generating estimates and invoices.

## Scripts

### 1. `generate-estimate.py`
Generate cost estimate before starting work.

**Usage**:
```bash
python3 generate-estimate.py JL-003 phase2
```

**Output**: Creates `JL-003-PHASE2-ESTIMATE.md` in mission folder

---

### 2. `generate-invoice.py`
Generate invoice after completing work.

**Usage**:
```bash
python3 generate-invoice.py JL-003 phase1 --oracle-cost 12.34 --agent-cost 0
```

**Output**: Creates `JL-003-PHASE1-INVOICE.md` in mission folder

---

### 3. `monthly-summary.py`
Generate monthly budget summary.

**Usage**:
```bash
python3 monthly-summary.py november 2025
```

**Output**: Creates `NOVEMBER-2025-SUMMARY.md` in mission root

---

### 4. `check-budget.py`
Quick budget status check.

**Usage**:
```bash
python3 check-budget.py
```

**Output**:
```
Budget: $100.00
Spent: $12.34
Remaining: $87.66
Status: ✅ HEALTHY
```

---

## Requirements

**Python 3.9+**

**Dependencies**: None (uses only standard library)

---

## Setup

No setup required. Scripts use templates from `_templates/simple-tracking/`.

---

## Examples

**Estimate for new phase**:
```bash
cd justice-league-missions
python3 scripts/generate-estimate.py JL-003 phase3
# Edit the generated estimate file with actual costs
```

**Invoice after work**:
```bash
python3 scripts/generate-invoice.py JL-003 phase2 --oracle-cost 8.50 --agent-cost 40.97
# Automatically updates simple-budget.json
```

**Monthly summary**:
```bash
python3 scripts/monthly-summary.py november 2025
# Shows all completed tasks for November
```
