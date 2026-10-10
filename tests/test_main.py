"""Test that demonstrates the basic functionality of abcdi-config."""

import tempfile
from pathlib import Path
import pytest

from abcdi_config import load_configuration, configuration
from abcdi_config.schema import Config


def test_basic_import():
    """Test that the package can be imported."""
    assert True


def test_empty_config():
    """Test loading an empty configuration."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        f.write("dependencies: {}")
        config_path = Path(f.name)

    try:
        load_configuration(config_path, Config)
        cfg = configuration()
        assert cfg.dependencies == {}
    finally:
        config_path.unlink()


if __name__ == "__main__":
    # Run tests directly
    test_basic_import()
    test_empty_config()
    print("All tests passed!")