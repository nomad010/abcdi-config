"""Custom exceptions for abcdi-config."""


class ConfigError(Exception):
    """Base exception for configuration errors."""


class ConfigLoadError(ConfigError):
    """Raised when configuration fails to load."""

    def __init__(self, message: str, original_error: Exception | None = None):
        if original_error:
            super().__init__(f"{message}: {original_error}")
            self.__cause__ = original_error
        else:
            super().__init__(message)


class ConfigAlreadyLoadedError(ConfigError):
    """Raised when trying to load configuration when already loaded."""

    def __init__(self) -> None:
        super().__init__("Configuration is already loaded. Call configuration() to access it.")


class DependencyFactoryError(ConfigError):
    """Raised when a dependency factory cannot be created."""

    def __init__(self, name: str, original_error: Exception) -> None:
        super().__init__(f"Failed to create factory for dependency '{name}': {original_error}")
        self.dependency_name = name
        self.__cause__ = original_error
