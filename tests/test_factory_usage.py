"""Integration tests demonstrating Factory pattern usage."""
import tempfile
from pathlib import Path

import pytest

from abcdi_config import load_configuration
from abcdi_config.schema import Config


class CustomService:
    """A custom service class for testing."""

    def __init__(self, host: str, port: int, debug: bool = False):
        self.host = host
        self.port = port
        self.debug = debug

    def get_url(self) -> str:
        protocol = "http" if not self.debug else "https"
        return f"{protocol}://{self.host}:{self.port}"


class TestFactoryPattern:
    """Tests for Factory pattern usage in configurations."""

    def test_factory_creates_instance(self):
        """Test that Factory correctly creates an instance."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            config_yaml = """
dependencies:
  custom_service:
    class_: tests.test_factory_usage.CustomService
    kwargs:
      host: localhost
      port: 8080
      debug: true
"""
            f.write(config_yaml)
            config_path = Path(f.name)

        try:
            import abcdi
            load_configuration(config_path, Config)

            service = abcdi.get_dependency('custom_service')
            assert isinstance(service, CustomService)
            assert service.host == "localhost"
            assert service.port == 8080
            assert service.debug is True
            assert service.get_url() == "https://localhost:8080"

        finally:
            # Clean up
            import abcdi

            import abcdi_config
            abcdi_config.CONFIGURATION = None
            abcdi._current_context = None
            config_path.unlink()

    def test_factory_with_multiple_instances(self):
        """Test creating multiple factory instances."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            config_yaml = """
dependencies:
  service_a:
    class_: tests.test_factory_usage.CustomService
    kwargs:
      host: host-a
      port: 8080
  service_b:
    class_: tests.test_factory_usage.CustomService
    kwargs:
      host: host-b
      port: 9090
"""
            f.write(config_yaml)
            config_path = Path(f.name)

        try:
            import abcdi
            load_configuration(config_path, Config)

            service_a = abcdi.get_dependency('service_a')
            service_b = abcdi.get_dependency('service_b')

            assert service_a.host == "host-a"
            assert service_b.host == "host-b"
            assert service_a.port == 8080
            assert service_b.port == 9090

        finally:
            # Clean up
            import abcdi

            import abcdi_config
            abcdi_config.CONFIGURATION = None
            abcdi._current_context = None
            config_path.unlink()

    def test_factory_with_nested_kwargs(self):
        """Test Factory with nested configuration objects."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            config_yaml = """
dependencies:
  database:
    class_: tests.test_factory_usage.CustomService
    kwargs:
      host: db.example.com
      port: 5432
      debug: false
"""
            f.write(config_yaml)
            config_path = Path(f.name)

        try:
            import abcdi
            load_configuration(config_path, Config)

            db = abcdi.get_dependency('database')
            assert db.host == "db.example.com"
            assert db.port == 5432
            assert db.debug is False
            assert db.get_url() == "http://db.example.com:5432"

        finally:
            # Clean up
            import abcdi

            import abcdi_config
            abcdi_config.CONFIGURATION = None
            abcdi._current_context = None
            config_path.unlink()


class TestDependencyResolution:
    """Tests for dependency resolution behavior."""

    def test_dependency_not_found_raises_error(self):
        """Test that get_dependency raises when dependency doesn't exist."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("dependencies: {}")
            config_path = Path(f.name)

        try:
            import abcdi
            load_configuration(config_path, Config)

            with pytest.raises(KeyError):  # abcdi raises KeyError for unknown dependency
                abcdi.get_dependency('nonexistent')

        finally:
            # Clean up
            import abcdi

            import abcdi_config
            abcdi_config.CONFIGURATION = None
            abcdi._current_context = None
            config_path.unlink()

    def test_multiple_dependencies_independent(self):
        """Test that multiple dependencies are independent instances."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            config_yaml = """
dependencies:
  counter:
    class_: tests.test_factory_usage.CustomService
    kwargs:
      host: localhost
      port: 1000
  counter2:
    class_: tests.test_factory_usage.CustomService
    kwargs:
      host: localhost
      port: 2000
"""
            f.write(config_yaml)
            config_path = Path(f.name)

        try:
            import abcdi
            load_configuration(config_path, Config)

            counter1 = abcdi.get_dependency('counter')
            counter2 = abcdi.get_dependency('counter2')

            # Verify they are different instances
            assert counter1 is not counter2
            assert counter1.port == 1000
            assert counter2.port == 2000

        finally:
            # Clean up
            import abcdi

            import abcdi_config
            abcdi_config.CONFIGURATION = None
            abcdi._current_context = None
            config_path.unlink()
