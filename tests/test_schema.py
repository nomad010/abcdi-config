"""Unit tests for the schema module."""
import pytest
from pydantic import ValidationError

from abcdi_config.schema import Config, Factory


class TestFactory:
    """Tests for the Factory class."""

    def test_factory_with_no_kwargs(self):
        """Test Factory with minimal kwargs (empty dict)."""
        factory = Factory(class_="datetime.datetime", kwargs={})
        assert factory.class_.__name__ == "datetime"
        assert factory.kwargs == {}

    def test_factory_with_kwargs(self):
        """Test Factory with keyword arguments."""
        factory = Factory(
            class_="datetime.datetime",
            kwargs={"year": 2024, "month": 1, "day": 15}
        )
        assert factory.class_.__name__ == "datetime"
        assert factory.kwargs == {"year": 2024, "month": 1, "day": 15}

    def test_factory_invalid_class(self):
        """Test Factory with invalid class path."""
        with pytest.raises(ValidationError) as exc_info:
            Factory(class_="nonexistent.module.Class", kwargs={})
        # The error message should indicate an invalid import path
        assert "nonexistent.module.Class" in str(exc_info.value)

    def test_factory_with_custom_class(self):
        """Test Factory with a custom class."""
        from pathlib import Path

        # Use Path from pathlib as the test class - it's a known importable class
        factory = Factory(class_="pathlib.Path", kwargs={})
        assert factory.class_ is Path
        assert factory.kwargs == {}


class TestConfig:
    """Tests for the Config class."""

    def test_config_with_no_dependencies(self):
        """Test Config with empty dependencies."""
        config = Config(dependencies={})
        assert config.dependencies == {}

    def test_config_with_single_dependency(self):
        """Test Config with a single dependency."""
        config = Config(dependencies={
            "my_factory": Factory(class_="datetime.datetime", kwargs={})
        })
        assert len(config.dependencies) == 1
        assert "my_factory" in config.dependencies

    def test_config_with_multiple_dependencies(self):
        """Test Config with multiple dependencies."""
        config = Config(dependencies={
            "factory1": Factory(class_="datetime.datetime", kwargs={}),
            "factory2": Factory(class_="os.PathLike", kwargs={}),
        })
        assert len(config.dependencies) == 2
        assert "factory1" in config.dependencies
        assert "factory2" in config.dependencies

    def test_config_default_dependencies(self):
        """Test Config default dependencies value."""
        config = Config()
        assert config.dependencies == {}
