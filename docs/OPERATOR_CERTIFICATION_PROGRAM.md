# 🎓 Oracle Operator Certification Program

**Program Version**: 1.0.0
**Duration**: 4-6 hours (training + certification)
**Passing Score**: 80% (24/30 questions)
**Validity**: 12 months

---

## Program Overview

This certification program validates that operators have the knowledge and skills to safely operate, monitor, and maintain Oracle in production. Operators must complete the training manual and pass this certification exam.

### Prerequisites
- Read: `OPERATOR_TRAINING_MANUAL.md` (4-6 hours)
- Read: `OPERATIONAL_RUNBOOKS.md` (2-3 hours)
- Read: `TROUBLESHOOTING_GUIDE.md` (1-2 hours)
- Complete: All 5 hands-on exercises

### Certification Levels
- **Level 1**: Operator (Monitor and basic operations)
- **Level 2**: Senior Operator (All operations including deployment)
- **Level 3**: On-Call Engineer (Incident response and emergency procedures)

---

## Level 1: Operator Certification

### Part 1: Core Concepts (10 questions)

#### Question 1: Oracle Purpose
**What is the primary purpose of Oracle?**

A) Replace Superman as the coordinator
B) Monitor and maintain the 11 Justice League agents
C) Write code for the agents
D) Deploy applications to production

<details>
<summary>✅ Correct Answer</summary>
**B) Monitor and maintain the 11 Justice League agents**

Oracle is a meta-agent that monitors health, coordinates updates, and maintains the Justice League of 11 specialized agents.
</details>

---

#### Question 2: Justice League Agents
**How many agents does Oracle manage?**

A) 5 agents
B) 7 agents
C) 11 agents
D) 15 agents

<details>
<summary>✅ Correct Answer</summary>
**C) 11 agents**

Oracle manages exactly 11 Justice League agents, from Superman (coordinator) to Cyborg (monitoring).
</details>

---

#### Question 3: Health Status Levels
**What are the 4 health status levels in Oracle? (Select all that apply)**

A) Healthy
B) OK
C) Warning
D) Unhealthy
E) Critical
F) Failed

<details>
<summary>✅ Correct Answer</summary>
**A) Healthy, C) Warning, D) Unhealthy, E) Critical**

Oracle uses a 4-level health system: Healthy → Warning → Unhealthy → Critical
</details>

---

#### Question 4: Morning Health Check
**What is the target for overall system health in the morning check?**

A) > 50%
B) > 75%
C) > 90%
D) 100%

<details>
<summary>✅ Correct Answer</summary>
**C) > 90%**

System health should be above 90% for healthy production operation. Below 90% requires investigation.
</details>

---

#### Question 5: Self-Healing
**When does Oracle automatically apply a fix without human approval?**

A) Always
B) When risk level is LOW
C) When risk level is MEDIUM
D) Never - always requires approval

<details>
<summary>✅ Correct Answer</summary>
**B) When risk level is LOW**

Oracle auto-applies fixes only when risk is LOW. MEDIUM requires approval, HIGH requires senior approval.
</details>

---

#### Question 6: Version Control
**What versioning scheme does Oracle use?**

A) Date-based (YYYY-MM-DD)
B) Sequential (v1, v2, v3)
C) Semantic (MAJOR.MINOR.PATCH)
D) Random UUID

<details>
<summary>✅ Correct Answer</summary>
**C) Semantic (MAJOR.MINOR.PATCH)**

Oracle uses semantic versioning: MAJOR for breaking changes, MINOR for features, PATCH for bug fixes.
</details>

---

#### Question 7: Learning System
**What triggers Oracle's learning system to create a new insight?**

A) Manual operator request
B) Pattern recognition across multiple agents
C) Daily scheduled scan
D) Superman's command

<details>
<summary>✅ Correct Answer</summary>
**B) Pattern recognition across multiple agents**

Oracle's learning system automatically detects patterns when the same issue or success occurs across multiple agents.
</details>

---

#### Question 8: Superman Integration
**What is Superman's role in the Oracle system?**

A) Superman manages Oracle
B) Oracle manages Superman
C) Superman coordinates agents, Oracle maintains them
D) They operate independently

<details>
<summary>✅ Correct Answer</summary>
**C) Superman coordinates agents, Oracle maintains them**

"Superman leads, Oracle supports." Superman handles task coordination, Oracle handles agent health and maintenance.
</details>

---

#### Question 9: Response Time SLA
**What is the p95 target for health check operations?**

A) < 100ms
B) < 500ms
C) < 1000ms
D) < 2000ms

<details>
<summary>✅ Correct Answer</summary>
**B) < 500ms**

Health checks must complete in under 500ms at the 95th percentile. System scan has a 2000ms target.
</details>

---

#### Question 10: Knowledge Base
**Where does Oracle store its knowledge base in production?**

A) PostgreSQL database
B) SQLite file (oracle.db)
C) JSON files in /tmp
D) Redis cache

<details>
<summary>✅ Correct Answer</summary>
**B) SQLite file (oracle.db)**

Oracle uses SQLite with WAL mode for its knowledge base, optimized for 11 agents.
</details>

---

### Part 2: Operations (10 questions)

#### Question 11: Starting Oracle
**What command starts Oracle in production?**

A) `python3 oracle.py`
B) `./deployment/deploy.sh production`
C) `docker-compose up -d`
D) `systemctl start oracle`

<details>
<summary>✅ Correct Answer</summary>
**B) `./deployment/deploy.sh production`**

Production deployment uses the deploy.sh script, which handles backup, health checks, and blue-green deployment.
</details>

---

#### Question 12: Health Check Command
**What command runs a health check?**

A) `oracle health`
B) `python3 deployment/health_check.py`
C) `./check_health.sh`
D) `curl http://localhost:8000/health`

<details>
<summary>✅ Correct Answer</summary>
**B) `python3 deployment/health_check.py`**

The health check script performs 8 comprehensive checks and returns 0 (healthy), 1 (unhealthy), or 2 (degraded).
</details>

---

#### Question 13: Agent Status
**If Batman agent shows "Warning" status, what should you do first?**

A) Immediately restart Oracle
B) Check recent metrics and logs for Batman
C) Roll back to previous version
D) Notify Superman

<details>
<summary>✅ Correct Answer</summary>
**B) Check recent metrics and logs for Batman**

Warning status indicates investigation needed but not critical. Check metrics first, then assess if action needed.
</details>

---

#### Question 14: Applying Fixes
**Before applying a MEDIUM-risk fix, you must:**

A) Apply immediately - it's already approved
B) Get operator approval
C) Get senior operator or manager approval
D) Wait for automatic application

<details>
<summary>✅ Correct Answer</summary>
**C) Get senior operator or manager approval**

MEDIUM-risk fixes require senior approval. Only LOW-risk fixes can be applied by operators.
</details>

---

#### Question 15: Version Rollback
**What information do you need before rolling back a version?**

A) Just the target version number
B) Target version and safety assessment
C) Approval from Superman
D) No information needed

<details>
<summary>✅ Correct Answer</summary>
**B) Target version and safety assessment**

Always check rollback safety level (safe/caution/dangerous) and breaking changes before rolling back.
</details>

---

#### Question 16: Monitoring Dashboards
**Where are Oracle's Grafana dashboards accessed?**

A) http://localhost:3000
B) http://localhost:8080
C) http://localhost:9090
D) http://localhost:5000

<details>
<summary>✅ Correct Answer</summary>
**A) http://localhost:3000**

Grafana runs on port 3000. Prometheus is 9090, Oracle API would be 8000.
</details>

---

#### Question 17: System Scan Frequency
**How often should a full system scan be run?**

A) Hourly
B) Daily
C) Weekly
D) Monthly

<details>
<summary>✅ Correct Answer</summary>
**C) Weekly**

Full system scans are run weekly (or before major changes). Daily health checks are sufficient for routine monitoring.
</details>

---

#### Question 18: Alert Threshold
**At what health percentage should you escalate to on-call engineer?**

A) < 95%
B) < 90%
C) < 75%
D) < 50%

<details>
<summary>✅ Correct Answer</summary>
**C) < 75%**

Below 90% requires investigation. Below 75% requires escalation to on-call engineer. Below 50% is critical.
</details>

---

#### Question 19: Backup Verification
**How often should backup restores be tested?**

A) Daily
B) Weekly
C) Monthly
D) Only when needed

<details>
<summary>✅ Correct Answer</summary>
**C) Monthly**

Backups are created daily, but restore testing should be done monthly to ensure backup integrity.
</details>

---

#### Question 20: Incident Logging
**When should you create an incident ticket?**

A) Only for P0 incidents
B) For any health below 90%
C) For any unplanned issue requiring investigation
D) Only after system recovery

<details>
<summary>✅ Correct Answer</summary>
**C) For any unplanned issue requiring investigation**

Document all incidents for tracking, learning, and metrics. This includes degraded performance, warnings, and unexpected behavior.
</details>

---

### Part 3: Troubleshooting (10 questions)

#### Question 21: Agent Unresponsive
**If an agent shows as "Critical" for 15+ minutes, what is your first action?**

A) Restart Oracle immediately
B) Follow the "Agent Not Responding" runbook
C) Wait 30 minutes to see if it recovers
D) Roll back to previous version

<details>
<summary>✅ Correct Answer</summary>
**B) Follow the "Agent Not Responding" runbook**

Always follow runbooks for systematic troubleshooting. Runbook will guide through diagnosis and resolution steps.
</details>

---

#### Question 22: High Error Rate
**Error rate suddenly jumps to 15%. What should you do?**

A) Immediately roll back
B) Check recent changes and monitor for 5 minutes
C) Restart all services
D) Notify stakeholders

<details>
<summary>✅ Correct Answer</summary>
**B) Check recent changes and monitor for 5 minutes**

10-50% error rate is manual rollback territory but check context first. If sustained >5 min or trending up, initiate rollback.
</details>

---

#### Question 23: Database Locked
**If you see "database is locked" errors, what is the likely cause?**

A) Disk full
B) Concurrent access without WAL mode
C) Corrupted database
D) Wrong permissions

<details>
<summary>✅ Correct Answer</summary>
**B) Concurrent access without WAL mode**

SQLite requires WAL (Write-Ahead Logging) mode for concurrent access. Check database journal mode.
</details>

---

#### Question 24: Disk Space
**What is the minimum free disk space required for Oracle operation?**

A) 100 MB
B) 500 MB
C) 1 GB
D) 5 GB

<details>
<summary>✅ Correct Answer</summary>
**C) 1 GB**

Oracle requires at least 1 GB free disk space for database growth, logs, and backups.
</details>

---

#### Question 25: Performance Degradation
**System scan p95 increases from 0.2ms to 500ms. What should you investigate?**

A) Network issues
B) Database size and query performance
C) Memory leaks
D) All of the above

<details>
<summary>✅ Correct Answer</summary>
**D) All of the above**

Performance degradation can have multiple causes. Check database size, memory usage, disk I/O, and system resources.
</details>

---

#### Question 26: Breaking Changes
**You want to update Agent X to v2.0.0. What should you check first?**

A) Agent health status
B) Breaking changes and dependent agents
C) Backup status
D) Superman approval

<details>
<summary>✅ Correct Answer</summary>
**B) Breaking changes and dependent agents**

Major version updates (2.0.0) may contain breaking changes. Check impact on dependent agents before updating.
</details>

---

#### Question 27: Learning System Not Working
**If no new insights are generated for 2 weeks, what could be the issue?**

A) Learning threshold too high
B) Not enough patterns detected
C) Learning system disabled
D) All of the above

<details>
<summary>✅ Correct Answer</summary>
**D) All of the above**

Check learning configuration, pattern thresholds, and system status. Lack of insights might be expected if no patterns exist.
</details>

---

#### Question 28: Rollback Failure
**If a rollback fails, what should you do?**

A) Try rolling back again
B) Restore from backup
C) Continue with current version
D) Panic

<details>
<summary>✅ Correct Answer</summary>
**B) Restore from backup**

Failed rollback is serious. Restore from last known good backup and investigate root cause.
</details>

---

#### Question 29: Multiple Agents Unhealthy
**If 3+ agents show unhealthy simultaneously, what is this likely?**

A) Individual agent issues
B) Oracle system issue or infrastructure problem
C) Coincidence
D) Normal operation

<details>
<summary>✅ Correct Answer</summary>
**B) Oracle system issue or infrastructure problem**

Multiple simultaneous issues suggest systemic problem (Oracle, database, disk, memory, network).
</details>

---

#### Question 30: After-Hours Issue
**You encounter a P1 issue at 2 AM. The runbook doesn't resolve it. What do you do?**

A) Wait until morning
B) Try experimental fixes
C) Escalate to on-call engineer per escalation path
D) Roll back to previous version without approval

<details>
<summary>✅ Correct Answer</summary>
**C) Escalate to on-call engineer per escalation path**

Follow escalation path: On-call engineer (0-15 min) → Backup on-call (15-30 min) → Manager (30-60 min). Never guess on P1 issues.
</details>

---

## Level 1 Scoring

### Scoring Guide
- **30/30 (100%)**: Excellent - Fully certified
- **27-29 (90-96%)**: Very Good - Certified with distinction
- **24-26 (80-86%)**: Good - Certified
- **20-23 (67-79%)**: Needs improvement - Review and retake
- **< 20 (<67%)**: Not certified - Complete training again

**Passing Score**: 24/30 (80%)

---

## Level 2: Senior Operator Certification

### Additional Requirements for Level 2
- Pass Level 1 with 85% or higher
- 3+ months experience as Level 1 operator
- Complete 2 supervised deployments
- Complete 5 supervised rollbacks
- Handle 10+ production incidents

### Additional Topics (15 questions)
- Deployment procedures and blue-green deployment
- Emergency rollback procedures
- Performance optimization
- Capacity planning
- Incident management
- Stakeholder communication

---

## Level 3: On-Call Engineer Certification

### Additional Requirements for Level 3
- Pass Level 2 with 85% or higher
- 6+ months experience as Level 2 operator
- Complete incident response training
- Shadow on-call engineer for 1 week
- Successfully handle 5+ P1 incidents
- Complete disaster recovery drill

### Additional Topics (15 questions)
- P0/P1 incident response
- Emergency procedures
- Disaster recovery
- Communication protocols
- Escalation procedures
- Post-incident reviews

---

## Certification Process

### Step 1: Training
1. Complete all required reading (7-11 hours)
2. Complete hands-on exercises (3-5 hours)
3. Shadow experienced operator (1-2 days)

### Step 2: Exam
1. Schedule 2-hour exam window
2. Take exam (open-book allowed)
3. Submit answers to training coordinator
4. Receive results within 24 hours

### Step 3: Certification
1. Pass exam with 80%+ score
2. Receive digital certificate
3. Added to certified operators list
4. Granted production access

### Step 4: Maintenance
1. Complete annual recertification exam (20 questions)
2. Complete 4 hours continuing education
3. Maintain active production experience

---

## Recertification

### Annual Recertification Requirements
- Complete 20-question recertification exam (80% passing)
- Review all documentation updates
- Complete any new training modules
- Maintain incident response skills

### Certification Expiration
- Certificates valid for 12 months
- 30-day grace period for recertification
- Expired certifications require full re-certification

---

## Training Resources

### Required Reading
1. `OPERATOR_TRAINING_MANUAL.md` (4-6 hours)
2. `OPERATIONAL_RUNBOOKS.md` (2-3 hours)
3. `TROUBLESHOOTING_GUIDE.md` (1-2 hours)

### Recommended Reading
1. `ORACLE_USER_GUIDE.md`
2. `ORACLE_BEST_PRACTICES.md`
3. `ORACLE_API_REFERENCE.md`

### Hands-On Exercises
1. Morning System Check (Exercise 1)
2. Investigating Issues (Exercise 2)
3. Applying Fixes (Exercise 3)
4. Managing Versions (Exercise 4)
5. Emergency Response (Exercise 5)

---

## Answer Key Summary

For certification coordinators - verify answers:

**Part 1 (Core Concepts)**: B, C, ACDE, C, B, C, B, C, B, B
**Part 2 (Operations)**: B, B, B, C, B, A, C, C, C, C
**Part 3 (Troubleshooting)**: B, B, B, C, D, B, D, B, B, C

---

## Certification Record

**Operator Name**: _________________________
**Date**: _________________________
**Score**: _______ / 30 (______%)
**Result**: ☐ PASS  ☐ FAIL
**Level Achieved**: ☐ Level 1  ☐ Level 2  ☐ Level 3
**Certificate ID**: _________________________
**Valid Until**: _________________________
**Coordinator Signature**: _________________________

---

**Oracle says**: "Knowledge is power. Certification ensures our operators protect the League effectively." 🎓
