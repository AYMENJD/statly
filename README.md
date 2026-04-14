<p align="center">
  <img src="./assets/demo.svg" width="800" alt="demo" />
  <br/><br/>
  <strong>statly</strong> is a lightweight tool for analyzing Git commit activity
  <br/><br/>

  <a href="https://pypi.org/project/statly">
    <img src="https://img.shields.io/pypi/v/statly?style=flat&logo=pypi" height="20" alt="PyPI version"/>
  </a>
  <a href="https://www.python.org">
    <img src="https://img.shields.io/pypi/pyversions/statly?style=flat&logo=python" height="20" alt="Python versions" />
  </a>
  <a href="https://pypi.org/project/statly">
    <img src="https://img.shields.io/pypi/dm/statly?style=flat&logo=pypi" height="20" alt="Downloads"/>
  </a>
</p>

### Installation

`statly` can be installed using `pip`:

```bash
pip install statly
```

### Usage

```bash
usage: statly [-h] [--git GIT] [--git-dir GIT_DIR] [--tz-mode {author,utc,local}] [--identity-mode {author,committer}]
              [-s SINCE] [-u UNTIL] [-a AUTHOR] [-j]

Statly — commit analytics for developers

options:
  -h, --help            show this help message and exit
  --git GIT             Path to git executable (default: use PATH or $STATLY_GIT)
  --git-dir GIT_DIR     Path to .git directory
  --tz-mode {author,utc,local}
                        Timezone mode (default: author)
  --identity-mode {author,committer}
                        Use author or committer identity (default: author)
  -s, --since SINCE     Start date (e.g. '2024-01-01')
  -u, --until UNTIL     End date
  -a, --author AUTHOR   Filter by author name/email
  -j, --json            Output results in JSON format

```

### Examples

```bash
# Analyze current repository
statly

# Filter by author
statly --author "john@example.com"

# Analyze a date range
statly --since 2024-01-01 --until 2024-12-31

# Use committer identity with UTC normalization
statly --identity-mode committer --tz-mode utc

# Output as JSON
statly --json

# Analyze another repository
statly --git-dir /path/to/repo/.git
```

### License

MIT [License](https://github.com/AYMENJD/statly/blob/main/LICENSE)
