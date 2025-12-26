# CacheKaro

<div align="center">

### **Cross-Platform Storage & Cache Manager**

*Cache Karo!* — Clean it up!

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)](#-platform-support)
[![Tests](https://img.shields.io/badge/tests-53%20passing-brightgreen.svg)](#-development)

</div>

---

## > Overview

**CacheKaro** is a cross-platform CLI tool to analyze and clean cache/storage on **macOS**, **Linux** and **Windows**. It automatically discovers caches from all installed applications and games.

### Why CacheKaro?

| Feature | Description |
|---------|-------------|
| **Auto-Discovery** | Automatically detects 300+ known apps and any new software you install |
| **Cross-Platform** | One tool for macOS, Linux and Windows |
| **Developer Friendly** | Cleans npm, pip, Gradle, Maven, Cargo, Go, Docker and more |
| **Game Support** | Steam, Epic Games, Riot Games, Battle.net, Minecraft and more |
| **Creative Suite** | Adobe CC, DaVinci Resolve, Blender, Ableton, AutoCAD and more |
| **Safe by Default** | Risk-based classification prevents accidental data loss |
| **Beautiful Reports** | Cyberpunk-themed HTML reports with charts |

---

## > Installation

### From Source

```bash
git clone https://github.com/mohitbagri/cachekaro.git
cd cachekaro
pip install -e .
```

### Run from anywhere

After installation, you can run `cachekaro` from any directory:

```bash
cachekaro analyze
cachekaro clean
cachekaro report
```

**Requirements:** Python 3.9+

---

## > Uninstall

```bash
pip uninstall cachekaro
```

To also remove configuration files:

| Platform | Config Path |
|----------|-------------|
| macOS/Linux | `rm -rf ~/.config/cachekaro` |
| Windows | `rmdir /s %APPDATA%\cachekaro` |

---

## > Quick Start

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

## > Commands

| Command | Description |
|---------|-------------|
| `cachekaro analyze` | Analyze storage and cache usage |
| `cachekaro clean` | Clean cache files (interactive, auto or dry-run) |
| `cachekaro report` | Generate detailed reports |
| `cachekaro info` | Show system information |

---

## > Options Reference

### Analyze Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--format` | `-f` | Output format | `text` |
| `--output` | `-o` | Save to file | — |
| `--category` | `-c` | Filter by category | `all` |
| `--min-size` | — | Minimum size (e.g., `100MB`) | `0` |
| `--stale-days` | — | Days for stale detection | `30` |

### Clean Options

| Option | Description | Default |
|--------|-------------|---------|
| `--dry-run` | Preview without deleting | `false` |
| `--auto` | Clean all without prompts | `false` |
| `--category` | Category to clean | `all` |
| `--risk` | Max risk level | `safe` |
| `--stale-only` | Only clean stale items | `false` |

### Report Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--format` | `-f` | Report format | `html` |
| `--output` | `-o` | Output file path | auto-generated |

---

## > What It Detects

### Automatic Discovery

CacheKaro automatically scans standard cache directories and identifies **any** application by its folder name. It recognizes 300+ known apps with friendly names.

### Categories

| Category | Examples |
|----------|----------|
| **Browser** | Chrome, Firefox, Safari, Edge, Brave, Arc, Vivaldi |
| **Development** | npm, pip, Cargo, Gradle, Maven, Docker, VS Code, JetBrains |
| **Games** | Steam, Epic Games, Riot Games, Battle.net, Minecraft, Unity |
| **Creative** | Photoshop, Premiere Pro, After Effects, DaVinci Resolve, Final Cut Pro |
| **3D & Design** | Blender, Cinema 4D, Maya, ZBrush, SketchUp, Figma |
| **Audio** | Ableton Live, FL Studio, Logic Pro, Pro Tools, Cubase |
| **Engineering** | AutoCAD, SolidWorks, Fusion 360, MATLAB, Simulink |
| **Applications** | Spotify, Discord, Slack, Zoom, WhatsApp, Notion |
| **System** | OS caches, temp files, logs, crash reports |

### Platform-Specific Paths

| Platform | Locations Scanned |
|----------|-------------------|
| **macOS** | `~/Library/Caches`, `~/.cache`, `~/Library/Logs` |
| **Linux** | `~/.cache`, `~/.config`, `~/.local/share`, `~/.steam` |
| **Windows** | `%LOCALAPPDATA%`, `%APPDATA%`, `%TEMP%` |

---

## > Safety & Risk Levels

| Level | Icon | Description | Examples |
|-------|------|-------------|----------|
| **Safe** | 🟢 | 100% safe, no data loss | Browser cache, npm cache, pip cache |
| **Moderate** | 🟡 | Generally safe, may require re-login | HuggingFace models, Maven repo |
| **Caution** | 🔴 | Review before deleting | Downloads folder |

```bash
# Only clean safe items (default)
cachekaro clean --risk safe

# Include moderate risk items
cachekaro clean --risk moderate
```

---

## > Export Formats

| Format | Use Case | Default |
|--------|----------|---------|
| **Text** | Terminal output with colors | `analyze` default |
| **JSON** | APIs and automation | — |
| **CSV** | Spreadsheet analysis | — |
| **HTML** | Interactive reports with charts | `report` default |

---

## > Configuration

**Config file location:**

| Platform | Path |
|----------|------|
| macOS/Linux | `~/.config/cachekaro/config.yaml` |
| Windows | `%APPDATA%\cachekaro\config.yaml` |

**Example config:**

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

## > Development

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

## > Platform Support

| OS | Python 3.9 | Python 3.10 | Python 3.11 | Python 3.12 |
|----|:----------:|:-----------:|:-----------:|:-----------:|
| macOS | ✅ | ✅ | ✅ | ✅ |
| Ubuntu | ✅ | ✅ | ✅ | ✅ |
| Windows | ✅ | ✅ | ✅ | ✅ |

---

## > License

MIT License - see [LICENSE](LICENSE)

---

<div align="center">

Made with ❤️ by [Mohit Bagri](https://github.com/mohitbagri)

*Cache Karo!* — Clean it up!

</div>
