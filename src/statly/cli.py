import argparse
import sys

from rich.console import Console

from .analysis import analyze_stream
from .git import get_git_log_stream, get_repo_name, is_git_repo
from .ui import print_json, print_report

console = Console()


def main():
    parser = argparse.ArgumentParser(
        description="Statly — commit analytics for developers",
    )

    parser.add_argument(
        "--git",
        help="Path to git executable (default: use PATH or $STATLY_GIT)",
    )
    parser.add_argument("--git-dir", help="Path to .git directory")
    parser.add_argument(
        "--tz-mode",
        choices=["author", "utc", "local"],
        default="author",
        help="Timezone mode (default: author)",
    )
    parser.add_argument(
        "--identity-mode",
        choices=["author", "committer"],
        default="author",
        help="Use author or committer identity (default: author)",
    )
    parser.add_argument("-s", "--since", help="Start date (e.g. '2024-01-01')")
    parser.add_argument("-u", "--until", help="End date")
    parser.add_argument("-a", "--author", help="Filter by author name/email")
    parser.add_argument(
        "-j", "--json", action="store_true", help="Output results in JSON format"
    )

    args = parser.parse_args()

    if not is_git_repo(args.git_dir):
        console.print("[bold red]Error:[/] Not a git repository.")
        sys.exit(1)

    repo_name = get_repo_name(args.git_dir)

    commits = get_git_log_stream(
        args.since,
        args.until,
        args.author,
        args.git_dir,
        args.tz_mode,
        args.identity_mode,
        args.json,
        args.git,
    )

    stats = analyze_stream(commits)

    if stats["total"] == 0:
        if not args.json:
            console.print("[bold yellow]No commits found.[/]")
        else:
            console.print_json(data={"error": "No commits found"})
        return

    title = args.author or repo_name
    if args.since and args.until:
        title += f" from {args.since} to {args.until}"
    elif args.since:
        title += f" since {args.since}"
    elif args.until:
        title += f" until {args.until}"

    if args.json:
        print_json(stats)
    else:
        print_report(stats, title)
