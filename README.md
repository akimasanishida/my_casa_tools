# skrbcr CASA scripts

<a href='https://skrbcr.github.io/my_casa_tools/' target="_blank"><img alt='GitHub' src='https://img.shields.io/badge/Documentation-100000?style=flat&logo=GitHub&logoColor=white&labelColor=333333&color=007ec6'/></a>

Additional scripts for NRAO CASA.

## About

This package is a collection of Python scripts for NRAO CASA.
It contains some useful shortcuts for plotting the image with matplotlib or image analysis.
For example, you can obtain the image (from CASA style image) that can be attached to your paper with just a few lines of code:

```python
import skrbcr_casa_scripts as scs
scs.lazy_raster('your_image.image')
```

## Usage

- Documetation is available [here](https://skrbcr.github.io/my_casa_tools/).
- Sample codes with some comments are available at the `sample` directory (I will add more in the future).

## Installation

Choose one (or both) method according to your usage.

### Method 1: Install via pip

You must have Python 3.11.
Neither older nor newer versions are supported.
The dependencies cannot be installed with other versions of Python.

```bash
pip install skrbcr-casa-scripts
```

### Method 2: Install manually and use in CASA

I have not tested which version of CASA is compatible with this package but I think CASA 6 is the best choice.

First, download or clone this repository.

Then, add the following lines to your `$HOME/.casa/startup.py`:

```python
import sys
sys.path.append('/path/to/my_casa_tools')
import skrbcr_casa_scripts as scs
```

If you have already installed analysisUtils, then this is just what you did for installing it.

## Contribution

I am very happy if you contribute to this package.
When you find bugs or have some ideas, please open an issue or pull request.
