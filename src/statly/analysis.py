from collections import Counter
from datetime import timedelta

from .utils import is_day


def calculate_streak(date_counter):
    if not date_counter:
        return (0, 0, None, None)

    dates = sorted(date_counter.keys())

    streak_len = 1
    streak_start = dates[0]
    streak_end = dates[0]
    streak_commits = date_counter[dates[0]]

    current_len = 1
    current_start = dates[0]
    current_commits = date_counter[dates[0]]

    for i in range(1, len(dates)):
        if dates[i] == dates[i - 1] + timedelta(days=1):
            current_len += 1
            current_commits += date_counter[dates[i]]
        else:
            if current_len > streak_len:
                streak_len = current_len
                streak_start = current_start
                streak_end = dates[i - 1]
                streak_commits = current_commits

            current_len = 1
            current_start = dates[i]
            current_commits = date_counter[dates[i]]

    if current_len > streak_len:
        streak_len = current_len
        streak_start = current_start
        streak_end = dates[-1]
        streak_commits = current_commits

    return (streak_len, streak_commits, streak_start, streak_end)


def analyze_stream(commits):
    day_count = 0
    night_count = 0
    total = 0

    last_dt = None

    weekday_counter = Counter()
    date_counter = Counter()
    hour_counter = Counter()

    for c in commits:
        dt = c["dt"]
        d = dt.date()

        if last_dt is None or dt > last_dt:
            last_dt = dt

        total += 1

        if is_day(dt):
            day_count += 1
        else:
            night_count += 1

        weekday_counter[dt.strftime("%A")] += 1
        date_counter[d] += 1
        hour_counter[dt.hour] += 1

    most_active_day = None

    if date_counter:
        most_active_day = max(date_counter.items(), key=lambda x: x[1])

    peak_hour = None
    if hour_counter:
        peak_hour = max(hour_counter.items(), key=lambda x: x[1])

    streak = calculate_streak(date_counter)

    return {
        "day": day_count,
        "night": night_count,
        "total": total,
        "weekday": weekday_counter,
        "most_active_day": most_active_day,
        "peak_hour": peak_hour,
        "streak": streak,
        "last_activity": last_dt,
    }
