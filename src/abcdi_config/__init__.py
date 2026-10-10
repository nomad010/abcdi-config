import os
from pathlib import Path
from typing import Type, TypeVar

import abcdi
from abcdi_config.exceptions import (
    ConfigAlreadyLoadedError,
    ConfigError,
    DependencyFactoryError,
)

from abcdi_config.schema import Config

import yaml

__all__ = [
    "ConfigAlreadyLoadedError",
    "ConfigError",
    "DependencyFactoryError",
    "configuration",
    "load_configuration",
]

# TypeVar bound to Config for type-safe configuration classes
ConfigT = TypeVar("ConfigT", bound=Config)


CONFIGURATION = None


def _resolve_class(cls_or_path: str) -> Type[Config]:
    """Resolve a class from either a class object or import path string."""
    try:
        from importlib import import_module
        module_path, class_name = cls_or_path.rsplit('.', 1)
        module = import_module(module_path)
        cls = getattr(module, class_name)
        if not issubclass(cls, Config):
            raise ConfigError(f"Config class {cls_or_path} is not a subclass of abcdi_config.Config")
        return cls
    except (ValueError, ImportError, AttributeError) as e:
        raise ConfigError(f"Failed to resolve class {cls_or_path}: {e}") from e


def load_configuration(
    path: Path, configuration_cls: Type[ConfigT], lazy_di: bool = False
) -> None:
    """Load configuration from YAML and set up abcdi dependency injection context.

    Args:
        path: Path to the YAML configuration file.
        lazy_di: If True, dependencies are created lazily. Defaults to False.
        configuration_cls: Custom configuration class (subclass of Config).

    Example:
        load_configuration(Path("config.yaml"), Config)
        load_configuration(Path("config.yaml"), CustomConfig)
    """
    global CONFIGURATION  # pylint: disable=global-statement
    if CONFIGURATION is not None:
        raise ConfigAlreadyLoadedError()

    # Determine configuration class to use
    # Priority: CONFIGURATION_CLS env var > configuration_cls param
    configuration_class_override = os.environ.get("CONFIGURATION_CLS")
    if configuration_class_override is not None:
        config_cls = _resolve_class(configuration_class_override)
    else:
        config_cls = configuration_cls

    # Determine lazy flag - env var takes priority over function parameter
    configuration_lazy_override = os.environ.get("CONFIGURATION_LAZY")
    if configuration_lazy_override is not None:
        use_lazy_di = configuration_lazy_override.lower() == "true"
    else:
        use_lazy_di = lazy_di

    # Use context manager for proper file handling
    with open(path, encoding='utf-8') as f:
        yaml_data = yaml.safe_load(f)
    # Handle empty YAML or YAML with None
    if yaml_data is None:
        yaml_data = {}

    # Handle null dependencies
    if yaml_data.get("dependencies") is None:
        yaml_data["dependencies"] = {}

    CONFIGURATION = config_cls.model_validate(yaml_data)

    # Convert to abcdi factory format
    # Pydantic's ImportString automatically resolves the class on model instantiation
    # Factory[X] has class_ and kwargs, abcdi.factory expects cls, *args, **kwargs
    dependency_config = {}
    for name, dependency in CONFIGURATION.dependencies.items():
        try:
            dependency_config[name] = abcdi.factory(dependency.class_, **dependency.kwargs)
        except (ImportError, AttributeError) as e:
            raise DependencyFactoryError(name, e) from e

    abcdi.set_context(dependencies=dependency_config, lazy=use_lazy_di)


def configuration() -> Config:
    """Return the loaded configuration."""
    if CONFIGURATION is None:
        raise ConfigError("Configuration has not been loaded. Call load_configuration() first.")
    return CONFIGURATION
