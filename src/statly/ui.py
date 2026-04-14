from rich import box
from rich.console import Console
from rich.table import Table

from .utils import make_bar, percent

console = Console()


def print_json(stats):
    length, commits, start, end = stats["streak"]

    data = {
        "total": stats["total"],
        "day": stats["day"],
        "night": stats["night"],
        "weekday": {k.lower(): v for k, v in stats["weekday"].items()},
        "longest_streak": {
            "days": length,
            "commits": commits,
            "start": start.isoformat() if start else None,
            "end": end.isoformat() if end else None,
        },
    }

    if most_active_day := stats["most_active_day"]:
        data["most_active_day"] = {
            "date": most_active_day[0].isoformat(),
            "commits": most_active_day[1],
        }

    if peak_hour := stats["peak_hour"]:
        data["peak_hour"] = {
            "hour": peak_hour[0],
            "commits": peak_hour[1],
        }

    if last_activity := stats["last_activity"]:
        data["last_activity"] = last_activity.isoformat()

    console.print_json(data=data)


def print_report(stats, title):
    total = stats["total"]
    day_p = percent(stats["day"], total)
    night_p = percent(stats["night"], total)

    header_brand = "[bold cyan]Statly[/]"
    header_desc = "[dim]— commit analytics for developers[/]"

    console.print(f"{header_brand} {header_desc}")
    console.print()
    console.print(f"[bold]{title}[/]")

    line_width = len(title)
    console.print(f"[dim]{'─' * line_width}[/]")

    console.print(f"[bold]Total commits:[/] {total}\n")

    console.print(f"[yellow]Day Activity[/]   {stats['day']} commits ({day_p:>.1f}%)")
    console.print(make_bar(day_p, "yellow"))
    console.print()

    console.print(f"[blue]Night Activity[/] {stats['night']} commits ({night_p:>.1f}%)")
    console.print(make_bar(night_p, "blue"))
    console.print()

    highlights = Table(show_header=False, box=None, padding=(0, 2, 0, 0))
    highlights.add_column("Stat")
    highlights.add_column("Value")

    if most_active_day := stats["most_active_day"]:
        date, count = most_active_day
        readable = date.strftime("%A, %b %d, %Y")
        highlights.add_row(
            "[bold magenta]Most Active Day:[/]", f"{readable} — {count} commits"
        )

    if peak_hour := stats["peak_hour"]:
        hour, count = peak_hour
        highlights.add_row(
            "[bold cyan]Peak Hour:[/]", f"{hour:02d}:00 — {count} commits"
        )

    if last_activity := stats["last_activity"]:
        readable = last_activity.strftime("%A, %b %d, %Y at %H:%M")
        highlights.add_row(
            "[bold green]Last Activity:[/]",
            readable,
        )

    length, commits, start, end = stats["streak"]
    if start and end:
        highlights.add_row(
            "[bold yellow]Longest Streak:[/]",
            f"{length} days ({commits} commits, {start} → {end})",
        )

    if highlights.row_count > 0:
        console.print(highlights)
        console.print()

    wd_table = Table(
        title="Commits by Weekday",
        box=box.SIMPLE_HEAD,
        title_justify="left",
        title_style="bold green",
    )
    wd_table.add_column("Day", style="cyan")
    wd_table.add_column("Commits", justify="right", style="bold")
    wd_table.add_column("Activity", style="dim")

    max_wd = stats["weekday"].most_common(1)[0][1] if stats["weekday"] else 0

    for day, count in stats["weekday"].most_common():
        ratio = count / max_wd if max_wd else 0
        bar_len = int(15 * ratio)

        if ratio > 0.8:
            color = "bright_red"
        elif ratio > 0.5:
            color = "orange3"
        elif ratio > 0.2:
            color = "green"
        else:
            color = "bright_blue"

        bar = f"[{color}]" + ("■" * bar_len) + "[/]"
        wd_table.add_row(day, str(count), bar)

    console.print(wd_table)
