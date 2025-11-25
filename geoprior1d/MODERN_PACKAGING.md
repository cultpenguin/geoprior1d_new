# Modern Python Packaging with pyproject.toml

## Overview

This project uses **modern Python packaging standards** (PEP 517, 518, 621) with `pyproject.toml` as the single source of truth for all project metadata and dependencies.

## Why pyproject.toml?

### Benefits

1. **Single Source of Truth**: All configuration in one file
2. **Modern Standard**: PEP 621 compliant
3. **Tool Configuration**: Includes settings for black, pytest, mypy, etc.
4. **Better Dependency Management**: Clear separation of runtime vs. dev dependencies
5. **Future-Proof**: Recommended by Python packaging authorities

### Old vs. New Approach

**Old Approach (deprecated):**
```
setup.py          # Package metadata and dependencies
requirements.txt  # Runtime dependencies
setup.cfg         # Tool configurations
MANIFEST.in       # Package data
```

**Modern Approach:**
```
pyproject.toml    # Everything in one file!
requirements-dev.txt  # Optional: for quick dev setup
setup.py          # Minimal file for backward compatibility
```

## File Structure

### pyproject.toml

Contains all project configuration:

```toml
[build-system]           # Build requirements
[project]                # Package metadata
[project.dependencies]   # Runtime dependencies
[project.optional-dependencies]  # Dev, docs, etc.
[project.scripts]        # CLI entry points
[tool.*]                 # Tool configurations
```

### setup.py

Minimal file for backward compatibility:

```python
from setuptools import setup
setup()  # All config in pyproject.toml
```

### requirements-dev.txt

Optional convenience file for developers:

```bash
pip install -r requirements-dev.txt
```

Equivalent to:
```bash
pip install -e ".[dev]"
```

## Installation Methods

### For Users

```bash
# Install from source
pip install .

# Install in editable mode (development)
pip install -e .

# Install with optional dependencies
pip install -e ".[dev]"        # Development tools
pip install -e ".[docs]"       # Documentation tools
pip install -e ".[all]"        # Everything
```

### For Developers

```bash
# Option 1: Using pyproject.toml
pip install -e ".[dev]"

# Option 2: Using requirements file
pip install -e .
pip install -r requirements-dev.txt
```

## Dependency Management

### Runtime Dependencies

Defined in `[project.dependencies]`:
- numpy
- h5py
- matplotlib
- pandas
- scipy
- tqdm

These are **automatically installed** with the package.

### Optional Dependencies

Defined in `[project.optional-dependencies]`:

**Development (`dev`):**
- pytest, pytest-cov
- black, flake8, mypy, isort

**Documentation (`docs`):**
- sphinx, sphinx-rtd-theme, myst-parser

Install with:
```bash
pip install -e ".[dev]"
pip install -e ".[docs]"
pip install -e ".[all]"  # Everything
```

## Tool Configurations

All tool configurations are in `pyproject.toml`:

### Black (Code Formatter)
```bash
black geoprior1d/
```

### isort (Import Sorter)
```bash
isort geoprior1d/
```

### pytest (Testing)
```bash
pytest
pytest --cov=geoprior1d  # With coverage
```

### mypy (Type Checking)
```bash
mypy geoprior1d/
```

### flake8 (Linting)
```bash
flake8 geoprior1d/
```

## Building and Publishing

### Build Distribution

```bash
# Install build tool
pip install build

# Build wheel and source distribution
python -m build

# Output: dist/geoprior1d-1.0.0-py3-none-any.whl
#         dist/geoprior1d-1.0.0.tar.gz
```

### Publish to PyPI

```bash
# Install twine
pip install twine

# Upload to Test PyPI (recommended first)
twine upload --repository testpypi dist/*

# Upload to PyPI
twine upload dist/*
```

## Version Management

Version is defined in `pyproject.toml`:

```toml
[project]
version = "1.0.0"
```

**Alternative: Dynamic versioning**

You can use tools like `setuptools_scm` to automatically version from git tags:

```toml
[build-system]
requires = ["setuptools>=61.0", "setuptools_scm[toml]>=6.2"]

[project]
dynamic = ["version"]

[tool.setuptools_scm]
write_to = "geoprior1d/_version.py"
```

## Migration from Old Packaging

If migrating from `setup.py` + `requirements.txt`:

1. ✓ Create `pyproject.toml` with all metadata
2. ✓ Move dependencies from `requirements.txt` to `[project.dependencies]`
3. ✓ Move dev dependencies to `[project.optional-dependencies.dev]`
4. ✓ Simplify `setup.py` to just call `setup()`
5. ✓ Remove or rename `requirements.txt` to `requirements-dev.txt`
6. ✓ Test installation: `pip install -e .`

## Best Practices

### 1. Keep pyproject.toml as Single Source

Don't duplicate information between files.

**Bad:**
```
pyproject.toml: version = "1.0.0"
__init__.py: __version__ = "1.0.0"  # Duplication!
```

**Good:**
```
pyproject.toml: version = "1.0.0"
__init__.py: __version__ = "1.0.0"  # Read from installed metadata
```

### 2. Use Optional Dependencies

Organize optional dependencies by purpose:

```toml
[project.optional-dependencies]
dev = [...]      # Development tools
docs = [...]     # Documentation
test = [...]     # Testing only
all = ["pkg[dev,docs,test]"]  # Everything
```

### 3. Configure Tools in pyproject.toml

Keep all tool configurations in one place:

```toml
[tool.black]
line-length = 100

[tool.pytest.ini_options]
addopts = "--cov"

[tool.mypy]
warn_return_any = true
```

### 4. Minimal setup.py

Keep `setup.py` minimal for backward compatibility:

```python
from setuptools import setup
setup()  # Config in pyproject.toml
```

## Common Commands

```bash
# Installation
pip install -e .                 # Basic install
pip install -e ".[dev]"          # With dev tools

# Development
black geoprior1d/                # Format code
isort geoprior1d/                # Sort imports
flake8 geoprior1d/               # Lint
mypy geoprior1d/                 # Type check
pytest                           # Run tests

# Building
python -m build                  # Build distribution
twine upload dist/*              # Upload to PyPI

# Verification
pip show geoprior1d              # Show package info
pip list | grep geoprior1d       # Check installation
```

## Resources

- [PEP 517](https://peps.python.org/pep-0517/) - Build system interface
- [PEP 518](https://peps.python.org/pep-0518/) - pyproject.toml specification
- [PEP 621](https://peps.python.org/pep-0621/) - Project metadata in pyproject.toml
- [Python Packaging Guide](https://packaging.python.org/en/latest/)
- [setuptools pyproject.toml guide](https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html)

## Summary

✅ **Do:**
- Use `pyproject.toml` for all configuration
- Separate runtime and optional dependencies
- Configure tools in `pyproject.toml`
- Keep `setup.py` minimal

❌ **Don't:**
- Put dependencies in `requirements.txt` (use `pyproject.toml`)
- Duplicate configuration across files
- Use complex `setup.py` files
- Mix old and new packaging styles
