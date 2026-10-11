"""Edge case and validation tests for abcdi-config."""
import tempfile
from pathlib import Path

import pytest
from pydantic import ValidationError

from abcdi_config import load_configuration
from abcdi_config.schema import Config


class TestValidation:
    """Tests for configuration validation."""

    def test_missing_class_field_raises_error(self):
        """Test that missing 'class' field raises ValidationError."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            config_yaml = """
dependencies:
  my_factory:
    kwargs:
      value: test
"""
            f.write(config_yaml)
            config_path = Path(f.name)

        try:
            with pytest.raises(ValidationError):
                load_configuration(config_path, Config)
        finally:
            config_path.unlink()

    def test_nonexistent_class_raises_error(self):
        """Test that nonexistent class path raises error."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            config_yaml = """
dependencies:
  my_factory:
    class_: nonexistent.module.ThatClass
    kwargs:
      value: test
"""
            f.write(config_yaml)
            config_path = Path(f.name)

        try:
            with pytest.raises(ValidationError):
                load_configuration(config_path, Config)
        finally:
            config_path.unlink()
