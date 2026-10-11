"""Integration tests for abcdi-config."""
import tempfile
from pathlib import Path

from abcdi_config import configuration, load_configuration
from abcdi_config.schema import Config


class CustomGreeting(Config):
    """A custom greeting config for testing."""

    name: str = "World"


def test_load_configuration_with_datetime():
    """Test loading configuration with a stdlib class (datetime.datetime)."""
    import abcdi
    # Create a temporary YAML configuration file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        config_yaml = """
dependencies:
  my_datetime:
    class_: datetime.datetime
    kwargs:
      year: 2024
      month: 1
      day: 15
"""
        f.write(config_yaml)
        config_path = Path(f.name)

    try:
        # Load the configuration
        load_configuration(config_path, Config)

        # Get the loaded configuration
        loaded_config = configuration()
        assert 'my_datetime' in loaded_config.dependencies

        # Get the dependency from abcdi context
        dt = abcdi.get_dependency('my_datetime')
        assert dt.year == 2024
        assert dt.month == 1
        assert dt.day == 15

    finally:
        # Clean up
        import abcdi

        import abcdi_config
        abcdi_config.CONFIGURATION = None
        abcdi._current_context = None
        config_path.unlink()


def test_load_configuration_with_custom_class():
    """Test loading configuration with a custom class from the project."""
    import abcdi
    # Create a temporary YAML configuration file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        config_yaml = """
dependencies:
  greeting:
    class_: tests.test_integration.CustomGreeting
    kwargs:
      name: World
"""
        f.write(config_yaml)
        config_path = Path(f.name)

    try:
        # Load the configuration
        load_configuration(config_path, Config)

        # Get the dependency from abcdi context
        greeting = abcdi.get_dependency('greeting')
        assert greeting.name == "World"

    finally:
        # Clean up
        import abcdi

        import abcdi_config
        abcdi_config.CONFIGURATION = None
        abcdi._current_context = None
        config_path.unlink()
