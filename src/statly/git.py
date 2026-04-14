import os
import subprocess
import sys
from contextlib import nullcontext

from rich.console import Console

from .utils import parse_git_datetime

console = Console()


def build_git_cmd(base_args, git_dir=None, git_bin=None):
    git = git_bin or os.getenv("STATLY_GIT") or "git"

    cmd = [git, "--no-pager"]
    if git_dir:
        cmd.extend(["--git-dir", git_dir])
    cmd.extend(base_args)
    return cmd


def is_git_repo(git_dir=None):
    cmd = build_git_cmd(["rev-parse", "--is-inside-work-tree"], git_dir)
    try:
        res = subprocess.run(cmd, capture_output=True, text=True)
        return res.returncode == 0
    except FileNotFoundError:
        return False


def get_repo_name(git_dir=None):
    try:
        cmd = build_git_cmd(["rev-parse", "--show-toplevel"], git_dir)
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return os.path.basename(res.stdout.strip())
    except subprocess.CalledProcessError:
        if git_dir:
            return os.path.basename(os.path.abspath(git_dir))
        return "Unknown"


def get_git_log_stream(
    since=None,
    until=None,
    author=None,
    git_dir=None,
    tz_mode="author",
    identity_mode="author",
    quiet=False,
    git_bin=None,
):
    cmd = build_git_cmd(
        [
            "log",
            "--pretty=format:%aI|%cI|%aE|%cE",
            "--no-decorate",
            "--no-color",
        ],
        git_dir,
        git_bin,
    )

    if since:
        cmd.append(f"--since={since}")
    if until:
        cmd.append(f"--until={until}")
    if author:
        cmd.append(f"--author={author}")

    ctx = nullcontext() if quiet else console.status("Analyzing commits...")
    with ctx:
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)

            for line in process.stdout:
                line = line.strip()
                if not line:
                    continue

                parts = line.split("|")
                if len(parts) != 4:
                    continue

                a_dt = parse_git_datetime(parts[0], tz_mode)
                c_dt = parse_git_datetime(parts[1], tz_mode)

                a_email = parts[2].lower()
                c_email = parts[3].lower()

                if identity_mode == "author":
                    yield {"dt": a_dt, "author": a_email}
                else:
                    yield {"dt": c_dt, "author": c_email}

            process.wait()

        except FileNotFoundError:
            console.print("[bold red]Error: Git is not installed or not in PATH.[/]")
            sys.exit(1)
