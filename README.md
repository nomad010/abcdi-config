# abcdi-config

A Python library for configuration-based dependency injection using the abcdi library.
Define your application dependencies in YAML configuration files and automatically
instantiate them with proper dependency injection.

## Features

- Configuration-driven dependency injection
- YAML-based configuration files
- Factory pattern for creating instances
- Support for environment variable overrides
- Type safety with Pydantic validation
- Lazy dependency loading support

## Installation

```bash
pip install abcdi-config
```

## Quick Start

```python
from pathlib import Path
from abcdi_config import load_configuration, configuration
from abcdi_config.schema import Config

# Load configuration from YAML file
load_configuration(Path("config.yaml"), Config)

# Access the loaded configuration
config = configuration()

# Get dependencies using abcdi
import abcdi
db = abcdi.get_dependency('database')
```

## Configuration Format

```yaml
dependencies:
  database:
    class_: sqlalchemy.create_engine
    kwargs:
      url: postgresql://user:pass@localhost/db
      echo: true
  
  api_client:
    class_: requests.Session
    kwargs:
      timeout: 30
```

## Development

This project uses `uv` for dependency management and virtual environments.

### Setup

```bash
# Install dependencies
uv sync

# Or install dependencies into your existing virtualenv
uv pip sync requirements.txt dev-requirements.txt
```

### Linting

#### Pylint

Pylint is configured with a focus on reducing false positives for test files while catching real issues in production code.

```bash
uv run pylint src/ tests/
```

#### MyPy

MyPy type checking is configured to skip third-party library stubs.

```bash
uv run mypy src/ tests/
```

### Running Tests

```bash
uv run pytest tests/
```

## Publishing to PyPI

This project uses `build` and `twine` for publishing to PyPI.

### Setup

Install build and twine:

```bash
uv add --dev build twine
```

### Release Process

1. Update the version in the `version` file:

   ```bash
   echo "0.1.0" > version
   ```

2. Build the package:

   ```bash
   uv run python -m build
   ```

3. Upload to PyPI (test or production):

   ```bash
   # Upload to TestPyPI (recommended for testing)
   uv run twine upload --repository testpypi dist/*

   # Or upload directly to PyPI
   uv run twine upload dist/*
   ```

   You'll need a PyPI API token. Generate one at https://pypi.org/manage/account/token/

## License

MIT License - see the [LICENSE](LICENSE) file for details
