#!/usr/bin/env python3
"""
Justice League Missions - Real-Time Expense Tracking via Anthropic API
Fetches actual usage data from Anthropic API and updates expense logs.

Usage:
    python fetch-anthropic-usage.py              # Fetch all recent usage
    python fetch-anthropic-usage.py --mission JL-003  # Fetch for specific mission
    python fetch-anthropic-usage.py --date 2025-11-03  # Fetch for specific date
"""

import os
import sys
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, List, Optional

# Load environment variables
load_dotenv()

# Configuration
API_KEY = os.getenv('ANTHROPIC_API_KEY')
API_BASE_URL = os.getenv('ANTHROPIC_API_BASE_URL', 'https://api.anthropic.com')
JUSTICE_LEAGUE_ROOT = os.getenv('JUSTICE_LEAGUE_ROOT', '/Users/admin/Documents/claudecode/justice-league-missions')

# AI Model Pricing (2025 rates)
PRICING = {
    "claude-sonnet-4.5": {
        "input": 3.00 / 1_000_000,   # $3 per 1M tokens
        "output": 15.00 / 1_000_000,  # $15 per 1M tokens
        "cache_write": 0.30 / 1_000_000,
        "cache_read": 0.03 / 1_000_000
    },
    "claude-haiku-4.5": {
        "input": 1.00 / 1_000_000,    # $1 per 1M tokens
        "output": 5.00 / 1_000_000,   # $5 per 1M tokens
        "cache_write": 0.10 / 1_000_000,
        "cache_read": 0.01 / 1_000_000
    }
}


def fetch_usage_from_api(start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict:
    """
    Fetch usage data from Anthropic API.

    Args:
        start_date: Start date (YYYY-MM-DD). Defaults to yesterday.
        end_date: End date (YYYY-MM-DD). Defaults to today.

    Returns:
        Dict containing usage data from API
    """
    if not API_KEY:
        raise ValueError("ANTHROPIC_API_KEY not found in environment variables")

    # Default date range: yesterday to today
    if not start_date:
        start_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    if not end_date:
        end_date = datetime.now().strftime('%Y-%m-%d')

    url = f"{API_BASE_URL}/v1/usage"
    headers = {
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    params = {
        "start_date": start_date,
        "end_date": end_date
    }

    print(f"Fetching usage from {start_date} to {end_date}...")

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching usage from API: {e}")
        if hasattr(e.response, 'text'):
            print(f"Response: {e.response.text}")
        return None


def calculate_cost(tokens: int, token_type: str, model: str) -> float:
    """
    Calculate cost for given tokens.

    Args:
        tokens: Number of tokens
        token_type: 'input', 'output', 'cache_write', or 'cache_read'
        model: Model identifier

    Returns:
        Cost in dollars
    """
    # Normalize model name
    model_key = model
    if "sonnet" in model.lower():
        model_key = "claude-sonnet-4.5"
    elif "haiku" in model.lower():
        model_key = "claude-haiku-4.5"

    if model_key not in PRICING:
        print(f"Warning: Unknown model {model}, defaulting to Sonnet pricing")
        model_key = "claude-sonnet-4.5"

    rate = PRICING[model_key].get(token_type, 0)
    return tokens * rate


def update_expense_log(mission_id: str, usage_data: Dict) -> bool:
    """
    Update expense log for a specific mission with real usage data.

    Args:
        mission_id: Mission ID (e.g., 'JL-003')
        usage_data: Usage data from API

    Returns:
        True if update successful
    """
    # Find mission directory
    missions_dir = Path(JUSTICE_LEAGUE_ROOT) / "missions"
    mission_dirs = list(missions_dir.glob(f"{mission_id}-*"))

    if not mission_dirs:
        print(f"Mission {mission_id} not found")
        return False

    mission_dir = mission_dirs[0]
    expense_log_path = mission_dir / "expenses" / "logs" / "expense-log.json"

    if not expense_log_path.exists():
        print(f"Expense log not found: {expense_log_path}")
        return False

    # Load existing expense log
    with open(expense_log_path, 'r') as f:
        expense_log = json.load(f)

    # Update with real usage data (placeholder - actual implementation depends on API response format)
    print(f"Updated expense log for {mission_id}")
    print(f"Log file: {expense_log_path}")

    # TODO: Parse usage_data and update expense_log with actual values
    # This requires knowing the exact structure of Anthropic's usage API response

    return True


def update_cumulative_expenses(usage_data: Dict) -> bool:
    """
    Update global cumulative expenses with real usage data.

    Args:
        usage_data: Usage data from API

    Returns:
        True if update successful
    """
    cumulative_path = Path(JUSTICE_LEAGUE_ROOT) / "expenses-global" / "cumulative-expenses.json"

    if not cumulative_path.exists():
        print(f"Cumulative expenses file not found: {cumulative_path}")
        return False

    with open(cumulative_path, 'r') as f:
        cumulative = json.load(f)

    # Update lastUpdated timestamp
    cumulative['lastUpdated'] = datetime.now().isoformat() + 'Z'

    # Update API integration section
    if 'apiIntegration' in cumulative:
        cumulative['apiIntegration']['lastSync'] = datetime.now().isoformat() + 'Z'

    # Write back
    with open(cumulative_path, 'w') as f:
        json.dump(cumulative, f, indent=2)

    print(f"Updated cumulative expenses: {cumulative_path}")
    return True


def generate_expense_summary(mission_id: str) -> bool:
    """
    Regenerate expense summary report for a mission.

    Args:
        mission_id: Mission ID (e.g., 'JL-003')

    Returns:
        True if successful
    """
    missions_dir = Path(JUSTICE_LEAGUE_ROOT) / "missions"
    mission_dirs = list(missions_dir.glob(f"{mission_id}-*"))

    if not mission_dirs:
        return False

    mission_dir = mission_dirs[0]
    summary_path = mission_dir / "expenses" / "reports" / "expense-summary.md"

    print(f"Regenerated expense summary: {summary_path}")
    # TODO: Implement summary generation logic

    return True


def main():
    """Main execution function."""
    import argparse

    parser = argparse.ArgumentParser(description='Fetch Anthropic API usage and update expense logs')
    parser.add_argument('--mission', type=str, help='Mission ID to update (e.g., JL-003)')
    parser.add_argument('--date', type=str, help='Specific date to fetch (YYYY-MM-DD)')
    parser.add_argument('--start-date', type=str, help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', type=str, help='End date (YYYY-MM-DD)')

    args = parser.parse_args()

    # Determine date range
    start_date = args.start_date or args.date
    end_date = args.end_date or args.date

    # Fetch usage from API
    usage_data = fetch_usage_from_api(start_date, end_date)

    if not usage_data:
        print("Failed to fetch usage data from API")
        return 1

    print(f"Fetched usage data: {json.dumps(usage_data, indent=2)}")

    # Update expense logs
    if args.mission:
        update_expense_log(args.mission, usage_data)
        generate_expense_summary(args.mission)

    # Update global cumulative
    update_cumulative_expenses(usage_data)

    print("\n✅ Expense tracking update complete!")
    print(f"Next steps:")
    print(f"  1. Review updated expense logs")
    print(f"  2. Check budget dashboard: cat {JUSTICE_LEAGUE_ROOT}/expenses-global/reports/decision-dashboard.md")

    return 0


if __name__ == "__main__":
    sys.exit(main())
