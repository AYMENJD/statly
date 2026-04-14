from datetime import datetime, timezone


def parse_git_datetime(s, tz_mode):
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"

    dt = datetime.fromisoformat(s)

    if tz_mode == "author":
        return dt
    elif tz_mode == "utc":
        return dt.astimezone(timezone.utc)
    elif tz_mode == "local":
        return dt.astimezone()
    return dt


def is_day(dt):
    return 6 <= dt.hour < 18


def percent(part, total):
    return (part / total * 100) if total else 0


def make_bar(p, color, width=30):
    filled = int(width * p / 100)
    return f"[{color}]{'█' * filled}[/][dim]{'░' * (width - filled)}[/]"
