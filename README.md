<div align="center">

# **CacheKaro**

### Cross-Platform Storage & Cache Manager

**CacheKaro** - *Clean It Up!*

[![PyPI](https://img.shields.io/pypi/v/cachekaro.svg)](https://pypi.org/project/cachekaro/)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)](#-platform-support)
[![Tests](https://img.shields.io/badge/tests-53%20passing-brightgreen.svg)](#-development)

[Features](#-features) · [Installation](#-installation) · [Quick Start](#-quick-start) · [Commands](#-commands) · [Detection](#-what-it-detects) · [Safety](#-safety--risk-levels)

</div>

---

## ▸ Features

| # | Feature | Description |
|:-:|---------|-------------|
| 1 | **Auto-Discovery** | Automatically detects 300+ known apps and any new software you install |
| 2 | **Cross-Platform** | One tool for macOS, Linux and Windows |
| 3 | **Developer Friendly** | Cleans npm, pip, Gradle, Maven, Cargo, Go, Docker and more |
| 4 | **Game Support** | Steam, Epic Games, Riot Games, Battle.net, Minecraft and more |
| 5 | **Creative Suite** | Adobe CC, DaVinci Resolve, Blender, Ableton, AutoCAD and more |
| 6 | **Safe by Default** | Risk-based classification prevents accidental data loss |
| 7 | **Beautiful Reports** | Interactive HTML reports with charts |

---

## ▸ Installation

### ● Install from PyPI (Recommended)

```bash
pip install cachekaro
```

That's it! Now you can use `cachekaro` from anywhere.

---

<details>
<summary><b>● Install from Source (For Contributors)</b></summary>

```bash
# Clone the repository
git clone https://github.com/Mohit-Bagri/cachekaro.git
cd cachekaro

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate        # macOS/Linux
# OR
.\venv\Scripts\activate         # Windows

# Install in development mode
pip install -e ".[dev]"
```

> **Note:** When installed from source, the `cachekaro` command only works when the virtual environment is activated.

</details>

---

## ▸ Quick Start

```bash
# Analyze your storage
cachekaro analyze

# Preview what can be cleaned (safe mode)
cachekaro clean --dry-run

# Clean caches interactively
cachekaro clean

# Auto-clean all safe items without prompts
cachekaro clean --auto

# Generate HTML report
cachekaro report --output report.html
```

---

## ▸ Commands

### ● `cachekaro analyze`

Scans and displays all cache/storage usage on your system.

```bash
cachekaro analyze                          # Basic analysis
cachekaro analyze -f json                  # Output as JSON
cachekaro analyze -f csv -o data.csv       # Export to CSV
cachekaro analyze -c browser               # Only browser caches
cachekaro analyze --min-size 100MB         # Only items > 100MB
```

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--format` | `-f` | Output format: `text`, `json`, `csv` | `text` |
| `--output` | `-o` | Save output to file | stdout |
| `--category` | `-c` | Filter by category | all |
| `--min-size` | — | Minimum size filter (e.g., `50MB`, `1GB`) | `0` |
| `--stale-days` | — | Days threshold for stale detection | `30` |

---

### ● `cachekaro clean`

Removes cache files based on selected criteria.

```bash
cachekaro clean                            # Interactive mode
cachekaro clean --dry-run                  # Preview only, no deletion
cachekaro clean --auto                     # Auto-clean without prompts
cachekaro clean --auto --risk moderate     # Include moderate risk items
cachekaro clean -c browser                 # Clean only browser caches
```

| Option | Description | Default |
|--------|-------------|---------|
| `--dry-run` | Preview what would be deleted without actually deleting | `false` |
| `--auto` | Automatically clean all items without confirmation prompts | `false` |
| `--category` | Category to clean | all |
| `--risk` | Maximum risk level: `safe`, `moderate`, `caution` | `safe` |
| `--stale-only` | Only clean items older than stale threshold | `false` |

---

### ● `cachekaro report`

Generates detailed visual reports with charts.

```bash
cachekaro report                           # Generate HTML report
cachekaro report -o myreport.html          # Custom filename
cachekaro report -f json -o report.json    # JSON format
```

---

### ● `cachekaro info`

Displays system information and CacheKaro configuration.

```bash
cachekaro info
```

---

## ▸ What It Detects

CacheKaro automatically scans standard cache directories and identifies **any** application. It recognizes 300+ known apps with friendly names.

| # | Category | Examples |
|:-:|----------|----------|
| 1 | **Browser** | Chrome, Firefox, Safari, Edge, Brave, Arc, Vivaldi, Opera |
| 2 | **Development** | npm, pip, Cargo, Gradle, Maven, Docker, VS Code, JetBrains, Xcode |
| 3 | **Games** | Steam, Epic Games, Riot Games, Battle.net, Minecraft, Unity, GOG |
| 4 | **Creative** | Photoshop, Premiere Pro, After Effects, DaVinci Resolve, Final Cut Pro |
| 5 | **3D & Design** | Blender, Cinema 4D, Maya, ZBrush, SketchUp, Figma, Sketch |
| 6 | **Audio** | Ableton Live, FL Studio, Logic Pro, Pro Tools, Cubase, GarageBand |
| 7 | **Engineering** | AutoCAD, SolidWorks, Fusion 360, MATLAB, Simulink, Revit |
| 8 | **Applications** | Spotify, Discord, Slack, Zoom, WhatsApp, Notion, Obsidian |
| 9 | **System** | OS caches, temp files, logs, crash reports, font caches |

---

## ▸ Safety & Risk Levels

| Level | Icon | Description | Examples |
|-------|------|-------------|----------|
| **Safe** | 🟢 | 100% safe to delete, no data loss | Browser cache, npm cache, pip cache, temp files |
| **Moderate** | 🟡 | Generally safe, may require re-login | HuggingFace models, Maven repo, Docker images |
| **Caution** | 🔴 | Review before deleting | Downloads folder, application data |

```bash
cachekaro clean --risk safe       # Only safe items (default)
cachekaro clean --risk moderate   # Include moderate risk
cachekaro clean --risk caution --dry-run   # Preview caution items
```

---

## ▸ Export Formats

| Format | Use Case | Command |
|--------|----------|---------|
| **Text** | Terminal output with colors | `cachekaro analyze` |
| **JSON** | APIs and automation | `cachekaro analyze -f json` |
| **CSV** | Spreadsheet analysis | `cachekaro analyze -f csv -o data.csv` |
| **HTML** | Interactive reports with charts | `cachekaro report` |

---

## ▸ Platform Support

| OS | Python 3.9 | Python 3.10 | Python 3.11 | Python 3.12 |
|----|:----------:|:-----------:|:-----------:|:-----------:|
| macOS | ✓ | ✓ | ✓ | ✓ |
| Ubuntu | ✓ | ✓ | ✓ | ✓ |
| Windows | ✓ | ✓ | ✓ | ✓ |

---

## ▸ Uninstall

```bash
pip uninstall cachekaro
```

To also remove configuration files:

| Platform | Command |
|----------|---------|
| macOS/Linux | `rm -rf ~/.config/cachekaro` |
| Windows | `rmdir /s %APPDATA%\cachekaro` |

---

## ▸ License

MIT License — see [LICENSE](LICENSE)

---

<div align="center">

Made in 🇮🇳 with ❤️ by [MOHIT BAGRI](https://github.com/Mohit-Bagri)

**CacheKaro** - *Clean It Up!*

</div>
