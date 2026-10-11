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
