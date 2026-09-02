# Sample Meeting Notes for Meeting-Notes-to-Actions Agent

## Example 1: Daily Standup Meeting

**Meeting Title:** Daily Standup - September 2, 2026  
**Date:** Tuesday, September 2, 2026  
**Time:** 9:00 AM - 9:30 AM  
**Location:** Conference Room B / Teams Virtual  
**Attendees:** Sarah Chen (Tech Lead), Mike Rodriguez (Ops Manager), John Smith (Senior Engineer), Lisa Wang (Operations Specialist), David Kim (DBA)

---

### Topics Discussed

#### 1. 🚨 CRITICAL - Production Database Issue (P1)

**Reported by:** Sarah Chen

**Issue Description:**
- Database connection pool exhaustion affecting payment processing
- Started approximately 8:00 AM this morning
- Current impact: ~2% of transactions failing
- Affects: Production environment only
- Ticket: #DB-12345

**Details:**
- Connection pool size: 100 connections
- Current usage: 127 (OVER LIMIT)
- Average query time: 2.3s (normal is <500ms)
- Root cause: Still investigating
- Possible causes: Slow query, connection leak, or external API timeout

**Decisions Made:**
1. ✅ Technical team to prioritize this investigation immediately
2. ✅ DBA (David) to check logs and query performance
3. ✅ Escalate to VP Engineering if not resolved within 4 hours (by 1:00 PM)
4. ✅ Operations to prepare customer notification if issue persists past 2 PM

**Action Items:**

| # | Task | Owner | Due Date | Priority | Dependencies |
|---|------|-------|----------|----------|--------------|
| AI-001 | Diagnose database connection pool issue #DB-12345 | John Smith | TODAY, 1:00 PM | P1 | None |
| AI-002 | Check database logs for connection errors | David Kim | TODAY, 12:00 PM | P1 | None |
| AI-003 | Identify and kill long-running queries | David Kim | TODAY, 12:30 PM | P1 | Depends on AI-002 |
| AI-004 | Prepare customer notification template | Mike Rodriguez | TODAY, 2:00 PM | P1 | Depends on AI-001 |
| AI-005 | Review and optimize connection pool settings | John Smith | TODAY, 3:00 PM | P1 | Depends on AI-001 |
| AI-006 | Deploy fix to production if identified | John Smith | TODAY, 4:00 PM | P1 | Depends on AI-005 |

---

#### 2. 📊 Authentication Service Degradation (P2)

**Reported by:** Mike Rodriguez

**Issue Description:**
- Login timeouts reported by 5 customers this morning
- Started around 7:30 AM
- Affects: Web application login page
- Ticket: #AUTH-6789

**Details:**
- Impact: ~0.5% of active users
- Current status: Intermittent (not consistent)
- Error message: "Login request timeout (>30s)"
- Environment: Production

**Decisions Made:**
1. ✅ Monitor service continuously - don't need immediate action yet
2. ✅ Investigate root cause (latency or resource issue)
3. ✅ No immediate escalation required

**Action Items:**

| # | Task | Owner | Due Date | Priority | Dependencies |
|---|------|-------|----------|----------|--------------|
| AI-007 | Investigate AUTH-6789 login timeout root cause | John Smith | TOMORROW, 5:00 PM | P2 | None |
| AI-008 | Check API response times and latency metrics | Sarah Chen | TODAY, 4:00 PM | P2 | None |
| AI-009 | Send status update email to affected customers | Lisa Wang | TODAY, 4:00 PM | P2 | Depends on AI-008 |

---

#### 3. 📋 Weekly Status Reporting

**Discussed by:** Mike Rodriguez

**Topic:** Need to compile weekly report on all P1 and P2 ticket status for leadership.

**Details:**
- Report due: Friday, September 6, 5:00 PM
- Distribution: VP Engineering, Director of Operations, Executive Leadership
- Content needed:
  - Summary of all P1 tickets this week (status, resolution if applicable)
  - Summary of all P2 tickets this week
  - Any SLA violations
  - Escalations summary
  - Key metrics and trends

**Decisions Made:**
1. ✅ Mike to compile report by Friday EOD
2. ✅ Lisa to send to leadership
3. ✅ Include escalation procedures and preventive measures

**Action Items:**

| # | Task | Owner | Due Date | Priority | Dependencies |
|---|------|-------|----------|----------|--------------|
| AI-010 | Create weekly P1/P2 ticket status report | Mike Rodriguez | FRIDAY, 5:00 PM | High | Depends on all tickets being updated |
| AI-011 | Send weekly report to leadership | Lisa Wang | FRIDAY, 6:00 PM | High | Depends on AI-010 |

---

### Key Decisions Summary

| Decision | Owner | Impact |
|----------|-------|--------|
| Prioritize DB issue immediately | Technical | Production availability |
| Escalate if not resolved by 1 PM | Technical | SLA compliance |
| Prepare customer notification | Operations | Communication readiness |
| Weekly reporting deadline Friday | Operations | Stakeholder visibility |

---

### Follow-up Actions

- ⏰ Reconvene at 12:00 PM if DB issue continues
- 📧 Send daily update to management on P1 status
- 📞 Call VP Engineering if escalation needed

---

### Next Meeting

**Daily Standup** - September 3, 2026 at 9:00 AM

---

## Example 2: Weekly Ticket Review Meeting

**Meeting Title:** Weekly Ticket Review - August 28, 2026  
**Date:** Wednesday, August 28, 2026  
**Time:** 2:00 PM - 3:30 PM  
**Location:** Teams Virtual  
**Attendees:** Sarah Chen (Tech Lead), Mike Rodriguez (Ops Manager), David Kim (DBA), Jessica Brown (VP Engineering), Lisa Wang (Operations Specialist)

---

### Overview

Weekly review of all P1 and P2 tickets from the past week. Focus on SLA compliance and escalations.

---

### P1 Tickets Summary

#### Ticket #DB-11111 - Database Replication Lag (⚠️ ESCALATION REQUIRED)

**Status:** ❌ BEYOND 48-HOUR SLA  
**Time Open:** 52 hours (opened Aug 26, 10:00 AM)  
**Priority:** P1 (Critical)

**Details:**
- Issue: Reporting database shows stale data (30+ minutes behind)
- Impact: Executive reports showing outdated information
- Owner: David Kim (DBA)
- Current Status: Still troubleshooting connection parameters

**SLA Status:** 🚨 VIOLATED - Past 48-hour mark by 4 hours

**Decisions Made:**
1. ✅ ESCALATE to VP Engineering immediately (Jessica present)
2. ✅ Operations to send formal escalation email to executives
3. ✅ Daily updates required until resolved
4. ✅ Post-mortem meeting scheduled for Sept 5

**Action Items:**

| # | Task | Owner | Due Date | Priority | Dependencies |
|---|------|-------|----------|----------|--------------|
| AI-012 | Escalate #DB-11111 to VP Engineering | David Kim | TODAY, 3:00 PM | P1 | None |
| AI-013 | Send escalation notification email to VP Engineering | Lisa Wang | TODAY, 3:30 PM | P1 | Depends on AI-012 |
| AI-014 | Notify executive stakeholders of SLA violation | Mike Rodriguez | TODAY, 4:00 PM | P1 | Depends on AI-013 |
| AI-015 | Implement replication lag monitoring alert | David Kim | TOMORROW | P1 | Depends on resolution |
| AI-016 | Schedule post-mortem meeting | Sarah Chen | THURSDAY | P1 | None |

---

#### Ticket #API-22222 - API Rate Limiting Issue (⚠️ CRITICAL - APPROACHING SLA)

**Status:** 🟡 CRITICAL - APPROACHING SLA  
**Time Open:** 45 hours (opened Aug 27, 11:00 AM)  
**Priority:** P1 (Critical)  
**Time Remaining:** 3 hours to SLA

**Details:**
- Issue: Mobile app users experiencing HTTP 429 (Too Many Requests)
- Impact: Mobile users cannot use app features
- Root Cause: Rate limiter threshold misconfigured
- Current Status: Fix deployed to staging, testing in progress
- Owner: John Smith

**SLA Status:** ⚠️ CRITICAL - 3 HOURS REMAINING (48h mark is Aug 28, 11:00 AM)

**Decisions Made:**
1. ✅ Complete testing immediately - high priority
2. ✅ Deploy to production if tests pass (should be by 10:00 AM tomorrow)
3. ✅ If deployment blocked, escalate to senior engineering
4. ✅ Operations to prepare production deployment communication

**Action Items:**

| # | Task | Owner | Due Date | Priority | Dependencies |
|---|------|-------|----------|----------|--------------|
| AI-017 | Complete testing of API rate limit fix | John Smith | TODAY, 5:00 PM | P1 | None |
| AI-018 | Deploy API fix to production | John Smith | TOMORROW, 10:00 AM | P1 | Depends on AI-017 |
| AI-019 | Notify customers of API rate limit restoration | Lisa Wang | TOMORROW, 11:00 AM | P1 | Depends on AI-018 |
| AI-020 | Configure monitoring and alerts for rate limiter | Sarah Chen | TOMORROW, 3:00 PM | P1 | Depends on AI-018 |

---

### P2 Tickets Summary

#### Ticket #UI-33333 - Dashboard Performance (✅ WITHIN SLA)

**Status:** ✅ On track  
**Time Open:** 36 hours (opened Aug 27, 2:00 PM)  
**Priority:** P2  
**SLA:** 5 business days (resolve by Sep 3)

**Details:**
- Issue: Dashboard loads slowly for large datasets (>10k records)
- Impact: Affects users filtering large date ranges
- Root Cause: N+1 query problem in dashboard rendering
- Owner: Sarah Chen

**Current Progress:**
- Analysis phase complete
- Performance profiling done
- Fix identified and ready for development

**Decisions Made:**
1. ✅ Continue normal investigation pace
2. ✅ No escalation needed - well within SLA
3. ✅ Include in code review process

**Action Items:**

| # | Task | Owner | Due Date | Priority | Dependencies |
|---|------|-------|----------|----------|--------------|
| AI-021 | Implement dashboard query optimization | Sarah Chen | THURSDAY, 5:00 PM | P2 | None |
| AI-022 | Test performance improvements on staging | Sarah Chen | FRIDAY, 10:00 AM | P2 | Depends on AI-021 |
| AI-023 | Deploy dashboard fix to production | John Smith | FRIDAY, 3:00 PM | P2 | Depends on AI-022 |

---

### Weekly Reports

**Action Items:**

| # | Task | Owner | Due Date | Priority | Dependencies |
|---|------|-------|----------|----------|--------------|
| AI-024 | Compile weekly P1/P2 ticket status report | Mike Rodriguez | FRIDAY, 5:00 PM | High | None |
| AI-025 | Include escalation timeline in report | Mike Rodriguez | FRIDAY, 5:00 PM | High | Depends on AI-024 |
| AI-026 | Send weekly report to executive stakeholders | Lisa Wang | FRIDAY, 6:00 PM | High | Depends on AI-024 |

---

### Key Metrics

| Metric | Week of Aug 26 | Previous Week | Trend |
|--------|---|---|---|
| P1 Tickets | 2 | 1 | ⬆️ +1 |
| P2 Tickets | 1 | 2 | ⬇️ -1 |
| SLA Violations | 1 | 0 | ⬆️ +1 |
| Avg Resolution Time (P1) | 42h | 36h | ⬆️ 6h slower |
| Escalations | 1 | 0 | ⬆️ +1 |

---

### Discussion Points

1. **SLA Violation Discussion**
   - #DB-11111 took too long due to insufficient monitoring
   - Need to add proactive alerts for replication lag
   - Plan: Implement automated alerts by end of week

2. **API Rate Limiting Issue**
   - Configuration was done incorrectly during last deployment
   - Need to add validation tests for rate limiter configs
   - Plan: Add configuration tests to CI/CD pipeline

3. **Process Improvement**
   - Consider implementing automated escalation notifications
   - Update runbook for P1 ticket procedures
   - Schedule training on SLA procedures

---

### Decisions Summary

| Decision | Owner | Deadline |
|----------|-------|----------|
| Escalate DB issue to VP Engineering | David Kim | TODAY |
| Complete API testing and deploy | John Smith | TOMORROW 10 AM |
| Finalize escalation procedures | Sarah Chen | THURSDAY |
| Submit weekly report | Mike Rodriguez | FRIDAY 5 PM |

---

### Follow-up Actions

- ✅ Formal escalation for #DB-11111
- 📧 Daily status updates on P1 tickets
- 📊 Weekly report ready for executive review
- 🔄 Process improvement items added to backlog

---

### Next Meeting

**Weekly Ticket Review** - September 4, 2026 at 2:00 PM

---

## Example 3: Incident Response Meeting

**Meeting Title:** P1 Incident Response - Database Exhaustion  
**Date:** September 2, 2026  
**Time:** 12:30 PM - 1:15 PM (Emergency Call)  
**Attendees:** Sarah Chen (Tech Lead), John Smith (Engineer), David Kim (DBA), Mike Rodriguez (Ops Manager), Lisa Wang (Operations Specialist)

---

### Incident Summary

Production database connection pool exhaustion. Started 8:00 AM, still ongoing. Payment processing at 2% failure rate.

**Incident ID:** INC-2026-0902-001  
**Priority:** P1 - CRITICAL  
**Status:** IN PROGRESS  
**Time Since Open:** 4.5 hours

---

### Current Status

**Investigation Results (12:30 PM):**
- ✅ Found root cause: Payment API slow (50+ second timeout)
- ✅ Payment API calling external service that's overloaded
- ✅ Connections not being released due to timeout
- ✅ Pool size exhausted in ~6 hours

**Impact:**
- 2% of transactions currently failing
- Estimated revenue impact: $15,000/hour
- Customer complaints increasing

---

### Resolution Plan

**Immediate Actions (Next 15 minutes):**
1. Add connection pool timeout (kill stuck connections after 30s)
2. Disable payment API retry logic temporarily
3. Route traffic to backup payment provider

**Short-term Actions (Next 2 hours):**
1. Increase connection pool size to 150
2. Enable circuit breaker on payment API
3. Monitor closely

**Root Cause Fix (Next 24 hours):**
1. Investigate external payment service
2. Optimize payment API timeout handling
3. Add comprehensive monitoring

---

### Action Items (Emergency)

| # | Task | Owner | Due | Priority |
|---|------|-------|-----|----------|
| AI-027 | Deploy connection timeout fix to production | John Smith | 12:45 PM | P1 |
| AI-028 | Route to backup payment provider | John Smith | 12:50 PM | P1 |
| AI-029 | Monitor connection pool and transaction rates | David Kim | CONTINUOUS | P1 |
| AI-030 | Update customer status page | Lisa Wang | 1:00 PM | P1 |
| AI-031 | Prepare customer notification if needed | Mike Rodriguez | 1:00 PM | P1 |
| AI-032 | Investigate external payment API issue | Sarah Chen | TODAY, 3:00 PM | P1 |
| AI-033 | Implement payment API circuit breaker | John Smith | TOMORROW, 2:00 PM | P1 |

---

### Communication Plan

| Who | What | When |
|-----|------|------|
| Lisa Wang | Update customer status page | Immediate |
| Mike Rodriguez | Notify top 10 affected customers | 1:00 PM |
| Executive Team | Incident notification | 1:15 PM |
| Customers | "Resolved" update | After deployment |

---

### Reconvene Schedule

- Next status: 1:30 PM (30 minutes)
- Follow-up call: 3:00 PM if ongoing
- Post-incident review: Tomorrow 10:00 AM

---

## How to Use These Examples

1. **Copy** the meeting notes into a text file
2. **Run** through the Meeting-Notes-to-Actions Agent
3. **Verify** that:
   - ✅ All action items are extracted
   - ✅ Owners are assigned correctly
   - ✅ Due dates are parsed
   - ✅ Teams are assigned (Technical vs Operations)
   - ✅ Dependencies are identified
   - ✅ P1/P2 priorities are categorized
   - ✅ SLA information is captured

4. **Expected Output** should include:
   - 11 items from Example 1 (Standup)
   - 16 items from Example 2 (Weekly Review)
   - 7 items from Example 3 (Incident Response)

---

## Key Patterns Demonstrated

### Example 1: Daily Standup
- Simple, actionable items
- Mix of Technical and Operations tasks
- Clear dependencies between items
- SLA escalation scenarios

### Example 2: Weekly Review
- Past-due P1 ticket (escalation required)
- Critical P1 approaching SLA threshold
- P2 within SLA
- Metrics and trend analysis
- Report generation tasks

### Example 3: Incident Response
- Time-critical incident
- Immediate vs. short-term vs. long-term actions
- Communication and escalation
- Backup plans

---

## Notes for Agent Implementation

- Dates can be explicit (e.g., "FRIDAY, 5:00 PM") or relative (e.g., "TODAY", "TOMORROW")
- Priorities are marked with emojis (🚨 for P1, ⚠️ for critical), keywords (P1, P2), or context
- Owners are person names and should be extracted exactly as written
- Dependencies can be stated as "Depends on", "Blocks", or "Requires"
- Team assignment should be automatic based on task description
- Tables are optional but help with readability
