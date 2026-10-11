from typing import Any

from pydantic import BaseModel, ImportString
from pydantic_settings import BaseSettings


class Factory[X](BaseModel):
    """Factory pattern for dynamically creating instances of classes with configuration."""
    class_: ImportString[type[X]]  # Class to instantiate (import path as string)
    kwargs: dict[str, Any] = {}  # Keyword arguments to pass to class constructor


class Config(BaseSettings):
    dependencies: dict[str, Factory[Any]] = {}  # Named dependencies to create upfront and make available throughout the application
