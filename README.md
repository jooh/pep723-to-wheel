# pep723-to-wheel

[![CI](https://github.com/jooh/pep723-to-wheel/actions/workflows/ci.yml/badge.svg)](https://github.com/jooh/pep723-to-wheel/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/jooh/pep723-to-wheel/branch/main/graph/badge.svg?token=PS0IS5TVBV)](https://codecov.io/gh/jooh/pep723-to-wheel)

A small utility for converting [PEP 723](https://peps.python.org/pep-0723/) inline dependency scripts into wheels and reconstructing scripts from wheels. Especially useful for taking [reproducible Marimo notebooks](https://marimo.io/blog/sandboxed-notebooks) to production environments.

## CLI

Build a wheel from a script that has a PEP 723 inline block:

```bash
pep723-to-wheel build path/to/script.py --output-dir dist
```

Set an explicit wheel version (defaults to calendar versioning using the script mtime as the patch segment):

```bash
pep723-to-wheel build path/to/script.py --version 2024.12.25
```

Reconstruct a script from a wheel or package name:

```bash
pep723-to-wheel import path/to/package.whl --output reconstructed.py
pep723-to-wheel import requests --output reconstructed.py
```

## Library

```python
from pathlib import Path
from pep723_to_wheel import build_script_to_wheel, import_wheel_to_script

result = build_script_to_wheel(Path("script.py"))
print(result.wheel_path)

import_result = import_wheel_to_script("requests", Path("reconstructed.py"))
print(import_result.script_path)
```

## Development

```bash
make test
make typecheck
make ruff
```
