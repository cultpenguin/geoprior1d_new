# Converting to geoprior1d Python Module

## Proposed Package Structure

```
geoprior1d/
├── setup.py                      # Installation configuration
├── pyproject.toml               # Modern Python packaging (optional alternative)
├── README.md                    # User documentation
├── requirements.txt             # Dependencies
├── LICENSE                      # License file
├── MANIFEST.in                  # Include non-Python files
├── .gitignore                   # Git ignore patterns
├── geoprior1d/                  # Main package directory
│   ├── __init__.py              # Package initialization & public API
│   ├── core.py                  # Main prior_generator function
│   ├── io.py                    # Input/output (extract_prior_info)
│   ├── sampling.py              # Sampling functions (get_prior_sample)
│   ├── lithology.py             # Lithology generation (prior_lith_reals)
│   ├── resistivity.py           # Resistivity generation (prior_res_reals)
│   ├── water.py                 # Water level sampling (prior_water_reals)
│   ├── colormaps.py             # Colormap utilities (flj_log)
│   ├── visualization.py         # Plotting functions
│   └── cli.py                   # Command-line interface
├── examples/
│   ├── basic_usage.py           # Simple usage example
│   ├── custom_parameters.py     # Advanced usage
│   └── data/
│       └── *.xlsx               # Example input files
├── tests/                       # Unit tests (future)
│   ├── __init__.py
│   ├── test_io.py
│   ├── test_sampling.py
│   └── test_core.py
└── docs/                        # Documentation (future)
    └── user_guide.md
```

## Step-by-Step Conversion Plan

### 1. Create Package Structure

```bash
# Create new directory structure
mkdir -p geoprior1d/geoprior1d
mkdir -p geoprior1d/examples/data
mkdir -p geoprior1d/tests
```

### 2. Reorganize Code Files

**Map existing files to new structure:**

- `prior_generator.py` → Split into:
  - `geoprior1d/core.py` (main `generate_prior()` function)
  - `geoprior1d/visualization.py` (plotting functions)

- `helpers/extract_prior_info.py` → `geoprior1d/io.py`
- `helpers/get_prior_sample.py` → `geoprior1d/sampling.py`
- `helpers/prior_lith_reals.py` → `geoprior1d/lithology.py`
- `helpers/prior_res_reals.py` → `geoprior1d/resistivity.py`
- `helpers/prior_water_reals.py` → `geoprior1d/water.py`
- `helpers/flj_log.py` → `geoprior1d/colormaps.py`
- `main.py` → `geoprior1d/cli.py` + `examples/basic_usage.py`

### 3. Create `setup.py`

```python
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="geoprior1d",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="1D geological prior generator for stochastic lithology and resistivity modeling",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/geoprior1d",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "geoprior1d=geoprior1d.cli:main",
        ],
    },
    include_package_data=True,
)
```

### 4. Create `pyproject.toml` (Modern Alternative)

```toml
[build-system]
requires = ["setuptools>=45", "wheel", "setuptools_scm[toml]>=6.2"]
build-backend = "setuptools.build_meta"

[project]
name = "geoprior1d"
version = "1.0.0"
description = "1D geological prior generator for stochastic lithology and resistivity modeling"
readme = "README.md"
requires-python = ">=3.8"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
keywords = ["geophysics", "geology", "resistivity", "prior", "stochastic"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Science/Research",
    "Topic :: Scientific/Engineering :: Physics",
    "Programming Language :: Python :: 3",
]
dependencies = [
    "numpy>=1.20.0",
    "h5py>=3.0.0",
    "matplotlib>=3.3.0",
    "pandas>=1.2.0",
    "scipy>=1.6.0",
    "tqdm>=4.60.0",
]

[project.optional-dependencies]
dev = ["pytest>=6.0", "pytest-cov", "black", "flake8"]

[project.scripts]
geoprior1d = "geoprior1d.cli:main"

[project.urls]
Homepage = "https://github.com/yourusername/geoprior1d"
Documentation = "https://geoprior1d.readthedocs.io"
Repository = "https://github.com/yourusername/geoprior1d"
```

### 5. Create `requirements.txt`

```
numpy>=1.20.0
h5py>=3.0.0
matplotlib>=3.3.0
pandas>=1.2.0
scipy>=1.6.0
tqdm>=4.60.0
```

### 6. Create `geoprior1d/__init__.py`

```python
"""
geoprior1d: 1D Geological Prior Generator

A Python package for generating stochastic realizations of subsurface
lithology and resistivity models based on geological constraints.
"""

__version__ = "1.0.0"
__author__ = "Your Name"

# Import main API functions
from .core import generate_prior
from .io import extract_prior_info
from .sampling import get_prior_sample
from .colormaps import flj_log

# Define public API
__all__ = [
    "generate_prior",
    "extract_prior_info",
    "get_prior_sample",
    "flj_log",
]
```

### 7. Refactor `geoprior1d/core.py`

Rename `prior_generator()` to `generate_prior()` for better API naming:

```python
"""Core prior generation functionality."""

import numpy as np
import h5py
import os
from datetime import datetime
import pandas as pd

from .io import extract_prior_info
from .sampling import get_prior_sample
from .visualization import plot_resistivity_distributions, plot_realizations


def generate_prior(input_data, n_realizations, depth_max, depth_step=1, plot=False):
    """
    Generate geological prior realizations.

    Parameters
    ----------
    input_data : str
        Path to Excel file containing geological constraints.
    n_realizations : int
        Number of realizations to generate.
    depth_max : float
        Maximum depth in meters.
    depth_step : float, optional
        Depth discretization step in meters (default: 1).
    plot : bool, optional
        Whether to display visualization plots (default: False).

    Returns
    -------
    output_file : str
        Path to generated HDF5 file.
    flag_vector : list
        Status flags [max_tries_exceeded, unused, avg_tries].

    Examples
    --------
    >>> from geoprior1d import generate_prior
    >>> filename, flags = generate_prior("input.xlsx", n_realizations=1000,
    ...                                   depth_max=90, plot=True)
    """
    # Extract input parameters
    info, cmaps = extract_prior_info(input_data)

    # Create z vector and generate priors
    z_vec = np.arange(depth_step, depth_max + depth_step, depth_step)
    ms, ns, ws, flag_vector = get_prior_sample(info, z_vec, n_realizations)

    # [Rest of function implementation...]

    return output_file, flag_vector
```

### 8. Create `geoprior1d/cli.py`

```python
"""Command-line interface for geoprior1d."""

import argparse
from .core import generate_prior


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Generate 1D geological prior realizations",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "input_file",
        type=str,
        help="Path to Excel input file with geological constraints"
    )

    parser.add_argument(
        "-n", "--n-realizations",
        type=int,
        default=1000,
        help="Number of realizations to generate"
    )

    parser.add_argument(
        "-d", "--depth-max",
        type=float,
        default=90,
        help="Maximum depth in meters"
    )

    parser.add_argument(
        "-s", "--depth-step",
        type=float,
        default=1.0,
        help="Depth discretization step in meters"
    )

    parser.add_argument(
        "-p", "--plot",
        action="store_true",
        help="Display visualization plots"
    )

    parser.add_argument(
        "-v", "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )

    args = parser.parse_args()

    # Run prior generator
    filename, flag_vector = generate_prior(
        args.input_file,
        args.n_realizations,
        args.depth_max,
        args.depth_step,
        args.plot
    )

    print(f"\nDone! Output saved to: {filename}")

    if flag_vector[0] == 1:
        print("⚠️  Warning: Max iterations exceeded. Check constraints.")


if __name__ == "__main__":
    main()
```

### 9. Create `.gitignore`

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# Output files
*.h5
*.hdf5

# OS
.DS_Store
Thumbs.db
```

### 10. Create `README.md`

```markdown
# geoprior1d

1D geological prior generator for stochastic lithology and resistivity modeling.

## Installation

### From source
```bash
git clone https://github.com/yourusername/geoprior1d.git
cd geoprior1d
pip install -e .
```

### From PyPI (after publishing)
```bash
pip install geoprior1d
```

## Quick Start

### Command Line

```bash
geoprior1d input.xlsx -n 10000 -d 90 --plot
```

### Python API

```python
from geoprior1d import generate_prior

# Generate priors
filename, flags = generate_prior(
    input_data="daugaard_matlab.xlsx",
    n_realizations=10000,
    depth_max=90,
    depth_step=1,
    plot=True
)

print(f"Output saved to: {filename}")
```

## Input File Format

See [CLAUDE.md](CLAUDE.md) for detailed input format specification.

## Documentation

For full documentation, see the [user guide](docs/user_guide.md).

## License

MIT License - see LICENSE file for details.
```

### 11. Create `examples/basic_usage.py`

```python
"""Basic usage example for geoprior1d."""

from geoprior1d import generate_prior

# Set parameters
input_file = "../data/daugaard_matlab.xlsx"
n_realizations = 10000
depth_max = 90
depth_step = 1
plot = True

# Generate prior realizations
filename, flag_vector = generate_prior(
    input_data=input_file,
    n_realizations=n_realizations,
    depth_max=depth_max,
    depth_step=depth_step,
    plot=plot
)

print(f"✓ Generated {n_realizations} realizations")
print(f"✓ Output file: {filename}")

if flag_vector[0] == 1:
    print("⚠️  Warning: Some constraints could not be satisfied")
print(f"✓ Average constraint satisfaction attempts: {flag_vector[2]:.1f}")
```

## Installation & Usage After Conversion

### Development Installation

```bash
cd geoprior1d
pip install -e .
```

### Usage

```bash
# Command line
geoprior1d input.xlsx -n 10000 -d 90 --plot

# Python
python -c "from geoprior1d import generate_prior; generate_prior('input.xlsx', 1000, 90)"
```

## Benefits of Module Structure

1. **Easy Installation**: `pip install geoprior1d`
2. **Clean Imports**: `from geoprior1d import generate_prior`
3. **CLI Tool**: `geoprior1d` command available system-wide
4. **Better Organization**: Clear separation of concerns
5. **Testable**: Easy to add unit tests
6. **Distributable**: Can publish to PyPI
7. **Version Control**: Proper versioning with `__version__`
8. **Documentation**: Clear API and examples

## Migration Checklist

- [ ] Create new directory structure
- [ ] Move and refactor code files
- [ ] Update all imports to use relative imports
- [ ] Create `setup.py` or `pyproject.toml`
- [ ] Create `requirements.txt`
- [ ] Create `__init__.py` with public API
- [ ] Create CLI script
- [ ] Write README.md
- [ ] Create .gitignore
- [ ] Move example data to examples/data/
- [ ] Test installation: `pip install -e .`
- [ ] Test CLI: `geoprior1d --help`
- [ ] Test import: `python -c "import geoprior1d"`
- [ ] Run examples to verify functionality
- [ ] Update CLAUDE.md with new structure
- [ ] (Optional) Add unit tests
- [ ] (Optional) Set up CI/CD
- [ ] (Optional) Publish to PyPI
