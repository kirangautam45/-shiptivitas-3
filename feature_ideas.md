# Shiptivity Feature Ideas - Increasing Daily Active Users

## Analysis Summary

The Kanban Board release on June 2, 2018 resulted in a **225% increase** in daily active users:
- **Before Kanban**: 3.63 avg DAU (Feb-May 2018)
- **After Kanban**: 11.79 avg DAU (Jun 2018-Feb 2019)

**Key Insights from Data:**
- The Kanban feature significantly boosted engagement
- Most cards (100 out of 162) only have 2 status changes (created -> moved once)
- Low "rework" rate (cards rarely move backwards from complete/in-progress)
- Opportunity to increase engagement depth per user

---

## Feature Idea 1: Daily Digest & Progress Notifications

### Hypothesis
Users who receive daily summary notifications about their card progress and team activity will return to the app more frequently, increasing DAU by creating a habit loop.

### Expected Impact
- **+15-25% increase in DAU** through notification-driven returns
- Higher 7-day retention rate
- Increased status change activity as users act on notifications

### Feature Description
A daily email/push notification system that sends users:
- Summary of cards they moved yesterday
- Cards approaching deadlines or stuck in "backlog" too long
- Team activity highlights (who completed what)
- A personalized "quick win" suggestion (e.g., "You have 3 cards ready to move to in-progress")

### Wireframe
```
+------------------------------------------+
|  DAILY DIGEST - Jan 15, 2019             |
+------------------------------------------+
|                                          |
|  YOUR PROGRESS YESTERDAY                 |
|  [====] 2 cards moved to complete        |
|  [====] 1 card started                   |
|                                          |
|  NEEDS ATTENTION                         |
|  ! "API Integration" - 7 days in backlog |
|  ! "Bug Fix #42" - no updates in 5 days  |
|                                          |
|  TEAM HIGHLIGHTS                         |
|  Sarah completed "User Auth"             |
|  Mike started 3 new cards                |
|                                          |
|  [Open Shiptivity] [Snooze for today]    |
+------------------------------------------+
```

---

## Feature Idea 2: Streak & Achievement System

### Hypothesis
Gamification elements like daily streaks and achievements will incentivize users to return daily to maintain their progress, directly increasing DAU.

### Expected Impact
- **+20-30% increase in DAU** through gamification engagement
- Users visit even when they have no immediate task to preserve streak
- Viral sharing of achievements brings new users

### Feature Description
A streak and achievement system that rewards daily activity:
- **Daily Streak Counter**: Track consecutive days with at least one card status change
- **Achievements**: "First Complete", "10 Cards Done", "7-Day Streak", "Team Player" (helped on 5 cards)
- **Leaderboard**: Weekly team leaderboard showing most active contributors
- **Milestone Badges**: Visual badges displayed on profile

### Wireframe
```
+------------------------------------------+
|  YOUR PROGRESS                           |
+------------------------------------------+
|                                          |
|  CURRENT STREAK: 12 DAYS [flame icon]    |
|  Keep going! 2 more days for "2 Week"    |
|  badge                                   |
|                                          |
|  +--------+  +--------+  +--------+      |
|  | FIRST  |  | STREAK |  | 10     |      |
|  | DONE   |  | 7 DAYS |  | CARDS  |      |
|  +--------+  +--------+  +--------+      |
|                                          |
|  TEAM LEADERBOARD (This Week)            |
|  1. Sarah    - 15 completions            |
|  2. You      - 12 completions            |
|  3. Mike     - 8 completions             |
|                                          |
+------------------------------------------+
```

---

## Feature Idea 3: Quick Card Actions from Dashboard

### Hypothesis
Reducing friction for common actions (moving cards between statuses) directly from the dashboard will increase engagement and daily visits, as users can make progress with minimal effort.

### Expected Impact
- **+10-15% increase in DAU** through reduced friction
- Higher number of status changes per session
- Lower bounce rate from dashboard

### Feature Description
A streamlined dashboard that shows actionable cards with one-click status transitions:
- **"Ready to Move" widget**: Cards that likely need status updates
- **Quick action buttons**: Move card to next logical status with one click
- **Smart suggestions**: AI-powered suggestions like "This card has been in-progress for 5 days, move to complete?"
- **Keyboard shortcuts**: Power users can navigate and update cards without mouse

### Wireframe
```
+------------------------------------------+
|  DASHBOARD                               |
+------------------------------------------+
|                                          |
|  QUICK ACTIONS (3 cards ready)           |
|                                          |
|  +--------------------------------------+|
|  | API Integration        [In Progress] ||
|  | in backlog for 5 days  [-> Start]    ||
|  +--------------------------------------+|
|                                          |
|  +--------------------------------------+|
|  | User Authentication    [Complete]    ||
|  | in progress 3 days     [-> Done]     ||
|  +--------------------------------------+|
|                                          |
|  +--------------------------------------+|
|  | Bug Fix #42            [In Progress] ||
|  | Last updated: 7 days   [-> Done]     ||
|  |                        [-> Backlog]  ||
|  +--------------------------------------+|
|                                          |
|  [View Full Kanban Board]                |
+------------------------------------------+
```

---

## Prioritization Recommendation

| Feature | Expected DAU Impact | Dev Effort | Priority |
|---------|---------------------|------------|----------|
| Daily Digest | +15-25% | Medium | 1 |
| Streak System | +20-30% | Medium-High | 2 |
| Quick Actions | +10-15% | Low | 3 |

**Recommendation**: Start with **Daily Digest** as it leverages external triggers to bring users back, then layer **Streak System** for retention, and finally **Quick Actions** for engagement depth.

---

## Files Delivered

1. `answer.sql` - SQL queries for DAU and status change analysis
2. `daily_active_users_graph.png` - DAU visualization before/after feature
3. `status_changes_by_card_graph.png` - Status change distribution
4. `generate_graphs.py` - Python script to regenerate graphs
5. `feature_ideas.md` - This document with three actionable feature ideas
