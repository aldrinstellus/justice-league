# Justice League Real-Time Expense Tracking Scripts

**Version**: 1.0.0
**Last Updated**: 2025-11-03

---

## Overview

This directory contains Python scripts for real-time expense tracking via the Anthropic API. The scripts fetch actual usage data and update mission expense logs automatically.

**Key Features**:
- Real-time usage data from Anthropic API
- Automatic expense log updates
- Per-mission and global tracking
- Budget alerts and threshold monitoring

---

## Files

| File | Purpose |
|------|---------|
| `fetch-anthropic-usage.py` | Main script for fetching API usage and updating expenses |
| `requirements.txt` | Python dependencies |
| `.env.example` | Template for environment variables |
| `.env` | Actual environment variables (**gitignored, contains API key**) |
| `README.md` | This file |

---

## Setup

### Step 1: Install Python Dependencies

```bash
cd /Users/admin/Documents/claudecode/justice-league-missions/expenses-global/scripts
pip install -r requirements.txt
```

**Dependencies**:
- `anthropic>=0.25.0` - Anthropic API client
- `python-dotenv>=1.0.0` - Environment variable management
- `requests>=2.31.0` - HTTP requests

### Step 2: Configure Environment Variables

The `.env` file is already created with your API key. **Never commit this file to git**.

**To verify setup**:
```bash
cat .env  # Should show your ANTHROPIC_API_KEY
```

**If you need to update the API key**:
```bash
nano .env
# Edit ANTHROPIC_API_KEY value
```

### Step 3: Test the Script

```bash
python fetch-anthropic-usage.py --help
```

**Expected output**:
```
usage: fetch-anthropic-usage.py [-h] [--mission MISSION] [--date DATE]
                                 [--start-date START_DATE] [--end-date END_DATE]

Fetch Anthropic API usage and update expense logs
```

---

## Usage

### Fetch All Recent Usage

```bash
python fetch-anthropic-usage.py
```

**What it does**:
- Fetches usage from yesterday to today
- Updates cumulative expenses
- Updates all active mission logs

### Fetch for Specific Mission

```bash
python fetch-anthropic-usage.py --mission JL-003
```

**What it does**:
- Fetches usage data
- Updates JL-003 expense log
- Regenerates JL-003 expense summary

### Fetch for Specific Date

```bash
python fetch-anthropic-usage.py --date 2025-11-03
```

**What it does**:
- Fetches usage for November 3, 2025
- Updates all relevant expense logs

### Fetch for Date Range

```bash
python fetch-anthropic-usage.py --start-date 2025-11-01 --end-date 2025-11-03
```

**What it does**:
- Fetches usage from Nov 1-3, 2025
- Updates expense logs with aggregated data

---

## Workflow

### After Each Activity (Real-Time Tracking)

```bash
# Run after completing a significant task
python fetch-anthropic-usage.py --mission JL-003

# Check updated budget
cat ../reports/decision-dashboard.md
```

### Daily Sync (Automated)

Set up a cron job for daily sync:

```bash
# Edit crontab
crontab -e

# Add this line (runs daily at midnight)
0 0 * * * cd /Users/admin/Documents/claudecode/justice-league-missions/expenses-global/scripts && python fetch-anthropic-usage.py
```

### Manual Sync (On-Demand)

```bash
# Update all expenses
python fetch-anthropic-usage.py

# Update specific mission
python fetch-anthropic-usage.py --mission JL-003

# Check results
cat ../reports/decision-dashboard.md
```

---

## Output Files Updated

When you run the script, it updates:

1. **Mission Expense Logs**:
   - `/missions/JL-XXX/expenses/logs/expense-log.json`

2. **Mission Summaries**:
   - `/missions/JL-XXX/expenses/reports/expense-summary.md`

3. **Global Cumulative**:
   - `/expenses-global/cumulative-expenses.json`

4. **Decision Dashboard**:
   - `/expenses-global/reports/decision-dashboard.md`

---

## Troubleshooting

### Error: "ANTHROPIC_API_KEY not found"

**Problem**: `.env` file missing or not loaded

**Solution**:
```bash
# Check .env exists
ls -la .env

# Verify API key is set
cat .env | grep ANTHROPIC_API_KEY

# If missing, copy from template
cp .env.example .env
nano .env  # Add your API key
```

### Error: "Failed to fetch usage from API"

**Problem**: API key invalid or API endpoint unreachable

**Solution**:
```bash
# Test API key manually
curl -H "x-api-key: YOUR_API_KEY" https://api.anthropic.com/v1/usage

# If fails, rotate API key at https://console.anthropic.com/settings/keys
```

### Error: "Mission JL-XXX not found"

**Problem**: Mission directory doesn't exist

**Solution**:
```bash
# List all missions
ls -la /Users/admin/Documents/claudecode/justice-league-missions/missions/

# Use correct mission ID
python fetch-anthropic-usage.py --mission JL-003
```

### Script runs but no updates

**Problem**: Usage data empty or date range incorrect

**Solution**:
```bash
# Check date range
python fetch-anthropic-usage.py --start-date 2025-11-01 --end-date 2025-11-03

# Verify usage data in output
```

---

## Security

### API Key Protection

✅ **DO**:
- Store API key in `.env` file (gitignored)
- Never commit `.env` to git
- Rotate API key if exposed
- Use environment variables only

❌ **DON'T**:
- Hardcode API key in Python scripts
- Share API key in conversation or messages
- Commit `.env` to version control
- Store API key in unencrypted files

### .gitignore Protection

The root `.gitignore` should include:
```
**/.env
.env
expenses-global/scripts/.env
```

**Verify**:
```bash
git status  # Should NOT show .env file
```

---

## Advanced Usage

### Custom Date Ranges

```bash
# Last week
python fetch-anthropic-usage.py --start-date 2025-10-27 --end-date 2025-11-03

# Entire month
python fetch-anthropic-usage.py --start-date 2025-11-01 --end-date 2025-11-30
```

### Multiple Missions

```bash
# Update JL-001
python fetch-anthropic-usage.py --mission JL-001

# Update JL-003
python fetch-anthropic-usage.py --mission JL-003

# Update all (default)
python fetch-anthropic-usage.py
```

### Integration with Workflows

```bash
# After completing JL-003 Phase 1
cd /path/to/missions/JL-003-auzmor-learn-web-mobile
# ... do work ...
cd /path/to/scripts
python fetch-anthropic-usage.py --mission JL-003
cat ../reports/decision-dashboard.md  # Check budget
```

---

## Future Enhancements

Planned features:
- [ ] Email alerts when budget thresholds crossed
- [ ] Slack/Discord webhook notifications
- [ ] Automated report generation (PDF, HTML)
- [ ] Budget forecasting and recommendations
- [ ] Cost optimization suggestions
- [ ] Integration with CI/CD pipelines

---

## Support

**Issues?**
1. Check `.env` file exists and has valid API key
2. Verify Python dependencies installed: `pip list | grep anthropic`
3. Test API connectivity: `curl https://api.anthropic.com/v1/usage`
4. Review error messages in console output

**Questions?**
- See main expense tracking guide: `../EXPENSE-TRACKING-GUIDE.md`
- Check decision dashboard: `../reports/decision-dashboard.md`
- Review cumulative expenses: `../cumulative-expenses.json`

---

**Created**: 2025-11-03
**Maintained By**: Oracle (Justice League Coordinator)
**Account**: aldrinstellus@gmail.com (Claude Max - $100/month)
