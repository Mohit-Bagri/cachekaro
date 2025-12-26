# CacheKaro

<div align="center">

```
   ____           _          _  __
  / ___|__ _  ___| |__   ___| |/ /__ _ _ __ ___
 | |   / _` |/ __| '_ \ / _ \ ' // _` | '__/ _ \
 | |__| (_| | (__| | | |  __/ . \ (_| | | | (_) |
  \____\__,_|\___|_| |_|\___|_|\_\__,_|_|  \___/
```

### **Cross-Platform Storage & Cache Manager**

*Cache Karo!* (Hindi-English: "Clean it up!")

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)](#platform-support)
[![Tests](https://img.shields.io/badge/tests-53%20passing-brightgreen.svg)](#testing)

</div>

---

## Overview

**CacheKaro** is a cross-platform CLI tool to analyze and clean cache/storage on **macOS**, **Linux**, and **Windows**. It automatically discovers caches from all installed applications and games.

### Why CacheKaro?

- **Auto-Discovery**: Automatically detects 200+ known apps and any new software you install
- **Cross-Platform**: One tool for macOS, Linux, and Windows
- **Developer Friendly**: Cleans npm, pip, Gradle, Maven, Cargo, Go, Docker, and more
- **Game Support**: Steam, Epic Games, Riot Games (Valorant/LoL), Battle.net, and more
- **Safe by Default**: Risk-based classification prevents accidental data loss
- **Beautiful Reports**: Cyberpunk-themed HTML reports with charts

---

## Installation

```bash
# From PyPI
pip install cachekaro

# Or from source
git clone https://github.com/mohitbagri/cachekaro.git
cd cachekaro
pip install -e .
```

**Requirements:** Python 3.9+

---

## Quick Start

```bash
# Analyze your storage
cachekaro analyze

# Preview what can be cleaned
cachekaro clean --dry-run

# Clean caches interactively
cachekaro clean

# Auto-clean all safe items
cachekaro clean --auto

# Generate HTML report
cachekaro report --output report.html
```

---

## Commands

| Command | Description |
|---------|-------------|
| `cachekaro analyze` | Analyze storage and cache usage |
| `cachekaro clean` | Clean cache files (interactive, auto, or dry-run) |
| `cachekaro report` | Generate detailed HTML/JSON/CSV reports |
| `cachekaro info` | Show system information |

### Common Options

```bash
# Output formats
cachekaro analyze --format json --output report.json
cachekaro analyze --format csv --output report.csv

# Filter by category
cachekaro analyze --category browser
cachekaro analyze --category development
cachekaro analyze --category game

# Clean options
cachekaro clean --dry-run          # Preview only
cachekaro clean --auto             # No prompts
cachekaro clean --category dev     # Clean only dev caches
cachekaro clean --stale-only       # Only old caches
cachekaro clean --risk moderate    # Include moderate risk items
```

---

## What It Detects

### Automatic Discovery
CacheKaro automatically scans standard cache directories and identifies **any** application by its folder name. It recognizes 200+ known apps with friendly names.

### Categories

| Category | Examples |
|----------|----------|
| **Browser** | Chrome, Firefox, Safari, Edge, Brave, Arc, Vivaldi |
| **Development** | npm, pip, Cargo, Gradle, Maven, Docker, VS Code, JetBrains |
| **Games** | Steam, Epic Games, Riot Games, Battle.net, Minecraft, Unity |
| **Applications** | Spotify, Discord, Slack, Zoom, WhatsApp, ChatGPT, Claude |
| **System** | OS caches, temp files, logs, crash reports |

### Platform-Specific Paths

| Platform | Locations Scanned |
|----------|-------------------|
| **macOS** | `~/Library/Caches`, `~/.cache`, `~/Library/Logs`, `~/Library/Application Support` |
| **Linux** | `~/.cache`, `~/.config`, `~/.local/share`, `~/.steam` |
| **Windows** | `%LOCALAPPDATA%`, `%APPDATA%`, `%TEMP%`, `C:\Program Files (x86)\Steam` |

---

## Safety & Risk Levels

| Level | Description | Examples |
|-------|-------------|----------|
| **Safe** | 100% safe, no data loss | Browser cache, npm cache, pip cache |
| **Moderate** | Generally safe, may require re-login | HuggingFace models, Maven repo |
| **Caution** | Review before deleting | Downloads folder |

```bash
# Only clean safe items (default)
cachekaro clean --risk safe

# Include moderate risk items
cachekaro clean --risk moderate
```

---

## Export Formats

| Format | Use Case |
|--------|----------|
| **Text** | Terminal output with colors |
| **JSON** | APIs and automation |
| **CSV** | Spreadsheet analysis |
| **HTML** | Interactive reports with charts (cyberpunk theme) |

```bash
cachekaro report --format html --output report.html
```

---

## Configuration

Config file location:
- macOS/Linux: `~/.config/cachekaro/config.yaml`
- Windows: `%APPDATA%\cachekaro\config.yaml`

```yaml
settings:
  stale_threshold_days: 30
  default_format: text
  color_output: true
  backup_before_delete: false

custom_paths:
  - path: ~/my-app/cache
    name: My App Cache
    category: custom
    risk_level: safe
```

---

## Development

```bash
# Setup
git clone https://github.com/mohitbagri/cachekaro.git
cd cachekaro
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"

# Run tests
pytest

# Linting
ruff check .
mypy cachekaro
```

---

## Platform Support

| OS | Python 3.9 | Python 3.10 | Python 3.11 | Python 3.12 |
|----|:----------:|:-----------:|:-----------:|:-----------:|
| macOS | ✅ | ✅ | ✅ | ✅ |
| Ubuntu | ✅ | ✅ | ✅ | ✅ |
| Windows | ✅ | ✅ | ✅ | ✅ |

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes and add tests
4. Run tests: `pytest` and `ruff check .`
5. Commit and push
6. Open a Pull Request

---

## License

MIT License - see [LICENSE](LICENSE)

---

<div align="center">

**[Report Bug](https://github.com/mohitbagri/cachekaro/issues)** · **[Request Feature](https://github.com/mohitbagri/cachekaro/issues)**

Made with ❤️ by [Mohit Bagri](https://github.com/mohitbagri)

*Cache Karo!*

</div>
