# Justice League Expense Tracking System - Technical Architecture

**Version**: 1.0.0
**Created**: 2025-11-03
**Maintained By**: Oracle (Justice League Coordinator)
**Purpose**: Complete documentation of expense tracking logic, data flow, and calculations

---

## 📋 Table of Contents

1. [System Overview](#system-overview)
2. [Folder Structure](#folder-structure)
3. [Data Flow](#data-flow)
4. [File Schemas](#file-schemas)
5. [Calculation Logic](#calculation-logic)
6. [5-Level Granularity System](#5-level-granularity-system)
7. [Budget Alert System](#budget-alert-system)
8. [Real-Time API Integration](#real-time-api-integration)
9. [How to Customize](#how-to-customize)
10. [Decision Logic](#decision-logic)

---

## 🎯 System Overview

### Purpose
Track AI token usage and costs across multiple missions to stay within monthly budget limits.

### Key Principles
1. **5-Level Granularity**: Activity → Task → File → Phase → Agent → Mission
2. **Real-Time Tracking**: Update after each activity via Anthropic API
3. **Multi-Month Support**: Large missions can span multiple billing cycles
4. **Automated Alerts**: Trigger warnings at budget thresholds (50%, 75%, 90%, 95%, 100%)
5. **Cost Optimization**: Track savings from Haiku, caching, and batch API

### Scope
- **Account**: aldrinstellus@gmail.com (Claude Max - $100/month)
- **Tracking Period**: Monthly (resets 1st of each month)
- **Missions**: Unlimited (constrained by monthly budget)
- **Granularity**: Per-token-level accuracy

---

## 📁 Folder Structure

```
justice-league-missions/
├── expenses-global/                    # GLOBAL TRACKING (cross-mission)
│   ├── account-config.json             # Claude Max plan configuration
│   ├── cumulative-expenses.json        # Cross-mission totals
│   ├── mission-forecasts.json          # Future mission planning
│   ├── EXPENSE-TRACKING-GUIDE.md       # User guide
│   ├── EXPENSE-SYSTEM-ARCHITECTURE.md  # This file (technical docs)
│   ├── scripts/                        # API integration
│   │   ├── .env                        # API key (gitignored)
│   │   ├── .env.example                # Template
│   │   ├── fetch-anthropic-usage.py    # Main API script
│   │   ├── requirements.txt            # Python deps
│   │   └── README.md                   # Script docs
│   └── reports/                        # Generated reports
│       ├── decision-dashboard.md       # GO/NO-GO tool
│       └── global-summary.md           # All-time performance
│
└── missions/JL-XXX-mission-name/       # PER-MISSION TRACKING
    └── expenses/
        ├── config/                     # Mission configuration
        │   ├── pricing-config.json     # AI model pricing (2025)
        │   └── budget-limits.json      # Mission budget allocation
        ├── logs/                       # Activity tracking
        │   └── expense-log.json        # Every activity logged
        └── reports/                    # Mission reports
            └── expense-summary.md      # Budget status
```

### File Relationships

```
                   ┌─────────────────────────────┐
                   │   account-config.json       │
                   │   (Plan limits: $100/month) │
                   └──────────┬──────────────────┘
                              │
                              ▼
                   ┌─────────────────────────────┐
                   │  cumulative-expenses.json   │
                   │  (All missions aggregated)  │
                   └──────────┬──────────────────┘
                              │
                 ┌────────────┴────────────┐
                 ▼                         ▼
    ┌────────────────────────┐  ┌────────────────────────┐
    │ JL-001/expenses/       │  │ JL-003/expenses/       │
    │ logs/expense-log.json  │  │ logs/expense-log.json  │
    └────────────────────────┘  └────────────────────────┘
                 │                         │
                 └────────────┬────────────┘
                              ▼
                   ┌─────────────────────────────┐
                   │  reports/                   │
                   │  decision-dashboard.md      │
                   │  global-summary.md          │
                   └─────────────────────────────┘
```

---

## 🔄 Data Flow

### Flow 1: Activity Logging (Manual)

```
1. User completes activity (e.g., "Analyze Figma file X")
   ↓
2. Log activity in expense-log.json:
   {
     "activityId": "JL-003-001",
     "timestamp": "2025-11-03T10:30:00Z",
     "agent": "aldrin",
     "phase": "phase1-discovery",
     "task": "figma-file-analysis",
     "file": "Q3-2025-LXP-Mobile",
     "model": "claude-sonnet-4.5",
     "tokens": {
       "input": 45000,
       "output": 22000,
       "cached": 12000
     }
   }
   ↓
3. Calculate cost using pricing-config.json:
   input_cost = 45000 * $0.000003 = $0.135
   output_cost = 22000 * $0.000015 = $0.330
   cache_cost = 12000 * $0.0000003 = $0.0036
   total_cost = $0.4686
   ↓
4. Add to expense-log.json with calculated cost
   ↓
5. Aggregate to cumulative-expenses.json
   ↓
6. Check budget thresholds → Trigger alerts if needed
   ↓
7. Regenerate reports (expense-summary.md, decision-dashboard.md)
```

### Flow 2: Real-Time API Sync (Automated)

```
1. User runs: python fetch-anthropic-usage.py --mission JL-003
   ↓
2. Script calls Anthropic API: GET /v1/usage
   {
     "start_date": "2025-11-03",
     "end_date": "2025-11-03"
   }
   ↓
3. API returns actual usage:
   {
     "data": [
       {
         "timestamp": "2025-11-03T10:30:00Z",
         "model": "claude-sonnet-4.5",
         "input_tokens": 45000,
         "output_tokens": 22000,
         "cost_usd": 0.4686
       }
     ]
   }
   ↓
4. Script updates expense-log.json with ACTUAL data
   ↓
5. Script updates cumulative-expenses.json
   ↓
6. Script regenerates reports
   ↓
7. User checks: cat ../reports/decision-dashboard.md
```

### Flow 3: Budget Decision (Before Starting Mission)

```
1. User checks: cat expenses-global/reports/decision-dashboard.md
   ↓
2. Dashboard shows:
   - Monthly budget: $100
   - Spent: $45.23
   - Committed: $50.00
   - Available: $4.77
   ↓
3. User wants to start new mission ($20 estimated)
   ↓
4. Check: $20 > $4.77? YES → CANNOT START
   ↓
5. Options:
   a) Wait for next month (Dec 1 = fresh $100)
   b) Reduce scope to <$5
   c) Split across 2 months
   ↓
6. User decides: Wait for December
   ↓
7. Add to mission-forecasts.json for planning
```

---

## 📊 File Schemas

### 1. account-config.json

**Purpose**: Claude Max plan configuration and monthly limits

```json
{
  "version": "1.0.0",
  "lastUpdated": "2025-11-03T00:00:00Z",

  "account": {
    "email": "aldrinstellus@gmail.com",
    "plan": "Claude Max",
    "planType": "pro",
    "subscriptionCost": 20.00,        // Monthly subscription fee
    "currency": "USD",
    "billingCycle": "monthly",
    "startDate": "2024-01-01"
  },

  "limits": {
    "monthly": {
      "estimatedTokens": 7500000,     // ~7.5M tokens/month
      "estimatedCost": 100.00,        // $100/month budget
      "note": "Actual Claude Max plan budget"
    },
    "daily": {
      "estimatedTokens": 250000,      // ~250K tokens/day average
      "estimatedCost": 3.25,          // ~$3.25/day average
      "note": "Daily average based on monthly limit"
    }
  },

  "alerts": {
    "monthlyThresholds": [50, 75, 90, 100],  // Alert at these % levels
    "alertEmail": "aldrinstellus@gmail.com",
    "autoStopAt": 100                 // Auto-stop at 100%
  },

  "optimization": {
    "enablePromptCaching": true,      // Use caching for 90% savings
    "preferHaikuForSimpleTasks": true,// Use Haiku (73% cheaper)
    "useBatchAPIWhenPossible": true,  // Use batch API (50% cheaper)
    "targetSavings": 60               // Target 60% cost reduction
  }
}
```

**How It's Used**:
- `limits.monthly.estimatedCost` → Monthly budget cap
- `alerts.monthlyThresholds` → Trigger warnings
- `optimization.*` → Cost reduction strategies

---

### 2. cumulative-expenses.json

**Purpose**: Cross-mission aggregated totals

```json
{
  "version": "1.0.0",
  "account": "aldrinstellus@gmail.com",
  "plan": "Claude Max",
  "lastUpdated": "2025-11-03T00:00:00Z",

  "totals": {
    "allTime": {
      "totalMissions": 3,
      "completedMissions": 1,
      "activeMissions": 1,
      "totalCost": 45.23,             // All-time total cost
      "totalInputTokens": 2500000,
      "totalOutputTokens": 1800000,
      "totalTokens": 4300000,
      "totalHours": 8.5,
      "totalDocuments": 30
    },

    "thisMonth": {
      "month": "2025-11",
      "spending": {
        "completed": 45.23,           // Spent on completed missions
        "committed": 50.00,           // Allocated to active missions
        "totalAllocated": 95.23,      // completed + committed
        "monthlyLimit": 100.00,
        "available": 4.77,            // monthlyLimit - totalAllocated
        "percentUsed": 95.2,          // (totalAllocated / monthlyLimit) * 100
        "percentCommitted": 50.0,     // (committed / monthlyLimit) * 100
        "percentSpent": 45.2          // (completed / monthlyLimit) * 100
      }
    }
  },

  "missions": [
    {
      "missionId": "JL-001",
      "status": "completed",
      "budget": {
        "estimated": 125.00,
        "actual": 45.23,
        "variance": -79.77,           // actual - estimated
        "variancePercent": -63.8      // (variance / estimated) * 100
      },
      "usage": {
        "inputTokens": 2500000,
        "outputTokens": 1800000,
        "totalTokens": 4300000
      }
    },
    {
      "missionId": "JL-003",
      "status": "active",
      "multiMonth": true,             // Spans multiple months
      "budget": {
        "total": 125.00,
        "november": 50.00,            // Nov allocation
        "december": 75.00,            // Dec allocation
        "spent": 0,
        "remaining": 125.00
      }
    }
  ],

  "budgetStatus": {
    "currentMonth": "2025-11",
    "monthlyBudget": 100.00,
    "spent": 45.23,
    "committed": 50.00,
    "totalAllocated": 95.23,
    "available": 4.77,
    "status": "critical",             // "good" | "caution" | "critical"
    "canStartNewMission": false,
    "maxNewMissionBudget": 4.77
  },

  "apiIntegration": {
    "enabled": true,
    "apiProvider": "Anthropic",
    "updateFrequency": "after-each-activity",
    "lastSync": null,                 // Updated by fetch-anthropic-usage.py
    "endpoints": {
      "usage": "https://api.anthropic.com/v1/usage"
    }
  }
}
```

**Key Calculations**:

```javascript
// Available budget
available = monthlyLimit - (completed + committed)
         = 100.00 - (45.23 + 50.00)
         = 4.77

// Percent used
percentUsed = (totalAllocated / monthlyLimit) * 100
            = (95.23 / 100.00) * 100
            = 95.2%

// Budget status
if (percentUsed >= 95) status = "critical"
else if (percentUsed >= 85) status = "caution"
else if (percentUsed >= 75) status = "warning"
else status = "good"

// Can start new mission?
canStartNewMission = (available > 0) && (status != "critical")
```

---

### 3. pricing-config.json (Per-Mission)

**Purpose**: AI model pricing for cost calculations

```json
{
  "version": "1.0.0",
  "lastUpdated": "2025-11-03",
  "source": "Anthropic Pricing (2025)",

  "models": {
    "claude-sonnet-4.5": {
      "name": "Claude Sonnet 4.5",
      "inputCostPerMillion": 3.00,        // $3 per 1M input tokens
      "outputCostPerMillion": 15.00,      // $15 per 1M output tokens
      "inputCostPerToken": 0.000003,      // $3 / 1M
      "outputCostPerToken": 0.000015,     // $15 / 1M

      "features": {
        "promptCaching": {
          "enabled": true,
          "cacheCostPerMillion": 0.30,    // $0.30 per 1M to write cache
          "cacheReadCostPerMillion": 0.03,// $0.03 per 1M to read cache
          "savingsPercent": 90            // 90% savings on cached reads
        },
        "batchAPI": {
          "enabled": true,
          "discountPercent": 50           // 50% discount vs real-time
        }
      }
    },

    "claude-haiku-4.5": {
      "name": "Claude Haiku 4.5",
      "inputCostPerMillion": 1.00,        // $1 per 1M input tokens
      "outputCostPerMillion": 5.00,       // $5 per 1M output tokens
      "inputCostPerToken": 0.000001,      // $1 / 1M
      "outputCostPerToken": 0.000005,     // $5 / 1M

      "savingsVsSonnet": {
        "inputSavings": 67,               // 67% cheaper than Sonnet
        "outputSavings": 67,
        "averageSavings": 67
      }
    }
  }
}
```

**How Cost Is Calculated**:

```javascript
// Example: Analyze Figma file with Sonnet
const activity = {
  model: "claude-sonnet-4.5",
  inputTokens: 45000,
  outputTokens: 22000,
  cachedTokens: 12000
};

// Load pricing
const pricing = pricingConfig.models["claude-sonnet-4.5"];

// Calculate costs
const inputCost = activity.inputTokens * pricing.inputCostPerToken;
              // = 45000 * 0.000003
              // = $0.135

const outputCost = activity.outputTokens * pricing.outputCostPerToken;
               // = 22000 * 0.000015
               // = $0.330

const cacheCost = activity.cachedTokens * pricing.features.promptCaching.cacheReadCostPerMillion / 1000000;
              // = 12000 * (0.03 / 1000000)
              // = $0.00036

const totalCost = inputCost + outputCost + cacheCost;
              // = 0.135 + 0.330 + 0.00036
              // = $0.4654

// Savings from caching
const noCacheCost = (activity.inputTokens + activity.cachedTokens) * pricing.inputCostPerToken;
                // = (45000 + 12000) * 0.000003
                // = $0.171

const cacheSavings = noCacheCost - (inputCost + cacheCost);
                 // = 0.171 - (0.135 + 0.00036)
                 // = $0.03564 (savings from caching)
```

---

### 4. budget-limits.json (Per-Mission)

**Purpose**: Mission budget allocation by phase and agent

```json
{
  "mission": {
    "missionId": "JL-003",
    "totalBudget": 125.00,
    "multiMonth": true,
    "monthAllocations": {
      "2025-11": 50.00,               // November allocation
      "2025-12": 75.00                // December allocation
    }
  },

  "perPhase": {
    "phase1-discovery": {
      "budget": 15.00,
      "duration": "Week 1-2",
      "month": "2025-11",
      "activities": [
        "Inventory Figma files",
        "Count pages and components",
        "Priority ranking"
      ]
    },
    "phase2-audit": {
      "budget": 20.00,
      "duration": "Week 3-4",
      "month": "2025-11"
    },
    "phase2-buffer": {
      "budget": 15.00,
      "duration": "Reserve",
      "month": "2025-11",
      "note": "Contingency for November overages"
    },
    "phase3-components": {
      "budget": 40.00,
      "duration": "Week 5-8",
      "month": "2025-12"
    }
    // ... phases 4-6
  },

  "perAgent": {
    "oracle": {
      "budget": 20.00,
      "preferredModel": "claude-haiku-4.5",  // Cost optimization
      "responsibilities": "Coordination, tracking, synthesis"
    },
    "wonder-woman": {
      "budget": 45.00,
      "preferredModel": "claude-sonnet-4.5",
      "responsibilities": "User flows, prioritization"
    },
    "aldrin": {
      "budget": 60.00,
      "preferredModel": "claude-sonnet-4.5",
      "responsibilities": "Token extraction, analysis"
    }
  },

  "alerts": {
    "thresholds": {
      "50": { "level": "info", "action": "Continue normally" },
      "75": { "level": "warning", "action": "Monitor closely" },
      "85": { "level": "caution", "action": "Enable optimizations" },
      "90": { "level": "alert", "action": "Reduce scope" },
      "95": { "level": "critical", "action": "Complete only" },
      "100": { "level": "stop", "action": "Auto-stop enabled" }
    },
    "email": "aldrinstellus@gmail.com",
    "enableAutoStop": true,
    "stopAtPercent": 100
  },

  "optimization": {
    "targetSavings": 60,              // Target 60% cost reduction
    "strategies": {
      "modelSelection": {
        "enabled": true,
        "estimatedSavings": 25.00,    // Use Haiku where possible
        "implementation": "Oracle uses Haiku, simple tasks use Haiku"
      },
      "promptCaching": {
        "enabled": true,
        "estimatedSavings": 45.00,    // Cache design system docs
        "implementation": "Cache across 100 Figma files"
      },
      "batchAPI": {
        "enabled": true,
        "estimatedSavings": 5.00,     // Batch non-urgent tasks
        "implementation": "Synthesis and reporting"
      }
    },
    "optimizedBudget": 50.00          // $125 → $50 with full optimization
  }
}
```

**Budget Alert Logic**:

```javascript
// Check budget threshold after each activity
function checkBudgetAlert(spent, budget, thresholds) {
  const percentUsed = (spent / budget) * 100;

  // Find highest triggered threshold
  let triggeredAlert = null;
  for (const [threshold, config] of Object.entries(thresholds)) {
    if (percentUsed >= parseInt(threshold)) {
      triggeredAlert = { threshold, ...config };
    }
  }

  if (triggeredAlert) {
    if (triggeredAlert.level === "stop") {
      // Auto-stop: prevent new activities
      return { canContinue: false, alert: triggeredAlert };
    } else if (triggeredAlert.level === "critical") {
      // Critical: warn but allow mission completion
      return { canContinue: true, alert: triggeredAlert };
    } else {
      // Warning levels: notify only
      return { canContinue: true, alert: triggeredAlert };
    }
  }

  return { canContinue: true, alert: null };
}

// Example
const result = checkBudgetAlert(
  47.50,  // $47.50 spent
  50.00,  // $50 budget
  thresholds
);
// result = {
//   canContinue: true,
//   alert: {
//     threshold: 95,
//     level: "critical",
//     action: "Complete only"
//   }
// }
```

---

### 5. expense-log.json (Per-Mission)

**Purpose**: Activity-level tracking (most granular)

```json
{
  "missionId": "JL-003",
  "missionName": "Auzmor-learn - Web&Mobile",
  "lastUpdated": "2025-11-03T10:30:00Z",

  "summary": {
    "totalActivities": 1,
    "totalCost": 0.4654,
    "totalTokens": 79000,
    "totalInputTokens": 57000,          // 45K input + 12K cached
    "totalOutputTokens": 22000
  },

  "activities": [
    {
      "activityId": "JL-003-001",
      "timestamp": "2025-11-03T10:30:00Z",
      "agent": "aldrin",
      "agentRole": "Design Systems Master",
      "phase": "phase1-discovery",
      "task": "figma-file-analysis",
      "file": "Q3-2025-LXP-Mobile.fig",
      "description": "Analyzed Figma file for color tokens",

      "model": {
        "name": "claude-sonnet-4.5",
        "version": "20250929"
      },

      "tokens": {
        "input": 45000,
        "output": 22000,
        "cached": 12000,                // Cached tokens (90% savings)
        "total": 79000                  // input + output + cached
      },

      "cost": {
        "input": 0.135,                 // 45K * $0.000003
        "output": 0.330,                // 22K * $0.000015
        "cache": 0.00036,               // 12K * $0.00000003
        "total": 0.4654,                // Sum of above
        "currency": "USD"
      },

      "optimization": {
        "cachingEnabled": true,
        "cacheSavings": 0.03564,        // Savings from caching
        "batchEligible": false,         // Real-time required
        "modelOptimal": true            // Sonnet appropriate for this task
      },

      "deliverables": [
        "Color token inventory",
        "Design system gaps analysis"
      ],

      "duration": {
        "startTime": "2025-11-03T10:00:00Z",
        "endTime": "2025-11-03T10:30:00Z",
        "durationMinutes": 30
      },

      "metadata": {
        "apiRequestId": "req_abc123",   // From Anthropic API
        "conversationId": "conv_xyz789",
        "source": "manual"              // "manual" | "api-sync"
      }
    }
    // ... more activities
  ],

  "aggregations": {
    "byAgent": {
      "oracle": { "activities": 0, "cost": 0, "tokens": 0 },
      "aldrin": { "activities": 1, "cost": 0.4654, "tokens": 79000 }
    },
    "byPhase": {
      "phase1-discovery": { "activities": 1, "cost": 0.4654, "tokens": 79000 }
    },
    "byTask": {
      "figma-file-analysis": { "activities": 1, "cost": 0.4654 }
    },
    "byFile": {
      "Q3-2025-LXP-Mobile.fig": { "activities": 1, "cost": 0.4654 }
    }
  }
}
```

**Activity Logging Workflow**:

```javascript
// Step 1: User completes activity
const activity = {
  agent: "aldrin",
  phase: "phase1-discovery",
  task: "figma-file-analysis",
  file: "Q3-2025-LXP-Mobile.fig",
  model: "claude-sonnet-4.5",
  tokens: {
    input: 45000,
    output: 22000,
    cached: 12000
  }
};

// Step 2: Calculate cost
const pricing = loadPricingConfig();
const cost = calculateCost(activity.tokens, activity.model, pricing);

// Step 3: Create activity entry
const activityEntry = {
  activityId: generateId("JL-003"),  // "JL-003-001"
  timestamp: new Date().toISOString(),
  ...activity,
  cost: cost,
  duration: calculateDuration(startTime, endTime)
};

// Step 4: Add to expense-log.json
expenseLog.activities.push(activityEntry);

// Step 5: Update aggregations
expenseLog.aggregations.byAgent[activity.agent].cost += cost.total;
expenseLog.aggregations.byPhase[activity.phase].cost += cost.total;
// ... update all aggregation levels

// Step 6: Update summary
expenseLog.summary.totalCost += cost.total;
expenseLog.summary.totalTokens += activity.tokens.total;

// Step 7: Save to file
saveExpenseLog(expenseLog);

// Step 8: Update cumulative expenses
updateCumulativeExpenses(activityEntry);

// Step 9: Check budget alerts
checkBudgetAlerts(expenseLog.summary.totalCost, budgetLimits.mission.totalBudget);
```

---

## 🔢 Calculation Logic

### Cost Calculation Formula

```javascript
// For each activity
function calculateActivityCost(tokens, model, pricingConfig) {
  const pricing = pricingConfig.models[model];

  // Input cost
  const inputCost = tokens.input * pricing.inputCostPerToken;

  // Output cost
  const outputCost = tokens.output * pricing.outputCostPerToken;

  // Cache cost (if caching enabled)
  let cacheCost = 0;
  if (tokens.cached > 0 && pricing.features.promptCaching.enabled) {
    const cacheReadRate = pricing.features.promptCaching.cacheReadCostPerMillion / 1_000_000;
    cacheCost = tokens.cached * cacheReadRate;
  }

  // Total cost
  const totalCost = inputCost + outputCost + cacheCost;

  // Calculate savings
  let savings = 0;
  if (tokens.cached > 0) {
    const noCacheCost = (tokens.input + tokens.cached) * pricing.inputCostPerToken;
    savings = noCacheCost - (inputCost + cacheCost);
  }

  return {
    input: inputCost,
    output: outputCost,
    cache: cacheCost,
    total: totalCost,
    savings: savings,
    currency: "USD"
  };
}
```

### Budget Aggregation Formula

```javascript
// Aggregate across all activities in a mission
function aggregateMissionCost(expenseLog) {
  let totalCost = 0;
  let totalInputTokens = 0;
  let totalOutputTokens = 0;
  let totalCachedTokens = 0;

  for (const activity of expenseLog.activities) {
    totalCost += activity.cost.total;
    totalInputTokens += activity.tokens.input;
    totalOutputTokens += activity.tokens.output;
    totalCachedTokens += activity.tokens.cached;
  }

  return {
    totalCost,
    totalInputTokens,
    totalOutputTokens,
    totalCachedTokens,
    totalTokens: totalInputTokens + totalOutputTokens + totalCachedTokens
  };
}

// Aggregate across all missions
function aggregateGlobalCost(missions) {
  let allTimeCost = 0;
  let thisMonthCost = 0;
  const currentMonth = "2025-11";

  for (const mission of missions) {
    allTimeCost += mission.budget.actual || mission.budget.spent;

    if (mission.month === currentMonth ||
        (mission.multiMonth && mission.month.includes(currentMonth))) {
      thisMonthCost += mission.budget.spent || 0;
    }
  }

  return { allTimeCost, thisMonthCost };
}
```

### Available Budget Calculation

```javascript
function calculateAvailableBudget(monthlyLimit, completedSpend, committedBudget) {
  // Total allocated = what's spent + what's promised
  const totalAllocated = completedSpend + committedBudget;

  // Available = monthly limit - total allocated
  const available = monthlyLimit - totalAllocated;

  // Percent used
  const percentUsed = (totalAllocated / monthlyLimit) * 100;

  // Status determination
  let status;
  if (percentUsed >= 95) status = "critical";
  else if (percentUsed >= 85) status = "caution";
  else if (percentUsed >= 75) status = "warning";
  else status = "good";

  // Can start new mission?
  const canStartNewMission = (available > 0) && (status !== "critical");

  return {
    monthlyLimit,
    totalAllocated,
    available,
    percentUsed,
    status,
    canStartNewMission,
    maxNewMissionBudget: Math.max(0, available)
  };
}

// Example
const result = calculateAvailableBudget(
  100.00,  // $100 monthly limit
  45.23,   // $45.23 spent (JL-001)
  50.00    // $50 committed (JL-003 Nov)
);
// result = {
//   monthlyLimit: 100.00,
//   totalAllocated: 95.23,
//   available: 4.77,
//   percentUsed: 95.2,
//   status: "critical",
//   canStartNewMission: false,
//   maxNewMissionBudget: 4.77
// }
```

---

## 🎯 5-Level Granularity System

### Level 1: Activity (Most Granular)

**Definition**: Single API call or task performed by an agent

**Example**:
```json
{
  "activityId": "JL-003-001",
  "description": "Analyze Figma file for color tokens",
  "cost": 0.4654
}
```

**Tracked In**: `missions/JL-XXX/expenses/logs/expense-log.json`

**Use Case**: Understand exactly where tokens are being spent

---

### Level 2: Task

**Definition**: Group of related activities completing a specific objective

**Example**:
```json
{
  "task": "figma-file-analysis",
  "activities": ["JL-003-001", "JL-003-002", "JL-003-003"],
  "totalCost": 1.25
}
```

**Tracked In**: `aggregations.byTask` in expense-log.json

**Use Case**: Compare cost of different task types (analysis vs synthesis)

---

### Level 3: File

**Definition**: All activities related to processing a single file

**Example**:
```json
{
  "file": "Q3-2025-LXP-Mobile.fig",
  "activities": 5,
  "totalCost": 2.35
}
```

**Tracked In**: `aggregations.byFile` in expense-log.json

**Use Case**: Know cost per Figma file for budgeting future file analysis

---

### Level 4: Phase

**Definition**: Mission phase containing multiple tasks

**Example**:
```json
{
  "phase": "phase1-discovery",
  "budget": 15.00,
  "spent": 5.75,
  "remaining": 9.25
}
```

**Tracked In**: `aggregations.byPhase` in expense-log.json

**Use Case**: Track progress through mission phases against phase budgets

---

### Level 5: Agent

**Definition**: All activities performed by a specific agent

**Example**:
```json
{
  "agent": "aldrin",
  "budget": 60.00,
  "spent": 12.50,
  "activities": 15
}
```

**Tracked In**: `aggregations.byAgent` in expense-log.json

**Use Case**: Balance workload and cost across agents

---

### Aggregation Flow

```
Activity (JL-003-001)
  ↓
Task (figma-file-analysis)
  ↓
File (Q3-2025-LXP-Mobile.fig)
  ↓
Phase (phase1-discovery)
  ↓
Agent (aldrin)
  ↓
Mission (JL-003)
  ↓
Global (All missions)
```

**Query Examples**:

```javascript
// How much did aldrin spend on phase1-discovery?
const cost = expenseLog.activities
  .filter(a => a.agent === "aldrin" && a.phase === "phase1-discovery")
  .reduce((sum, a) => sum + a.cost.total, 0);

// Which Figma file cost the most?
const fileCosts = expenseLog.aggregations.byFile;
const mostExpensive = Object.entries(fileCosts)
  .sort((a, b) => b[1].cost - a[1].cost)[0];

// What's the average cost per activity?
const avgCost = expenseLog.summary.totalCost / expenseLog.summary.totalActivities;

// What % of budget has aldrin used?
const aldrinPercent = (aggregations.byAgent.aldrin.cost / budgetLimits.perAgent.aldrin.budget) * 100;
```

---

## 🚨 Budget Alert System

### Alert Thresholds

```javascript
const THRESHOLDS = {
  50: { level: "info", icon: "ℹ️", action: "Continue normally" },
  75: { level: "warning", icon: "⚠️", action: "Monitor closely" },
  85: { level: "caution", icon: "⚠️", action: "Enable optimizations" },
  90: { level: "alert", icon: "🚨", action: "Reduce scope or stop new tasks" },
  95: { level: "critical", icon: "🚨", action: "Complete mission only" },
  100: { level: "stop", icon: "🛑", action: "Auto-stop enabled" }
};
```

### Alert Logic

```javascript
function checkAlerts(spent, budget, thresholds) {
  const percentUsed = (spent / budget) * 100;
  const alerts = [];

  for (const [threshold, config] of Object.entries(thresholds)) {
    if (percentUsed >= parseInt(threshold)) {
      alerts.push({
        threshold: parseInt(threshold),
        percentUsed: percentUsed.toFixed(1),
        ...config,
        triggered: true,
        timestamp: new Date().toISOString()
      });
    }
  }

  // Return highest alert
  return alerts.length > 0 ? alerts[alerts.length - 1] : null;
}

// Example
const alert = checkAlerts(95.23, 100.00, THRESHOLDS);
// alert = {
//   threshold: 95,
//   percentUsed: "95.2",
//   level: "critical",
//   icon: "🚨",
//   action: "Complete mission only",
//   triggered: true,
//   timestamp: "2025-11-03T10:30:00Z"
// }
```

### Auto-Stop Logic

```javascript
function shouldAutoStop(spent, budget, enableAutoStop) {
  if (!enableAutoStop) return false;

  const percentUsed = (spent / budget) * 100;
  return percentUsed >= 100;
}

// Before allowing new activity
function canPerformActivity(missionBudget, enableAutoStop) {
  const spent = calculateSpentBudget();

  if (shouldAutoStop(spent, missionBudget, enableAutoStop)) {
    return {
      allowed: false,
      reason: "Budget 100% consumed. Auto-stop enabled.",
      alert: THRESHOLDS[100]
    };
  }

  return { allowed: true };
}
```

---

## 🔌 Real-Time API Integration

### API Call Flow

```python
# fetch-anthropic-usage.py

def fetch_usage_from_api(start_date, end_date):
    """Fetch actual usage from Anthropic API"""

    headers = {
        "x-api-key": os.getenv("ANTHROPIC_API_KEY"),
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }

    params = {
        "start_date": start_date,  # "2025-11-03"
        "end_date": end_date        # "2025-11-03"
    }

    response = requests.get(
        "https://api.anthropic.com/v1/usage",
        headers=headers,
        params=params
    )

    return response.json()
```

### API Response Format (Expected)

```json
{
  "data": [
    {
      "timestamp": "2025-11-03T10:30:00Z",
      "model": "claude-sonnet-4.5",
      "input_tokens": 45000,
      "output_tokens": 22000,
      "cached_tokens": 12000,
      "cost_usd": 0.4654,
      "metadata": {
        "conversation_id": "conv_xyz789",
        "request_id": "req_abc123"
      }
    }
  ],
  "total_cost_usd": 0.4654,
  "period": {
    "start": "2025-11-03T00:00:00Z",
    "end": "2025-11-03T23:59:59Z"
  }
}
```

### Update Logic

```python
def update_expense_log(mission_id, api_data):
    """Update expense log with real API data"""

    # Load existing log
    log_path = f"missions/{mission_id}/expenses/logs/expense-log.json"
    with open(log_path, 'r') as f:
        expense_log = json.load(f)

    # Process each API activity
    for api_activity in api_data['data']:
        # Check if already logged
        existing = find_activity_by_timestamp(
            expense_log.activities,
            api_activity['timestamp']
        )

        if existing:
            # Update with actual data
            existing['tokens'] = {
                'input': api_activity['input_tokens'],
                'output': api_activity['output_tokens'],
                'cached': api_activity['cached_tokens']
            }
            existing['cost']['total'] = api_activity['cost_usd']
            existing['metadata']['apiRequestId'] = api_activity['metadata']['request_id']
            existing['metadata']['source'] = 'api-sync'
        else:
            # Create new activity from API data
            new_activity = create_activity_from_api(api_activity)
            expense_log['activities'].append(new_activity)

    # Recalculate aggregations
    expense_log['aggregations'] = recalculate_aggregations(expense_log['activities'])

    # Update summary
    expense_log['summary'] = calculate_summary(expense_log['activities'])

    # Save updated log
    with open(log_path, 'w') as f:
        json.dump(expense_log, f, indent=2)

    return expense_log
```

---

## 🛠️ How to Customize

### 1. Change Monthly Budget

**File**: `expenses-global/account-config.json`

```json
{
  "limits": {
    "monthly": {
      "estimatedCost": 150.00  // Change from 100 to 150
    }
  }
}
```

**Impact**: All budget calculations, alerts, and dashboard will reflect new limit

---

### 2. Modify Alert Thresholds

**File**: `missions/JL-XXX/expenses/config/budget-limits.json`

```json
{
  "alerts": {
    "thresholds": {
      "60": { "level": "info" },      // Add new threshold
      "80": { "level": "warning" },   // Modify existing
      "95": { "level": "critical" }
    }
  }
}
```

---

### 3. Add Custom Cost Optimization

**File**: `missions/JL-XXX/expenses/config/budget-limits.json`

```json
{
  "optimization": {
    "strategies": {
      "customStrategy": {
        "enabled": true,
        "estimatedSavings": 10.00,
        "implementation": "Use smaller context windows"
      }
    }
  }
}
```

---

### 4. Change Model Pricing

**File**: `missions/JL-XXX/expenses/config/pricing-config.json`

```json
{
  "models": {
    "claude-sonnet-4.5": {
      "inputCostPerMillion": 2.50  // Update if pricing changes
    }
  }
}
```

---

### 5. Add New Granularity Level

**File**: `missions/JL-XXX/expenses/logs/expense-log.json`

```json
{
  "aggregations": {
    "byCustomLevel": {
      "level1": { "cost": 0, "activities": 0 }
    }
  }
}
```

Then update aggregation logic to track new level.

---

### 6. Customize Real-Time Update Frequency

**File**: `expenses-global/scripts/.env`

```bash
# Change from after-each-activity to daily
UPDATE_FREQUENCY=daily
```

Then modify cron job or manual workflow accordingly.

---

## 🧠 Decision Logic

### Can We Start a New Mission?

```javascript
function canStartNewMission(estimatedBudget) {
  // Load current state
  const cumulative = loadCumulativeExpenses();
  const available = cumulative.budgetStatus.available;
  const status = cumulative.budgetStatus.status;

  // Decision tree
  if (status === "critical") {
    return {
      decision: "NO",
      reason: "Current month is 95%+ allocated (critical status)",
      options: [
        "Wait for next month (fresh budget)",
        "Reduce mission scope to fit available budget",
        "Split mission across multiple months"
      ]
    };
  }

  if (estimatedBudget > available) {
    return {
      decision: "NO",
      reason: `Mission needs $${estimatedBudget}, only $${available} available`,
      options: [
        `Reduce scope to <$${available}`,
        "Wait for next month",
        "Structure as multi-month mission"
      ]
    };
  }

  if (estimatedBudget <= available && status !== "critical") {
    return {
      decision: "YES",
      reason: `Mission fits within available budget ($${available})`,
      recommendations: [
        "Enable cost optimizations from start",
        "Use Haiku for simple tasks",
        "Enable prompt caching if analyzing multiple files"
      ]
    };
  }
}
```

### Should We Enable Optimizations?

```javascript
function shouldEnableOptimizations(currentSpend, budget) {
  const percentUsed = (currentSpend / budget) * 100;

  if (percentUsed >= 75) {
    return {
      enable: true,
      reason: "Budget 75%+ used",
      strategies: [
        "Switch to Haiku for remaining simple tasks",
        "Enable prompt caching for repeated content",
        "Defer non-urgent tasks to batch API"
      ],
      estimatedSavings: calculateOptimizationSavings(budget - currentSpend)
    };
  }

  return {
    enable: false,
    reason: "Budget usage healthy (<75%)",
    recommendation: "Continue current approach"
  };
}
```

### Multi-Month Mission Planning

```javascript
function planMultiMonthMission(totalBudget, monthlyLimit) {
  const monthsNeeded = Math.ceil(totalBudget / monthlyLimit);

  if (monthsNeeded === 1) {
    return {
      structure: "single-month",
      allocation: { month1: totalBudget }
    };
  }

  // Split budget across months
  const allocations = {};
  let remaining = totalBudget;

  for (let i = 1; i <= monthsNeeded; i++) {
    const monthKey = `month${i}`;
    const allocation = Math.min(remaining, monthlyLimit);
    allocations[monthKey] = allocation;
    remaining -= allocation;
  }

  return {
    structure: "multi-month",
    monthsNeeded: monthsNeeded,
    allocations: allocations,
    example: "JL-003: Nov $50 + Dec $75 = $125 total"
  };
}

// Example
const plan = planMultiMonthMission(125.00, 100.00);
// plan = {
//   structure: "multi-month",
//   monthsNeeded: 2,
//   allocations: {
//     month1: 100.00,
//     month2: 25.00
//   }
// }
```

---

## 📝 Summary

**This expense tracking system provides**:

1. **5-Level Granularity**: Activity → Task → File → Phase → Agent → Mission
2. **Real-Time Accuracy**: Anthropic API integration for actual usage data
3. **Multi-Month Support**: Large missions span multiple billing cycles
4. **Budget Protection**: Alerts at 50%, 75%, 85%, 90%, 95%, 100%
5. **Cost Optimization**: Track savings from Haiku, caching, batch API
6. **Full Transparency**: Every token tracked, every dollar accounted

**Key Files**:
- `account-config.json` - Plan limits ($100/month)
- `cumulative-expenses.json` - Cross-mission totals
- `budget-limits.json` - Per-mission allocation
- `expense-log.json` - Activity-level tracking
- `decision-dashboard.md` - GO/NO-GO tool

**Customization**: All thresholds, prices, and logic can be modified in JSON config files.

---

**Created By**: Oracle
**Date**: 2025-11-03
**For**: aldrinstellus@gmail.com
**Account**: Claude Max ($100/month)
