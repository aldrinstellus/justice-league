# Data Analysis & Metrics Skill

## Purpose
Key metrics, KPIs, and data analysis patterns for business intelligence, financial tracking, and performance monitoring.

## Auto-Activation Keywords
- "metrics"
- "kpi"
- "analytics"
- "data analysis"
- "dashboard"
- "reporting"

## Business Metrics Categories

### 1. Financial Metrics

**Revenue Metrics**:
- MRR (Monthly Recurring Revenue)
- ARR (Annual Recurring Revenue)
- Revenue Growth Rate = ((Current - Previous) / Previous) × 100
- ARPU (Average Revenue Per User) = Total Revenue / Total Users

**Profitability Metrics**:
- Gross Margin = (Revenue - COGS) / Revenue × 100
- Net Profit Margin = Net Income / Revenue × 100
- EBITDA = Earnings Before Interest, Taxes, Depreciation, Amortization

**Cash Flow Metrics**:
- Burn Rate = Cash Spent / Month
- Runway = Cash Balance / Monthly Burn Rate
- Cash Conversion Cycle = DIO + DSO - DPO

### 2. Growth Metrics

**User Acquisition**:
- CAC (Customer Acquisition Cost) = Marketing Spend / New Customers
- LTV (Lifetime Value) = ARPU × Average Customer Lifespan
- LTV:CAC Ratio (target: > 3:1)

**Engagement Metrics**:
- DAU (Daily Active Users)
- MAU (Monthly Active Users)
- DAU/MAU Ratio (stickiness, target: > 20%)
- Session Duration (avg time per visit)
- Session Frequency (visits per user per time period)

**Retention Metrics**:
- Retention Rate = (Users at End - New Users) / Users at Start × 100
- Churn Rate = Lost Customers / Total Customers × 100
- NRR (Net Revenue Retention) = (Revenue - Churn + Expansion) / Starting Revenue × 100

### 3. Product Metrics

**Adoption**:
- Feature Adoption Rate = Users Using Feature / Total Users × 100
- Time to First Value (how quickly users get value)
- Activation Rate = Activated Users / Signups × 100

**Engagement**:
- Feature Usage Frequency
- Feature Depth (how many features used per session)
- Power User Ratio = Power Users / Total Users

**Quality**:
- Error Rate = Errors / Total Requests × 100
- Crash Rate = Crashes / Total Sessions × 100
- API Response Time (p50, p95, p99)

### 4. Marketing Metrics

**Traffic**:
- Total Visitors
- Unique Visitors
- Traffic Sources (organic, paid, referral, direct)
- Bounce Rate = Single-Page Sessions / Total Sessions × 100

**Conversion**:
- Conversion Rate = Conversions / Visitors × 100
- Funnel Drop-off Rates
- Lead-to-Customer Conversion Rate

**ROI**:
- ROAS (Return on Ad Spend) = Revenue from Ads / Ad Spend
- CPA (Cost Per Acquisition) = Ad Spend / Acquisitions
- CPL (Cost Per Lead) = Marketing Spend / Leads Generated

### 5. Operational Metrics

**Performance**:
- Uptime = (Total Time - Downtime) / Total Time × 100
- Incident Response Time (mean, median, p95)
- Mean Time to Recovery (MTTR)

**Efficiency**:
- Throughput = Requests Processed / Time Period
- Resource Utilization = Used Resources / Total Resources × 100
- Cost Per Request = Infrastructure Cost / Total Requests

**Quality**:
- SLA Compliance Rate
- First Response Time (support)
- Resolution Time (support)

## Data Analysis Patterns

### Cohort Analysis

Track user groups over time:

```javascript
// Example: Monthly cohorts
const cohorts = {
  '2024-01': {
    users: 100,
    month0: 100, // 100% (signup month)
    month1: 75,  // 75% retained
    month2: 60,  // 60% retained
    month3: 55   // 55% retained
  },
  '2024-02': {
    users: 150,
    month0: 150,
    month1: 120, // 80% retained
    month2: 100, // 67% retained
  }
};

// Cohort retention rate = Users in Month N / Users in Month 0 × 100
```

### Funnel Analysis

Track conversion through stages:

```
Stage 1: Landing Page     → 10,000 visitors
Stage 2: Signup           → 2,000 (20% conversion)
Stage 3: Activation       → 1,400 (70% of signups, 14% overall)
Stage 4: Payment          → 700 (50% of activated, 7% overall)

Drop-off Analysis:
- Biggest drop: Landing → Signup (80% lost)
- Optimization priority: Improve signup CTA and value prop
```

### Segmentation Analysis

Group users by characteristics:

```javascript
// Segment by behavior
const segments = {
  powerUsers: {
    criteria: 'sessions > 20/month',
    count: 500,
    revenue: '$50,000',
    ltv: '$100'
  },
  casualUsers: {
    criteria: 'sessions 5-20/month',
    count: 2000,
    revenue: '$80,000',
    ltv: '$40'
  },
  dormant: {
    criteria: 'sessions < 5/month',
    count: 7500,
    revenue: '$20,000',
    ltv: '$2.67'
  }
};

// Action: Focus retention efforts on power users (highest LTV)
```

### Trend Analysis

Identify patterns over time:

```javascript
// Week-over-week growth
const wowGrowth = (currentWeek - previousWeek) / previousWeek × 100;

// Moving average (smooth out noise)
const movingAvg = (data, window) => {
  return data.map((val, idx, arr) => {
    const slice = arr.slice(Math.max(0, idx - window + 1), idx + 1);
    return slice.reduce((sum, v) => sum + v, 0) / slice.length;
  });
};

// Seasonality detection
// Compare same period across multiple years
const seasonalityFactor = currentMonth / avgOfSameMonthPreviousYears;
```

### A/B Testing Analysis

Statistical significance testing:

```javascript
// Sample data
const controlGroup = { visitors: 10000, conversions: 500 }; // 5%
const testGroup = { visitors: 10000, conversions: 600 }; // 6%

// Conversion rates
const controlRate = controlGroup.conversions / controlGroup.visitors;
const testRate = testGroup.conversions / testGroup.visitors;

// Relative improvement
const improvement = (testRate - controlRate) / controlRate × 100; // 20%

// Statistical significance (simplified)
// Use z-test or t-test for proper calculation
// p-value < 0.05 = statistically significant
```

## Dashboard Design Principles

### Visual Hierarchy
1. **Primary KPIs**: Large, prominent (top of dashboard)
2. **Secondary Metrics**: Medium size, grouped by category
3. **Detailed Data**: Tables, charts at bottom

### Chart Selection

**Line Chart**: Trends over time
```
Use for: Revenue over time, user growth, engagement trends
```

**Bar Chart**: Comparisons between categories
```
Use for: Revenue by product, users by country, feature usage
```

**Pie Chart**: Part-to-whole relationships (use sparingly)
```
Use for: Traffic sources, revenue mix (max 5-7 slices)
```

**Heatmap**: Intensity across two dimensions
```
Use for: Activity by day/hour, feature usage matrix
```

**Funnel**: Conversion flow
```
Use for: Signup flow, checkout process, onboarding steps
```

### Dashboard Anti-Patterns

❌ **Too many metrics** (cognitive overload)
✅ **3-5 primary metrics**, rest grouped/hidden

❌ **Misleading scales** (starting Y-axis at non-zero)
✅ **Start at zero** for bar/area charts

❌ **3D charts** (distort perception)
✅ **2D charts** (clear, accurate)

❌ **Rainbow colors** (no meaning)
✅ **Intentional color** (red=bad, green=good, gray=neutral)

## SQL for Analytics

### Common Queries

**Daily Active Users**:
```sql
SELECT
  DATE(event_time) as date,
  COUNT(DISTINCT user_id) as dau
FROM events
WHERE event_time >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY date
ORDER BY date;
```

**Retention Cohort**:
```sql
WITH cohorts AS (
  SELECT
    user_id,
    DATE_TRUNC('month', MIN(signup_date)) as cohort_month
  FROM users
  GROUP BY user_id
)
SELECT
  cohort_month,
  COUNT(DISTINCT user_id) as cohort_size,
  COUNT(DISTINCT CASE WHEN activity_month = cohort_month THEN user_id END) as month_0,
  COUNT(DISTINCT CASE WHEN activity_month = DATE_ADD(cohort_month, INTERVAL 1 MONTH) THEN user_id END) as month_1,
  COUNT(DISTINCT CASE WHEN activity_month = DATE_ADD(cohort_month, INTERVAL 2 MONTH) THEN user_id END) as month_2
FROM cohorts
JOIN user_activity USING(user_id)
GROUP BY cohort_month
ORDER BY cohort_month;
```

**Revenue by Product**:
```sql
SELECT
  product_name,
  SUM(amount) as total_revenue,
  COUNT(*) as num_purchases,
  AVG(amount) as avg_purchase_value
FROM purchases
WHERE purchase_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY product_name
ORDER BY total_revenue DESC;
```

## Metric Calculation Examples

### SaaS Metrics

**MRR Calculation**:
```javascript
const calculateMRR = (subscriptions) => {
  return subscriptions.reduce((total, sub) => {
    const monthlyAmount = sub.billingPeriod === 'monthly'
      ? sub.amount
      : sub.amount / 12; // Annual to monthly
    return total + monthlyAmount;
  }, 0);
};
```

**LTV Calculation**:
```javascript
const calculateLTV = (arpu, churnRate) => {
  // LTV = ARPU / Churn Rate
  // Example: $50 ARPU, 5% monthly churn
  // LTV = $50 / 0.05 = $1000
  return arpu / churnRate;
};
```

**CAC Payback Period**:
```javascript
const cacPaybackMonths = (cac, monthlyRevenue) => {
  // How many months to recover acquisition cost
  // Example: $300 CAC, $50 monthly revenue
  // Payback = 6 months
  return cac / monthlyRevenue;
};
```

## Visualization Libraries

**JavaScript**:
- Recharts (React)
- Chart.js (vanilla JS)
- D3.js (advanced, custom)
- Victory (React Native)

**Python**:
- Matplotlib (static plots)
- Plotly (interactive)
- Seaborn (statistical)
- Dash (web dashboards)

## MCP Dashboard Verification

Use Chrome DevTools MCP to verify dashboards render correctly:

```typescript
await mcp__chrome-devtools__navigate_page({
  url: "http://localhost:3000/analytics"
})
await mcp__chrome-devtools__take_screenshot({
  filePath: "dashboard-metrics.png"
})
```

**Result**: 50% faster dashboard QA with visual verification
