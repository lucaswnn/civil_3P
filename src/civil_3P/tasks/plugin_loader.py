from __future__ import annotations

import shutil
import importlib.util
from types import ModuleType
import inspect
import logging
from pathlib import Path

from civil_3P.tasks.task_base import TaskMetadata, TaskPlugin
from civil_3P.tasks.task_registry import TaskRegistry

logger = logging.getLogger(__name__)


class PluginLoader:
    def __init__(self, registry: TaskRegistry) -> None:
        self._registry = registry

    def add_from(self,
                 source_files: list[str] | list[Path],
                 destiny_directory: str | Path,
                 ) -> list[str]:
        destiny_directory = Path(destiny_directory)
        if not destiny_directory.is_dir():
            raise ValueError(
                f"Destiny directory {destiny_directory} is not a valid directory")

        loaded: list[str] = []
        for source_file in source_files:
            source_path = Path(source_file)
            if not source_path.is_file():
                logger.warning(
                    "Source file %s is not a valid file", source_path)
                continue

            destiny_path = destiny_directory / source_path.name
            try:
                shutil.copy2(source_path, destiny_path)
                identifier = self._check_file(destiny_path)
                if identifier is not None:
                    loaded.append(identifier)
            except Exception:
                logger.exception(
                    "Could not copy and load plugin from %s to %s", source_path, destiny_path)
        return loaded

    def load_from(self, directory: str | Path) -> list[str]:
        plugin_directory = Path(directory)
        if not plugin_directory.is_dir():
            return []

        loaded: list[str] = []
        for plugin_path in sorted(plugin_directory.glob("*.py")):
            identifier = self._check_file(plugin_path)
            if identifier is not None:
                loaded.append(identifier)

        return loaded

    def _check_file(self, plugin_path: str | Path) -> str | None:
        module_name = f"civil_3P_user_plugin_{plugin_path.stem}"
        try:
            spec = importlib.util.spec_from_file_location(
                module_name, plugin_path)
            if spec is None or spec.loader is None:
                raise ImportError("Could not create module loader")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return self._check_plugin(module, plugin_path)
        except Exception:
            logger.exception("Could not load plugin module %s", plugin_path)

    def _check_plugin(self, module: ModuleType, plugin_path: Path) -> str | None:
        for _, plugin_class in inspect.getmembers(module, inspect.isclass):
            if (
                plugin_class.__module__ != module.__name__
                or plugin_class is TaskPlugin
                or not issubclass(plugin_class, TaskPlugin)
            ):
                continue
            if inspect.isabstract(plugin_class):
                continue
            plugin = plugin_class()
            metadata = plugin.metadata
            if not isinstance(metadata, TaskMetadata):
                raise TypeError("Plugin metadata must be TaskMetadata")
            if not metadata.identifier:
                raise ValueError("Plugin identifier cannot be empty")
            if self._registry.register(plugin):
                return metadata.identifier
            else:
                logger.warning(
                    "Ignoring duplicate plugin identifier %s from %s",
                    metadata.identifier,
                    plugin_path,
                )
