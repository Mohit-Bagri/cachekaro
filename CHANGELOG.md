# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.5] - 2025-12-26

### Added
- Minimalist purple theme for terminal and HTML reports
- Auto-discovery for 300+ applications and games
- Glow effects and hover animations in HTML reports
- Attribution protection with obfuscation
- "Made in India" branding

### Changed
- Redesigned HTML reports with clean Inter font
- Updated ASCII art banner in terminal
- Improved footer styling (bold CacheKaro, italic Clean It Up!)

### Fixed
- CI pipeline: ruff linting and mypy type checking
- GitHub profile links

---

## [2.0.0] - 2025-12-26

### Added
- Cyberpunk-themed HTML reports with charts
- Navigation menu in README
- Serial numbers in tables

### Changed
- Complete UI overhaul
- Enhanced cache detection

---

## [1.0.0] - 2025-12-26

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
