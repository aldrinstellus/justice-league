#!/usr/bin/env python3
"""
Simple Justice League Budget Checker
Quick status check of monthly budget
"""

import json
import os
from datetime import datetime

# Configuration
BUDGET_FILE = "../simple-budget.json"
MONTHLY_BUDGET = 100.00


def load_budget():
    """Load simple budget tracking file"""
    budget_path = os.path.join(os.path.dirname(__file__), BUDGET_FILE)

    if not os.path.exists(budget_path):
        print("⚠️  simple-budget.json not found. Creating new file...")
        return {
            "monthlyBudget": MONTHLY_BUDGET,
            "currentMonth": datetime.now().strftime("%B").lower() + datetime.now().strftime("%Y"),
            "tasks": []
        }

    with open(budget_path, 'r') as f:
        return json.load(f)


def format_currency(amount):
    """Format amount as currency"""
    return f"${amount:,.2f}"


def get_status_emoji(percentage):
    """Get status emoji based on percentage used"""
    if percentage < 50:
        return "✅"
    elif percentage < 75:
        return "⚠️"
    elif percentage < 95:
        return "🚨"
    else:
        return "❌"


def main():
    """Check and display budget status"""
    budget_data = load_budget()

    # Get current month key
    current_month = datetime.now().strftime("%B").lower() + datetime.now().strftime("%Y")

    # Calculate spent amount for current month
    spent = 0.0
    if current_month in budget_data:
        tasks = budget_data[current_month].get("tasks", [])
        spent = sum(task.get("total", 0) for task in tasks if task.get("status") == "complete")

    # Calculate remaining and percentage
    monthly_budget = budget_data.get("monthlyBudget", MONTHLY_BUDGET)
    remaining = monthly_budget - spent
    percentage = (spent / monthly_budget * 100) if monthly_budget > 0 else 0

    # Determine status
    status_emoji = get_status_emoji(percentage)

    if percentage < 75:
        status = "HEALTHY"
    elif percentage < 95:
        status = "CAUTION"
    elif percentage < 100:
        status = "CRITICAL"
    else:
        status = "OVER BUDGET"

    # Display budget status
    print("═" * 60)
    print("🔮 JUSTICE LEAGUE BUDGET STATUS")
    print("═" * 60)
    print(f"Month:     {datetime.now().strftime('%B %Y')}")
    print(f"Budget:    {format_currency(monthly_budget)}")
    print(f"Spent:     {format_currency(spent)}  ({percentage:.1f}%)")
    print(f"Remaining: {format_currency(remaining)}  ({100-percentage:.1f}%)")
    print(f"Status:    {status_emoji} {status}")
    print("═" * 60)

    # Display tasks if any
    if current_month in budget_data and budget_data[current_month].get("tasks"):
        tasks = budget_data[current_month]["tasks"]
        completed_tasks = [t for t in tasks if t.get("status") == "complete"]

        if completed_tasks:
            print(f"\n✅ Completed Tasks ({len(completed_tasks)}):")
            for task in completed_tasks:
                task_id = task.get("id", "Unknown")
                task_total = task.get("total", 0)
                print(f"   • {task_id}: {format_currency(task_total)}")

        pending_tasks = [t for t in tasks if t.get("status") == "pending"]
        if pending_tasks:
            print(f"\n⏳ Pending Tasks ({len(pending_tasks)}):")
            for task in pending_tasks:
                task_id = task.get("id", "Unknown")
                task_total = task.get("total", 0)
                print(f"   • {task_id}: ~{format_currency(task_total)}")

    print()

    # Recommendations
    if percentage < 50:
        print("💡 Healthy budget. You can take on more work.")
    elif percentage < 75:
        print("💡 Good progress. Continue monitoring spending.")
    elif percentage < 90:
        print("⚠️  Approaching limit. Consider smaller tasks only.")
    elif percentage < 100:
        print("🚨 Critical! Mission completion only. No new work.")
    else:
        print("❌ Over budget! Wait for next month or reduce scope.")

    print()


if __name__ == "__main__":
    main()
