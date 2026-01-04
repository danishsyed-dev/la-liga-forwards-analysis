# Contributing to La Liga Forwards Analysis

Thank you for your interest in contributing! 🎉

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/danishsyed-dev/la-liga-forwards-analysis/issues)
2. If not, create a new issue with:
   - A clear, descriptive title
   - Steps to reproduce the bug
   - Expected vs actual behavior
   - Screenshots if applicable

### Suggesting Features

1. Open a new issue with the `enhancement` label
2. Describe the feature and its use case
3. Explain why it would benefit users

### Pull Requests

1. **Fork** the repository
2. **Create a branch**: `git checkout -b feature/your-feature-name`
3. **Make changes** following our coding style
4. **Test** your changes: `pytest tests/ -v`
5. **Commit**: `git commit -m "Add your feature description"`
6. **Push**: `git push origin feature/your-feature-name`
7. **Open a Pull Request**

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/la-liga-forwards-analysis.git
cd la-liga-forwards-analysis

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v
```

## Coding Style

- Follow PEP 8 guidelines
- Use type hints where applicable
- Write docstrings for functions and classes
- Keep functions focused and small

## Questions?

Feel free to open an issue for any questions!
