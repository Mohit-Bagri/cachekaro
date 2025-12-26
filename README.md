# CacheKaro

<div align="center">

```
   ____           _          _  __
  / ___|__ _  ___| |__   ___| |/ /__ _ _ __ ___
 | |   / _` |/ __| '_ \ / _ \ ' // _` | '__/ _ \
 | |__| (_| | (__| | | |  __/ . \ (_| | | | (_) |
  \____\__,_|\___|_| |_|\___|_|\_\__,_|_|  \___/
```

**Cross-Platform Storage & Cache Manager**

*Cache Karo!* (Hindi-English: "Clean it up!")

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)](#platform-support)

</div>

---

## Overview

**CacheKaro** is a production-ready, cross-platform tool to analyze and clean cache/storage on **macOS**, **Linux**, and **Windows**. It provides comprehensive insights into what's consuming your disk space and safely cleans caches to free up storage.

### Key Features

- **Cross-Platform**: Works on macOS, Linux, and Windows
- **Comprehensive Analysis**: Scans 50+ cache locations across browsers, dev tools, apps
- **Rich Metadata**: File age, types, stale detection, largest files
- **Multiple Export Formats**: Text, JSON, CSV, HTML with interactive charts
- **Safe Cleaning**: Multiple modes (interactive, auto, dry-run) with risk levels
- **Beautiful CLI**: Colored output, progress bars, formatted reports

---

## Installation

### From PyPI (Recommended)

```bash
pip install cachekaro
```

### From Source

```bash
git clone https://github.com/mohitbagri/cachekaro.git
cd cachekaro
pip install -e .
```

### Requirements

- Python 3.9 or higher
- No external dependencies required for basic usage

---

## Quick Start

### Analyze Storage

```bash
# Basic analysis
cachekaro analyze

# Output as JSON
cachekaro analyze --format json

# Save HTML report
cachekaro analyze --format html --output report.html

# Only development caches
cachekaro analyze --category development
```

### Clean Caches

```bash
# Interactive cleaning (confirm each item)
cachekaro clean

# Preview what would be cleaned
cachekaro clean --dry-run

# Clean all safe items without prompts
cachekaro clean --auto

# Clean only stale caches (not accessed in 30+ days)
cachekaro clean --stale-only
```

### Generate Reports

```bash
# Generate HTML report with charts
cachekaro report

# Generate CSV for spreadsheet analysis
cachekaro report --format csv
```

---

## Commands

| Command | Description |
|---------|-------------|
| `cachekaro analyze` | Analyze storage and cache usage |
| `cachekaro clean` | Clean cache and temporary files |
| `cachekaro report` | Generate detailed reports |
| `cachekaro info` | Show system information |

### Analyze Options

| Option | Description |
|--------|-------------|
| `-f, --format` | Output format: `text`, `json`, `csv`, `html` |
| `-o, --output` | Save output to file |
| `-c, --category` | Filter by category |
| `--min-size` | Minimum size to show (e.g., `100MB`) |
| `--stale-days` | Days for stale detection (default: 30) |
| `--safe-only` | Only show safe-to-clean items |
| `--no-color` | Disable colored output |

### Clean Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Preview without deleting |
| `--auto` | Clean all without prompts |
| `--risk` | Max risk level: `safe`, `moderate`, `caution` |
| `--stale-only` | Only clean stale items |
| `--backup` | Create backup before deleting |

---

## Categories

CacheKaro scans these cache categories:

| Category | Description | Examples |
|----------|-------------|----------|
| `user_cache` | User application caches | `~/Library/Caches`, `~/.cache` |
| `browser` | Browser caches | Chrome, Firefox, Safari, Edge |
| `development` | Dev tool caches | npm, pip, Gradle, Maven, Docker |
| `logs` | Log files | System logs, app logs |
| `trash` | Deleted files | Trash/Recycle Bin |
| `downloads` | Downloaded files | Downloads folder |
| `application` | App-specific caches | Spotify, Discord, Slack |

---

## Platform Support

### macOS

- User caches (`~/Library/Caches`)
- Application Support (`~/Library/Application Support`)
- Logs (`~/Library/Logs`)
- Developer tools (Xcode, CocoaPods)
- Homebrew cache
- Container apps

### Linux

- XDG cache (`~/.cache`)
- Config directories (`~/.config`)
- Snap and Flatpak data
- System logs
- Development caches

### Windows

- Temp directories (`%TEMP%`, `C:\Windows\Temp`)
- Local app data (`%LOCALAPPDATA%`)
- Roaming app data (`%APPDATA%`)
- Browser caches
- Windows Update cache

---

## Export Formats

### Text (Terminal)
Colored, formatted output with progress bars and summaries.

### JSON
Complete structured data for automation and APIs.

```bash
cachekaro analyze --format json > report.json
```

### CSV
Flat data for spreadsheet analysis.

```bash
cachekaro analyze --format csv --output report.csv
```

### HTML
Interactive report with:
- Pie charts (space by category)
- Bar charts (top consumers)
- Sortable/filterable tables
- Dark/light mode

```bash
cachekaro report --format html --output report.html
```

---

## Configuration

Create a config file at `~/.config/cachekaro/config.yaml`:

```yaml
settings:
  stale_threshold_days: 30
  default_format: text
  color_output: true
  backup_before_delete: false

exclusions:
  paths: []
  patterns:
    - ".git"
    - "node_modules"

custom_paths:
  - path: ~/my-app/cache
    name: My App Cache
    category: custom
    risk_level: safe
```

---

## Safety

CacheKaro prioritizes safety:

- **Risk Levels**: Each path is classified as `safe`, `moderate`, or `caution`
- **Dry Run**: Preview what would be deleted with `--dry-run`
- **Interactive Mode**: Confirm each deletion (default)
- **Backup Option**: Create backups before deleting with `--backup`
- **No Destructive Defaults**: Auto mode requires explicit `--auto` flag

---

## Development

### Setup

```bash
git clone https://github.com/mohitbagri/cachekaro.git
cd cachekaro
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest
```

### Code Quality

```bash
ruff check .
mypy cachekaro
```

---

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- Inspired by the need for a simple, cross-platform cache cleaner
- Built with love and a bit of Hindi-English fusion: *Cache Karo!*

---

<div align="center">

**[Report Bug](https://github.com/mohitbagri/cachekaro/issues)** · **[Request Feature](https://github.com/mohitbagri/cachekaro/issues)** · **[Documentation](docs/)**

Made with ❤️ by [Mohit Bagri](https://github.com/mohitbagri)

</div>
