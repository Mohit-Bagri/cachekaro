# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-26

### Added

- Initial release of CacheKaro
- Cross-platform support for macOS, Linux, and Windows
- Storage analysis with comprehensive metadata:
  - File sizes and counts
  - File age and staleness detection
  - File type breakdown
  - Largest files tracking
- Multiple cleaning modes:
  - Interactive (confirm each item)
  - Auto (clean all without prompts)
  - Dry-run (preview only)
- Risk level classification (safe, moderate, caution)
- Export formats:
  - Text (terminal with colors)
  - JSON (structured data)
  - CSV (spreadsheet compatible)
  - HTML (interactive charts and tables)
- Cache categories:
  - User caches
  - Browser caches (Chrome, Firefox, Safari, Edge, Brave)
  - Development caches (npm, pip, Gradle, Maven, Cargo, Go)
  - Application caches (Spotify, Discord, Slack, VS Code)
  - Logs
  - Trash
  - Downloads
- Configuration file support
- Progress indicators during scanning
- Colored terminal output
- Command-line interface with subcommands

### Platform-Specific Features

#### macOS
- Library/Caches scanning
- Application Support caches
- Xcode derived data
- Homebrew cache
- Container apps

#### Linux
- XDG cache directories
- Snap and Flatpak support
- System logs

#### Windows
- Temp directories
- AppData caches
- Windows Update cache
- Prefetch files

---

## [Unreleased]

### Planned
- TUI (Terminal User Interface) mode
- Watch mode for real-time monitoring
- Cloud cache detection (Dropbox, iCloud, OneDrive)
- Docker cache analysis
- ASCII art logo
- Scheduled scan support
