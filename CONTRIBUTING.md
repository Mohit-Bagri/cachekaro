# Contributing to CacheKaro

Thank you for your interest in contributing to CacheKaro! This document provides guidelines and information for contributors.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/mohitbagri/cachekaro/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (OS, Python version)

### Suggesting Features

1. Check existing issues for similar suggestions
2. Create a new issue with the `enhancement` label
3. Describe the feature and its use case

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Add tests if applicable
5. Ensure all tests pass: `pytest`
6. Run linting: `ruff check .`
7. Commit with clear messages
8. Push and create a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/cachekaro.git
cd cachekaro

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check .
```

## Code Style

- Follow PEP 8 guidelines
- Use type hints for function signatures
- Write docstrings for public functions
- Keep functions focused and small
- Add tests for new functionality

## Adding New Cache Paths

To add support for new cache locations:

1. Identify the platform(s) the path applies to
2. Edit the appropriate platform file in `cachekaro/platforms/`
3. Add a `CachePath` object with:
   - `path`: The cache path
   - `name`: Display name
   - `category`: Appropriate Category enum
   - `description`: Brief description
   - `risk_level`: RiskLevel.SAFE, MODERATE, or CAUTION

Example:
```python
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

## Testing

- Write tests for new functionality
- Ensure existing tests pass
- Use fixtures from `conftest.py`
- Mock file system operations when possible

## Documentation

- Update README.md for user-facing changes
- Add docstrings to new functions
- Update CHANGELOG.md with your changes

## Questions?

Feel free to open an issue for questions or join discussions.

Thank you for contributing! 🎉
