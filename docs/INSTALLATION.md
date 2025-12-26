# Installation Guide

## Requirements

- Python 3.9 or higher
- pip (Python package manager)

## Install from PyPI

The easiest way to install CacheKaro:

```bash
pip install cachekaro
```

## Install from Source

### Clone the Repository

```bash
git clone https://github.com/mohitbagri/cachekaro.git
cd cachekaro
```

### Install in Development Mode

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install with development dependencies
pip install -e ".[dev]"
```

### Install in Regular Mode

```bash
pip install .
```

## Verify Installation

```bash
# Check version
cachekaro --version

# Run info command
cachekaro info
```

## Platform-Specific Notes

### macOS

No additional setup required. CacheKaro will use standard macOS paths.

### Linux

No additional setup required. CacheKaro follows XDG Base Directory Specification.

### Windows

CacheKaro automatically enables ANSI color support on Windows 10+.

For older Windows versions, colors may not display correctly in the default command prompt. Consider using Windows Terminal or PowerShell.

## Uninstall

```bash
pip uninstall cachekaro
```

## Troubleshooting

### "command not found: cachekaro"

Make sure the Python Scripts directory is in your PATH:

- **macOS/Linux**: Usually `~/.local/bin`
- **Windows**: Usually `%APPDATA%\Python\Python3X\Scripts`

### Permission Errors

Some cache paths may require administrator privileges. Run with sudo (Linux/macOS) or as Administrator (Windows) if needed.

### Import Errors

Ensure you're using Python 3.9 or higher:

```bash
python --version
```
