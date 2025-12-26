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
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)](#-platform-support)
[![Tests](https://img.shields.io/badge/tests-53%20passing-brightgreen.svg)](#-testing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Commands Reference](#-commands-reference)
- [Cache Categories](#-cache-categories)
- [Platform Support](#-platform-support)
- [Export Formats](#-export-formats)
- [Configuration](#-configuration)
- [Project Structure](#-project-structure)
- [Architecture](#-architecture)
- [Safety & Risk Levels](#-safety--risk-levels)
- [API Reference](#-api-reference)
- [Development](#-development)
- [Testing](#-testing)
- [Contributing](#-contributing)
- [Roadmap](#-roadmap)
- [License](#-license)

---

## 🎯 Overview

**CacheKaro** is a production-ready, cross-platform command-line tool designed to analyze and clean cache/storage on **macOS**, **Linux**, and **Windows**. Built with Python, it provides comprehensive insights into what's consuming your disk space and safely cleans caches to free up storage.

### Why CacheKaro?

- **Unified Tool**: One tool for all operating systems instead of platform-specific solutions
- **Developer Friendly**: Cleans npm, pip, Gradle, Maven, Cargo, Go modules, Docker, and more
- **Safe by Default**: Risk-based classification prevents accidental data loss
- **Rich Insights**: Detailed metadata including file age, types, and stale detection
- **Automation Ready**: JSON/CSV export for scripts and CI/CD pipelines
- **Beautiful Reports**: Interactive HTML reports with charts and filtering

---

## ✨ Key Features

### Core Features

| Feature | Description |
|---------|-------------|
| **Cross-Platform** | Native support for macOS, Linux, and Windows |
| **56+ Cache Paths** | Pre-configured paths for browsers, dev tools, apps, system caches |
| **Smart Analysis** | Parallel scanning with progress indicators |
| **Safe Cleaning** | Interactive, auto, and dry-run modes |
| **Risk Classification** | Safe, moderate, and caution levels for each path |

### Analysis Features

| Feature | Description |
|---------|-------------|
| **Size Calculation** | Accurate size for each cache location |
| **File Count** | Total files and directories |
| **File Age Tracking** | Last accessed, modified, and created times |
| **Stale Detection** | Identify caches not accessed in X days |
| **File Type Breakdown** | Statistics by file extension |
| **Largest Files** | Top N largest files per location |
| **Category Grouping** | Organize by browser, dev tools, apps, etc. |

### Export Features

| Feature | Description |
|---------|-------------|
| **Text Output** | Colored terminal output with formatting |
| **JSON Export** | Complete structured data for APIs |
| **CSV Export** | Spreadsheet-compatible flat data |
| **HTML Reports** | Interactive charts, sortable tables |

### Cleaning Features

| Feature | Description |
|---------|-------------|
| **Interactive Mode** | Confirm each deletion with details |
| **Auto Mode** | Clean all without prompts |
| **Dry Run Mode** | Preview without deleting |
| **Category Filtering** | Clean specific categories only |
| **Size Filtering** | Clean items above minimum size |
| **Stale-Only Cleaning** | Clean only old, unused caches |
| **Backup Option** | Create backup before deletion |

---

## 📦 Installation

### From PyPI (Recommended)

```bash
pip install cachekaro
```

### From Source

```bash
# Clone the repository
git clone https://github.com/mohitbagri/cachekaro.git
cd cachekaro

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### Requirements

- **Python**: 3.9 or higher
- **Dependencies**:
  - `pyyaml` - Configuration file parsing
  - `colorama` - Cross-platform colored output (Windows)

### Verify Installation

```bash
# Check version
cachekaro --version

# Show system info
cachekaro info
```

---

## 🚀 Quick Start

### 1. Analyze Your Storage

```bash
# Run basic analysis
cachekaro analyze

# Or simply (analyze is the default command)
cachekaro
```

**Output:**
```
   ____           _          _  __
  / ___|__ _  ___| |__   ___| |/ /__ _ _ __ ___
 | |   / _` |/ __| '_ \ / _ \ ' // _` | '__/ _ \
 | |__| (_| | (__| | | |  __/ . \ (_| | | | (_) |
  \____\__,_|\___|_| |_|\___|_|\_\__,_|_|  \___/

Platform: macOS
Scanning cache locations...

================================================================================
                    CACHEKARO - STORAGE & CACHE ANALYSIS REPORT
================================================================================

DISK OVERVIEW
Total Disk Space: 228.27 GB
Used Space: 134.14 GB (58.8%)
Free Space: 94.13 GB

CACHE SUMMARY
Total Cache Size: 241.35 GB
Cleanable (Safe): 10.68 GB
Total Files: 32,167
Cache Locations: 18
```

### 2. Preview What Can Be Cleaned

```bash
# Dry run shows what would be deleted
cachekaro clean --dry-run
```

### 3. Clean Caches

```bash
# Interactive mode (recommended for first time)
cachekaro clean

# Auto mode (clean all safe items)
cachekaro clean --auto
```

### 4. Generate HTML Report

```bash
# Create interactive HTML report
cachekaro report --output my-report.html
```

---

## 📖 Commands Reference

### Main Commands

```bash
cachekaro [command] [options]
```

| Command | Aliases | Description |
|---------|---------|-------------|
| `analyze` | `scan`, `check` | Analyze storage and cache usage |
| `clean` | `clear`, `delete` | Clean cache and temporary files |
| `report` | - | Generate detailed reports |
| `info` | - | Show system information |

### `cachekaro analyze`

Analyze storage and display cache information.

```bash
cachekaro analyze [OPTIONS]
```

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--format` | `-f` | Output format: `text`, `json`, `csv`, `html` | `text` |
| `--output` | `-o` | Save output to file | - |
| `--category` | `-c` | Filter by category | `all` |
| `--min-size` | - | Minimum size (e.g., `100MB`) | `0` |
| `--stale-days` | - | Days for stale detection | `30` |
| `--safe-only` | - | Only safe-to-clean items | `false` |
| `--include-empty` | - | Include empty locations | `false` |
| `--no-color` | - | Disable colored output | `false` |
| `--quiet` | `-q` | Suppress progress output | `false` |

**Examples:**

```bash
# Basic analysis
cachekaro analyze

# JSON output to file
cachekaro analyze --format json --output cache-report.json

# Only browser caches
cachekaro analyze --category browser

# Items larger than 100MB
cachekaro analyze --min-size 100MB

# Stale items (not accessed in 60 days)
cachekaro analyze --stale-days 60 --safe-only

# Quiet mode for scripts
cachekaro analyze --format json --quiet
```

### `cachekaro clean`

Clean cache files with various safety options.

```bash
cachekaro clean [OPTIONS]
```

| Option | Description | Default |
|--------|-------------|---------|
| `--dry-run` | Preview without deleting | `false` |
| `--auto` | Clean all without prompts | `false` |
| `--category` | `-c` | Category to clean | `all` |
| `--risk` | Max risk level: `safe`, `moderate`, `caution` | `safe` |
| `--min-size` | Minimum size to clean | `0` |
| `--stale-only` | Only clean stale items | `false` |
| `--stale-days` | Days for stale detection | `30` |
| `--backup` | Backup before deleting | `false` |

**Examples:**

```bash
# Interactive mode (default)
cachekaro clean

# Preview what would be cleaned
cachekaro clean --dry-run

# Auto clean all safe items
cachekaro clean --auto

# Clean only development caches
cachekaro clean --category development --auto

# Clean stale items only
cachekaro clean --stale-only --auto

# Clean with backup
cachekaro clean --backup --auto

# Clean including moderate risk items
cachekaro clean --risk moderate --auto

# Clean items larger than 50MB
cachekaro clean --min-size 50MB --auto
```

### `cachekaro report`

Generate detailed reports in various formats.

```bash
cachekaro report [OPTIONS]
```

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--format` | `-f` | Report format: `text`, `json`, `csv`, `html` | `html` |
| `--output` | `-o` | Output file path | auto-generated |
| `--quiet` | `-q` | Suppress progress | `false` |

**Examples:**

```bash
# Generate HTML report (default)
cachekaro report

# Generate CSV report
cachekaro report --format csv --output report.csv

# Generate JSON report
cachekaro report --format json --output report.json
```

### `cachekaro info`

Display system and cache information.

```bash
cachekaro info
```

**Output:**
```
System Information
========================================
Platform: macOS
Version: 14.0
Architecture: arm64
Hostname: my-mac.local
Username: user
Home Directory: /Users/user

Disk Usage
========================================
Total: 228.27 GB
Used: 134.14 GB (58.8%)
Free: 94.13 GB

Cache Paths
========================================
Total defined: 56
Existing on system: 35
```

---

## 📂 Cache Categories

CacheKaro organizes caches into these categories:

| Category | Description | Examples |
|----------|-------------|----------|
| `user_cache` | General user application caches | System caches, app temporary files |
| `system_cache` | Operating system caches | Text understanding, geolocation |
| `browser` | Web browser caches | Chrome, Firefox, Safari, Edge, Brave |
| `development` | Developer tool caches | npm, pip, Gradle, Maven, Cargo, Docker |
| `logs` | Application and system logs | JetBrains logs, crash reports |
| `trash` | Deleted files | Trash/Recycle Bin |
| `downloads` | Downloaded files | Downloads folder |
| `application` | App-specific caches | Spotify, Discord, Slack, Zoom |
| `container` | Sandboxed app data | macOS containers, Snap, Flatpak |

### Detailed Cache Paths

#### Browsers
- Google Chrome (Cache, Code Cache, Service Workers)
- Mozilla Firefox
- Safari
- Microsoft Edge
- Brave Browser
- Chromium

#### Development Tools
- **JavaScript**: npm, pnpm, Yarn, node-gyp
- **Python**: pip, uv, HuggingFace models
- **Java**: Gradle, Maven
- **Rust**: Cargo registry
- **Go**: Go modules
- **iOS/macOS**: Xcode DerivedData, CocoaPods, Carthage
- **Containers**: Docker buildx
- **IDEs**: VS Code, Cursor, JetBrains (IntelliJ, PyCharm, WebStorm)
- **Other**: Homebrew, Playwright, Puppeteer, pre-commit

#### Applications
- Spotify
- Discord
- Slack
- Zoom
- ChatGPT
- Microsoft Teams

---

## 💻 Platform Support

### macOS

**Cache Locations:**
- `~/Library/Caches` - User caches
- `~/Library/Application Support` - App data
- `~/Library/Logs` - Log files
- `~/Library/Developer` - Xcode, simulators
- `~/Library/Containers` - Sandboxed apps
- `~/.cache` - XDG-style caches
- `~/.npm` - npm cache
- `~/.Trash` - Trash

**Special Features:**
- DNS cache flushing (`sudo dscacheutil -flushcache`)
- Xcode DerivedData cleaning
- Homebrew cache management

### Linux

**Cache Locations (XDG Compliant):**
- `~/.cache` - XDG_CACHE_HOME
- `~/.config` - XDG_CONFIG_HOME
- `~/.local/share` - XDG_DATA_HOME
- `~/.local/share/Trash` - Trash (FreeDesktop.org spec)
- `~/snap` - Snap packages
- `~/.npm` - npm cache

**Special Features:**
- XDG Base Directory Specification compliance
- Snap and Flatpak support
- Multiple DNS flush methods (systemd-resolved, nscd, dnsmasq)
- WSL detection

### Windows

**Cache Locations:**
- `%LOCALAPPDATA%` - Local app data
- `%APPDATA%` - Roaming app data
- `%TEMP%` - User temp
- `C:\Windows\Temp` - System temp
- `C:\Windows\Prefetch` - Prefetch files
- `C:\Windows\SoftwareDistribution` - Windows Update

**Special Features:**
- ANSI color support on Windows 10+
- Recycle Bin clearing via PowerShell
- DNS flush via `ipconfig /flushdns`
- Admin privilege detection

---

## 📊 Export Formats

### Text (Terminal)

Default format with colored, formatted output.

```bash
cachekaro analyze --format text
```

Features:
- ANSI colored output
- Progress bars during scanning
- Formatted tables
- Category icons
- Size highlighting (red for large, green for small)

### JSON

Structured data for automation and APIs.

```bash
cachekaro analyze --format json > report.json
```

**Structure:**
```json
{
  "summary": {
    "total_size": 259150248781,
    "formatted_total_size": "241.35 GB",
    "total_files": 32167,
    "item_count": 18,
    "cleanable_size": 11467798741,
    "stale_size": 6148,
    "stale_count": 2
  },
  "disk": {
    "total": 245107195904,
    "used": 144031326208,
    "free": 101075869696,
    "usage_percent": 58.76
  },
  "categories": { ... },
  "items": [ ... ],
  "metadata": {
    "scan_time": "2024-12-26T12:00:00",
    "duration_seconds": 5.5,
    "platform": "macOS"
  }
}
```

### CSV

Flat data for spreadsheet analysis.

```bash
cachekaro analyze --format csv --output report.csv
```

**Columns:**
- Path, Name, Category, Size (Bytes), Size (Formatted)
- File Count, Age (Days), Is Stale, Risk Level
- App Name, Description

### HTML

Interactive report with visualizations.

```bash
cachekaro report --format html --output report.html
```

**Features:**
- **Pie Chart**: Space distribution by category
- **Bar Chart**: Top cache consumers
- **Sortable Table**: Click headers to sort
- **Search/Filter**: Find specific caches
- **Responsive**: Works on mobile
- **Dark Mode**: Toggle theme support
- **Standalone**: No external dependencies (uses CDN Chart.js)

---

## ⚙️ Configuration

### Config File Location

| Platform | Path |
|----------|------|
| macOS/Linux | `~/.config/cachekaro/config.yaml` |
| Windows | `%APPDATA%\cachekaro\config.yaml` |

### Default Configuration

```yaml
# CacheKaro Configuration
# https://github.com/mohitbagri/cachekaro

settings:
  # Days after which a cache is considered stale
  stale_threshold_days: 30

  # Minimum size to display (in bytes)
  min_size_display_bytes: 1024

  # Default output format (text, json, csv, html)
  default_format: text

  # Enable colored output in terminal
  color_output: true

  # Show hidden files and directories
  show_hidden: false

  # Create backup before deleting
  backup_before_delete: false

  # Number of parallel scanning workers
  max_workers: 4

  # Number of largest files to track per location
  max_largest_files: 10

exclusions:
  # Paths to never scan or clean
  paths: []

  # Patterns to exclude (glob-style)
  patterns:
    - ".git"
    - ".svn"
    - "node_modules"

# Custom cache paths to scan
custom_paths:
  - path: ~/my-app/cache
    name: My App Cache
    category: custom
    description: Cache for my custom application
    risk_level: safe  # safe, moderate, or caution
```

### Adding Custom Paths

Add your own cache locations to scan:

```yaml
custom_paths:
  - path: ~/Projects/.build-cache
    name: Build Cache
    category: development
    description: Project build artifacts
    risk_level: safe

  - path: /var/cache/myapp
    name: MyApp System Cache
    category: application
    description: System-wide app cache
    risk_level: moderate
```

---

## 🏗️ Project Structure

```
cachekaro/
├── cachekaro/                      # Main package
│   ├── __init__.py                 # Package initialization, version
│   ├── __main__.py                 # Entry point for `python -m cachekaro`
│   ├── cli.py                      # Command-line interface (argparse)
│   │
│   ├── core/                       # Core functionality
│   │   ├── __init__.py
│   │   ├── scanner.py              # File/directory scanner
│   │   ├── analyzer.py             # Storage analysis engine
│   │   └── cleaner.py              # Safe cleaning with modes
│   │
│   ├── platforms/                  # Platform implementations
│   │   ├── __init__.py
│   │   ├── base.py                 # Abstract base class
│   │   ├── detector.py             # OS detection
│   │   ├── macos.py                # macOS: 56 cache paths
│   │   ├── linux.py                # Linux: XDG-compliant paths
│   │   └── windows.py              # Windows: AppData paths
│   │
│   ├── models/                     # Data models
│   │   ├── __init__.py
│   │   ├── cache_item.py           # CacheItem with rich metadata
│   │   └── scan_result.py          # ScanResult container
│   │
│   ├── exporters/                  # Export formats
│   │   ├── __init__.py
│   │   ├── base.py                 # Abstract exporter
│   │   ├── text.py                 # Colored terminal output
│   │   ├── json_export.py          # JSON export
│   │   ├── csv_export.py           # CSV export
│   │   └── html_export.py          # Interactive HTML reports
│   │
│   ├── config/                     # Configuration
│   │   ├── __init__.py
│   │   ├── default.py              # Config loading/saving
│   │   └── paths/                  # Platform-specific paths
│   │
│   └── utils/                      # Utilities
│       ├── __init__.py
│       ├── colors.py               # Cross-platform colors
│       └── formatting.py           # Size/time formatting
│
├── tests/                          # Test suite (53 tests)
│   ├── __init__.py
│   ├── conftest.py                 # Pytest fixtures
│   ├── test_platforms.py           # Platform tests
│   ├── test_analyzer.py            # Analyzer tests
│   ├── test_cleaner.py             # Cleaner tests
│   └── test_exporters.py           # Exporter tests
│
├── docs/                           # Documentation
│   ├── INSTALLATION.md
│   └── USAGE.md
│
├── .github/                        # GitHub configuration
│   ├── workflows/
│   │   └── ci.yml                  # CI/CD pipeline
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── pull_request_template.md
│
├── pyproject.toml                  # Modern Python packaging
├── requirements.txt                # Dependencies
├── README.md                       # This file
├── LICENSE                         # MIT License
├── CONTRIBUTING.md                 # Contribution guidelines
└── CHANGELOG.md                    # Version history
```

---

## 🏛️ Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                            CLI                                   │
│                         (cli.py)                                 │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Core Layer                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │   Scanner   │  │  Analyzer   │  │        Cleaner          │  │
│  │(scanner.py) │  │(analyzer.py)│  │      (cleaner.py)       │  │
│  └──────┬──────┘  └──────┬──────┘  └───────────┬─────────────┘  │
└─────────┼────────────────┼─────────────────────┼────────────────┘
          │                │                     │
          ▼                ▼                     ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Platform Layer                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐  │
│  │    macOS    │  │    Linux    │  │        Windows          │  │
│  │ (macos.py)  │  │ (linux.py)  │  │     (windows.py)        │  │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Models Layer                               │
│  ┌─────────────────────┐  ┌───────────────────────────────────┐ │
│  │     CacheItem       │  │          ScanResult               │ │
│  │  (cache_item.py)    │  │       (scan_result.py)            │ │
│  └─────────────────────┘  └───────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Exporters Layer                             │
│  ┌───────┐  ┌───────┐  ┌───────┐  ┌───────────────────────────┐ │
│  │ Text  │  │ JSON  │  │  CSV  │  │           HTML            │ │
│  └───────┘  └───────┘  └───────┘  └───────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **CLI** parses arguments and invokes appropriate command
2. **Platform Detector** identifies the OS and loads platform-specific paths
3. **Scanner** recursively scans paths and collects metadata
4. **Analyzer** orchestrates scanning and generates results
5. **Models** store structured data (CacheItem, ScanResult)
6. **Exporters** convert results to desired output format
7. **Cleaner** safely removes files based on user confirmation

### Key Classes

#### `CacheItem`
```python
@dataclass
class CacheItem:
    path: Path              # Cache location path
    name: str               # Display name
    category: Category      # Category enum
    description: str        # Human-readable description
    size_bytes: int         # Total size
    file_count: int         # Number of files
    last_accessed: datetime # Last access time
    age_days: int           # Days since access
    is_stale: bool          # Stale detection
    risk_level: RiskLevel   # Safe/moderate/caution
    file_types: dict        # Extension breakdown
    largest_files: list     # Top N largest files
```

#### `ScanResult`
```python
@dataclass
class ScanResult:
    items: list[CacheItem]  # All scanned items
    metadata: ScanMetadata  # Scan info
    disk_total: int         # Total disk space
    disk_used: int          # Used space
    disk_free: int          # Free space

    # Computed properties
    total_size: int
    cleanable_size: int
    stale_size: int
```

---

## 🛡️ Safety & Risk Levels

### Risk Classification

| Level | Badge | Description | Examples |
|-------|-------|-------------|----------|
| **Safe** | 🟢 | 100% safe, no data loss | Browser cache, npm cache, pip cache |
| **Moderate** | 🟡 | Generally safe, may require re-login | HuggingFace models, Maven repo |
| **Caution** | 🔴 | Review before deleting | Downloads, container data |

### Safety Features

1. **Dry Run Mode**: Preview all deletions without making changes
   ```bash
   cachekaro clean --dry-run
   ```

2. **Interactive Mode**: Confirm each item with full details
   ```bash
   cachekaro clean
   ```

3. **Risk Filtering**: Limit cleaning to safe items only
   ```bash
   cachekaro clean --risk safe
   ```

4. **Backup Option**: Create backup before deletion
   ```bash
   cachekaro clean --backup
   ```

5. **Category Isolation**: Clean specific categories only
   ```bash
   cachekaro clean --category development
   ```

---

## 📚 API Reference

### Using CacheKaro as a Library

```python
from cachekaro.platforms import get_platform
from cachekaro.core.analyzer import Analyzer
from cachekaro.core.cleaner import Cleaner, CleanMode
from cachekaro.exporters import JsonExporter

# Get platform instance
platform = get_platform()

# Create analyzer
analyzer = Analyzer(
    platform=platform,
    stale_threshold_days=30,
    min_size_bytes=1024,
)

# Run analysis
result = analyzer.analyze()

# Access results
print(f"Total cache size: {result.formatted_total_size}")
print(f"Cleanable: {result.formatted_cleanable_size}")
print(f"Items found: {len(result.items)}")

# Export to JSON
exporter = JsonExporter()
json_output = exporter.export(result)

# Clean with dry run
cleaner = Cleaner(mode=CleanMode.DRY_RUN)
summary = cleaner.clean(result.items)
print(f"Would free: {summary.formatted_size_freed}")
```

### Key APIs

```python
# Platform detection
from cachekaro.platforms import get_platform, get_platform_name
platform = get_platform()  # Returns MacOSPlatform, LinuxPlatform, or WindowsPlatform
name = get_platform_name()  # Returns 'macos', 'linux', or 'windows'

# Analysis
from cachekaro.core.analyzer import Analyzer
analyzer = Analyzer(platform)
result = analyzer.analyze(categories=[Category.BROWSER], max_risk=RiskLevel.SAFE)

# Cleaning
from cachekaro.core.cleaner import Cleaner, CleanMode
cleaner = Cleaner(mode=CleanMode.DRY_RUN)
summary = cleaner.clean(result.items)

# Export
from cachekaro.exporters import get_exporter
exporter = get_exporter('json')  # or 'text', 'csv', 'html'
output = exporter.export(result)
```

---

## 🔧 Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/mohitbagri/cachekaro.git
cd cachekaro

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install with dev dependencies
pip install -e ".[dev]"
```

### Development Dependencies

- `pytest` - Testing framework
- `pytest-cov` - Code coverage
- `ruff` - Fast Python linter
- `mypy` - Static type checking

### Code Quality

```bash
# Run linter
ruff check cachekaro tests

# Run type checker
mypy cachekaro --ignore-missing-imports

# Auto-fix linting issues
ruff check --fix cachekaro tests
```

---

## 🧪 Testing

### Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=cachekaro --cov-report=term-missing

# Run specific test file
pytest tests/test_platforms.py

# Run with verbose output
pytest -v
```

### Test Coverage

| Module | Coverage |
|--------|----------|
| `platforms/` | 87% |
| `core/` | 83% |
| `models/` | 80% |
| `exporters/` | 85% |
| **Total** | **46%** (due to platform-specific code) |

### Test Matrix

| OS | Python 3.9 | Python 3.10 | Python 3.11 | Python 3.12 |
|----|------------|-------------|-------------|-------------|
| macOS | ✅ | ✅ | ✅ | ✅ |
| Ubuntu | ✅ | ✅ | ✅ | ✅ |
| Windows | ✅ | ✅ | ✅ | ✅ |

---

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Quick Start

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Add tests for new functionality
5. Ensure tests pass: `pytest`
6. Run linting: `ruff check .`
7. Commit: `git commit -m 'Add amazing feature'`
8. Push: `git push origin feature/amazing-feature`
9. Open a Pull Request

### Adding New Cache Paths

To add support for new cache locations, edit the appropriate platform file:

```python
# In cachekaro/platforms/macos.py (or linux.py, windows.py)
CachePath(
    path=home / ".cache" / "myapp",
    name="MyApp Cache",
    category=Category.APPLICATION,
    description="MyApp application cache",
    risk_level=RiskLevel.SAFE,
    app_specific=True,
    app_name="MyApp",
)
```

---

## 🗺️ Roadmap

### Version 1.1 (Planned)
- [ ] ASCII art logo on startup
- [ ] TUI (Terminal User Interface) with `rich` library
- [ ] Watch mode for real-time monitoring
- [ ] Configuration via CLI (`cachekaro config`)

### Version 1.2 (Planned)
- [ ] Cloud cache detection (Dropbox, iCloud, OneDrive)
- [ ] Docker image and volume analysis
- [ ] Browser profile separation
- [ ] Scheduled scan support (cron/Task Scheduler)

### Version 2.0 (Future)
- [ ] GUI version (Electron/Tauri)
- [ ] System tray integration
- [ ] Notification system
- [ ] API server mode

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Mohit Bagri

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 🙏 Acknowledgments

- Inspired by the need for a unified, cross-platform cache cleaner
- Built with Python and love
- Name inspired by Hindi-English fusion: *"Cache Karo!"* means "Clean it up!"

---

<div align="center">

### Quick Links

**[Report Bug](https://github.com/mohitbagri/cachekaro/issues)** · **[Request Feature](https://github.com/mohitbagri/cachekaro/issues)** · **[Documentation](docs/)**

---

Made with ❤️ by [Mohit Bagri](https://github.com/mohitbagri)

*Cache Karo!* 🧹

</div>
