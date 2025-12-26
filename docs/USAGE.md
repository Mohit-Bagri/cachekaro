# Usage Guide

## Basic Commands

### Analyze Storage

View your cache and storage usage:

```bash
# Default analysis (text output)
cachekaro analyze

# With JSON output
cachekaro analyze --format json

# Save to file
cachekaro analyze --format html --output report.html
```

### Clean Caches

Remove cache files to free up space:

```bash
# Interactive mode (confirm each item)
cachekaro clean

# Preview what would be deleted
cachekaro clean --dry-run

# Auto mode (no confirmations)
cachekaro clean --auto
```

### Generate Reports

Create detailed reports:

```bash
# HTML report with charts
cachekaro report

# CSV for spreadsheet analysis
cachekaro report --format csv --output report.csv
```

## Analysis Options

### Filter by Category

```bash
# Only browser caches
cachekaro analyze --category browser

# Only development caches
cachekaro analyze --category development
```

Available categories:
- `user_cache` - General user caches
- `browser` - Browser caches
- `development` - Dev tool caches
- `logs` - Log files
- `trash` - Trash/Recycle Bin
- `downloads` - Downloads folder
- `application` - App-specific caches

### Filter by Size

```bash
# Only items larger than 100MB
cachekaro analyze --min-size 100MB
```

### Stale Detection

```bash
# Only show items not accessed in 60+ days
cachekaro analyze --stale-days 60
```

## Cleaning Options

### Risk Levels

```bash
# Only safe items (default)
cachekaro clean --risk safe

# Include moderate risk items
cachekaro clean --risk moderate

# Include all items (use with caution!)
cachekaro clean --risk caution
```

### Stale Only

```bash
# Only clean items not accessed recently
cachekaro clean --stale-only
```

### Backup Before Delete

```bash
# Create backup before cleaning
cachekaro clean --backup
```

## Export Formats

### Text (Default)

Colored, formatted terminal output.

### JSON

Complete structured data:

```bash
cachekaro analyze --format json | jq '.summary'
```

### CSV

Flat data for spreadsheets:

```bash
cachekaro analyze --format csv --output data.csv
```

### HTML

Interactive report with:
- Pie charts (space by category)
- Bar charts (top consumers)
- Sortable tables
- Dark/light mode

## Configuration

Create a config file for persistent settings:

```bash
# Location
# macOS/Linux: ~/.config/cachekaro/config.yaml
# Windows: %APPDATA%\cachekaro\config.yaml
```

Example config:

```yaml
settings:
  stale_threshold_days: 30
  default_format: text
  color_output: true

exclusions:
  paths:
    - ~/important-cache  # Never scan this

custom_paths:
  - path: ~/my-app/cache
    name: My App
    category: custom
    risk_level: safe
```

## Tips

1. **Start with dry-run**: Always use `--dry-run` first to preview changes
2. **Use categories**: Filter to specific categories for focused cleaning
3. **Check stale items**: Old caches are usually safe to remove
4. **Generate HTML reports**: Great for understanding your storage usage
5. **Regular cleaning**: Run periodically to keep disk space free

## Examples

### Weekly Cleanup Routine

```bash
# 1. Check what's using space
cachekaro analyze

# 2. Preview safe cleanable items
cachekaro clean --dry-run

# 3. Clean stale items automatically
cachekaro clean --auto --stale-only

# 4. Generate report for records
cachekaro report --output weekly-cleanup.html
```

### Developer Focused

```bash
# Check dev cache usage
cachekaro analyze --category development

# Clean npm, pip, gradle caches
cachekaro clean --category development --auto
```

### Before Backup

```bash
# Clean everything safe before a backup
cachekaro clean --auto --risk safe

# Verify space freed
cachekaro info
```
