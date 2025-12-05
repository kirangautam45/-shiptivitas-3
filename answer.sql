-- TYPE YOUR SQL QUERY BELOW

-- PART 1: Create a SQL query that maps out the daily average users before and after the feature change
-- Feature release date: 2018-06-02 (Unix timestamp: 1527897600)

-- Daily Active Users (DAU) with before/after feature classification
SELECT
    date(login_timestamp, 'unixepoch') AS login_date,
    
    COUNT(DISTINCT user_id) AS daily_active_users,
    CASE
        WHEN login_timestamp < 1527897600 THEN 'Before Kanban'
        ELSE 'After Kanban'
    END AS feature_period
FROM login_history
GROUP BY date(login_timestamp, 'unixepoch')
ORDER BY login_date;

-- Average DAU before and after feature release
SELECT
    CASE
        WHEN login_timestamp < 1527897600 THEN 'Before Kanban (Feb-May 2018)'
        ELSE 'After Kanban (Jun 2018 - Feb 2019)'
    END AS period,
    ROUND(AVG(daily_users), 2) AS avg_daily_active_users,
    COUNT(*) AS total_days,
    SUM(daily_users) AS total_logins
FROM (
    SELECT
        date(login_timestamp, 'unixepoch') AS login_date,
        COUNT(DISTINCT user_id) AS daily_users,
        login_timestamp
    FROM login_history
    GROUP BY date(login_timestamp, 'unixepoch')
) daily_stats
GROUP BY CASE
    WHEN login_timestamp < 1527897600 THEN 'Before Kanban (Feb-May 2018)'
    ELSE 'After Kanban (Jun 2018 - Feb 2019)'
END;


-- PART 2: Create a SQL query that indicates the number of status changes by card

-- Status changes by card (excluding initial creation where oldStatus is NULL)
SELECT
    cardID,
    c.name AS card_name,
    COUNT(*) AS total_status_changes,
    SUM(CASE WHEN oldStatus IS NULL OR oldStatus = '' THEN 1 ELSE 0 END) AS card_creations,
    SUM(CASE WHEN oldStatus = 'backlog' AND newStatus = 'in-progress' THEN 1 ELSE 0 END) AS backlog_to_progress,
    SUM(CASE WHEN oldStatus = 'in-progress' AND newStatus = 'complete' THEN 1 ELSE 0 END) AS progress_to_complete,
    SUM(CASE WHEN oldStatus = 'in-progress' AND newStatus = 'backlog' THEN 1 ELSE 0 END) AS progress_to_backlog,
    SUM(CASE WHEN oldStatus = 'complete' AND newStatus = 'in-progress' THEN 1 ELSE 0 END) AS complete_to_progress
FROM card_change_history cch
LEFT JOIN card c ON cch.cardID = c.id
GROUP BY cardID
ORDER BY total_status_changes DESC;

-- Distribution of status change counts
SELECT
    total_status_changes,
    COUNT(*) AS number_of_cards
FROM (
    SELECT
        cardID,
        COUNT(*) AS total_status_changes
    FROM card_change_history
    GROUP BY cardID
)
GROUP BY total_status_changes
ORDER BY total_status_changes;

-- Most common status transitions
SELECT
    COALESCE(oldStatus, 'NEW') AS from_status,
    newStatus AS to_status,
    COUNT(*) AS transition_count
FROM card_change_history
GROUP BY oldStatus, newStatus
ORDER BY transition_count DESC;
