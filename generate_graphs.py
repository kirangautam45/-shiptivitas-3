#!/usr/bin/env python3
"""
Analytics script for Shiptivity - Kanban Feature Analysis
Generates graphs for daily active users and status changes
"""

import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

DB_PATH = '/Users/kiran/Developer/Developer_UK/-shiptivitas-3/shiptivity.db'
FEATURE_DATE = datetime(2018, 6, 2)
FEATURE_TIMESTAMP = 1527897600

def get_daily_active_users(conn):
    """Get daily active users data"""
    query = """
    SELECT
        date(login_timestamp, 'unixepoch') AS login_date,
        COUNT(DISTINCT user_id) AS daily_active_users,
        login_timestamp
    FROM login_history
    GROUP BY date(login_timestamp, 'unixepoch')
    ORDER BY login_date;
    """
    cursor = conn.execute(query)
    return cursor.fetchall()

def get_status_changes_by_card(conn):
    """Get status changes count per card"""
    query = """
    SELECT
        cardID,
        COUNT(*) AS total_status_changes
    FROM card_change_history
    WHERE oldStatus IS NOT NULL AND oldStatus != ''
    GROUP BY cardID
    ORDER BY total_status_changes DESC;
    """
    cursor = conn.execute(query)
    return cursor.fetchall()

def get_status_change_distribution(conn):
    """Get distribution of status change counts"""
    query = """
    SELECT
        total_status_changes,
        COUNT(*) AS number_of_cards
    FROM (
        SELECT
            cardID,
            COUNT(*) AS total_status_changes
        FROM card_change_history
        WHERE oldStatus IS NOT NULL AND oldStatus != ''
        GROUP BY cardID
    )
    GROUP BY total_status_changes
    ORDER BY total_status_changes;
    """
    cursor = conn.execute(query)
    return cursor.fetchall()

def plot_daily_active_users(data):
    """Create DAU graph with before/after feature comparison"""
    dates = [datetime.strptime(row[0], '%Y-%m-%d') for row in data]
    dau = [row[1] for row in data]

    # Separate before and after
    before_dates = [d for d, row in zip(dates, data) if row[2] < FEATURE_TIMESTAMP]
    before_dau = [row[1] for row in data if row[2] < FEATURE_TIMESTAMP]
    after_dates = [d for d, row in zip(dates, data) if row[2] >= FEATURE_TIMESTAMP]
    after_dau = [row[1] for row in data if row[2] >= FEATURE_TIMESTAMP]

    # Calculate averages
    avg_before = np.mean(before_dau) if before_dau else 0
    avg_after = np.mean(after_dau) if after_dau else 0

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

    # Time series plot
    ax1.plot(before_dates, before_dau, 'b-', alpha=0.7, linewidth=1, label='Before Kanban')
    ax1.plot(after_dates, after_dau, 'g-', alpha=0.7, linewidth=1, label='After Kanban')
    ax1.axvline(x=FEATURE_DATE, color='r', linestyle='--', linewidth=2, label='Kanban Release (Jun 2, 2018)')
    ax1.axhline(y=avg_before, color='b', linestyle=':', alpha=0.8, label=f'Avg Before: {avg_before:.1f}')
    ax1.axhline(y=avg_after, color='g', linestyle=':', alpha=0.8, label=f'Avg After: {avg_after:.1f}')

    ax1.set_xlabel('Date', fontsize=12)
    ax1.set_ylabel('Daily Active Users', fontsize=12)
    ax1.set_title('Daily Active Users Before and After Kanban Feature Release', fontsize=14, fontweight='bold')
    ax1.legend(loc='upper left')
    ax1.grid(True, alpha=0.3)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)

    # Bar chart comparison
    periods = ['Before Kanban\n(Feb-May 2018)', 'After Kanban\n(Jun 2018-Feb 2019)']
    avgs = [avg_before, avg_after]
    colors = ['#3498db', '#2ecc71']
    bars = ax2.bar(periods, avgs, color=colors, edgecolor='black', linewidth=1.2)

    # Add value labels on bars
    for bar, val in zip(bars, avgs):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                f'{val:.2f}', ha='center', va='bottom', fontsize=14, fontweight='bold')

    # Add percentage change
    pct_change = ((avg_after - avg_before) / avg_before) * 100
    ax2.annotate(f'+{pct_change:.0f}% increase',
                xy=(1, avg_after), xytext=(1.3, (avg_before + avg_after)/2),
                fontsize=12, color='green', fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='green'))

    ax2.set_ylabel('Average Daily Active Users', fontsize=12)
    ax2.set_title('Average DAU Comparison: Before vs After Kanban Feature', fontsize=14, fontweight='bold')
    ax2.set_ylim(0, max(avgs) * 1.3)
    ax2.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('/Users/kiran/Developer/Developer_UK/-shiptivitas-3/daily_active_users_graph.png', dpi=150, bbox_inches='tight')
    plt.close()

    print(f"Daily Active Users Graph saved!")
    print(f"  - Before Kanban: {avg_before:.2f} avg DAU ({len(before_dau)} days)")
    print(f"  - After Kanban: {avg_after:.2f} avg DAU ({len(after_dau)} days)")
    print(f"  - Increase: {pct_change:.1f}%")

def plot_status_changes_by_card(changes_data, distribution_data):
    """Create status changes graphs"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Histogram of status changes distribution
    change_counts = [row[0] for row in distribution_data]
    card_counts = [row[1] for row in distribution_data]

    colors = plt.cm.Blues(np.linspace(0.3, 0.9, len(change_counts)))
    bars = ax1.bar(change_counts, card_counts, color=colors, edgecolor='black', linewidth=0.5)

    ax1.set_xlabel('Number of Status Changes', fontsize=12)
    ax1.set_ylabel('Number of Cards', fontsize=12)
    ax1.set_title('Distribution: Status Changes per Card', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')

    # Add value labels
    for bar, count in zip(bars, card_counts):
        if count > 0:
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    str(count), ha='center', va='bottom', fontsize=9)

    # Top 20 cards by status changes
    top_20 = changes_data[:20]
    card_ids = [f'Card {row[0]}' for row in top_20]
    changes = [row[1] for row in top_20]

    colors2 = plt.cm.Oranges(np.linspace(0.3, 0.9, len(changes)))
    bars2 = ax2.barh(card_ids[::-1], changes[::-1], color=colors2[::-1], edgecolor='black', linewidth=0.5)

    ax2.set_xlabel('Number of Status Changes', fontsize=12)
    ax2.set_ylabel('Card ID', fontsize=12)
    ax2.set_title('Top 20 Cards by Status Changes', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='x')

    plt.tight_layout()
    plt.savefig('/Users/kiran/Developer/Developer_UK/-shiptivitas-3/status_changes_by_card_graph.png', dpi=150, bbox_inches='tight')
    plt.close()

    print(f"\nStatus Changes Graph saved!")
    print(f"  - Total cards with status changes: {len(changes_data)}")
    print(f"  - Most active card: Card {changes_data[0][0]} ({changes_data[0][1]} changes)")
    print(f"  - Average changes per card: {np.mean([row[1] for row in changes_data]):.2f}")

def main():
    conn = sqlite3.connect(DB_PATH)

    print("=" * 60)
    print("SHIPTIVITY ANALYTICS - KANBAN FEATURE ANALYSIS")
    print("=" * 60)

    # Generate DAU graph
    print("\n[1] Generating Daily Active Users Graph...")
    dau_data = get_daily_active_users(conn)
    plot_daily_active_users(dau_data)

    # Generate status changes graph
    print("\n[2] Generating Status Changes Graph...")
    changes_data = get_status_changes_by_card(conn)
    distribution_data = get_status_change_distribution(conn)
    plot_status_changes_by_card(changes_data, distribution_data)

    conn.close()

    print("\n" + "=" * 60)
    print("GRAPHS GENERATED SUCCESSFULLY!")
    print("=" * 60)
    print("\nFiles created:")
    print("  - daily_active_users_graph.png")
    print("  - status_changes_by_card_graph.png")

if __name__ == "__main__":
    main()
