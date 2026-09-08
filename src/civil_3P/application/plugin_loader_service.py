from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import importlib.util
import inspect
import logging
import shutil

from civil_3P.tasks.task_base import (
    TaskMetadata,
    TaskPlugin,
)

if TYPE_CHECKING:
    from types import ModuleType

logger = logging.getLogger(__name__)


class PluginLoaderService:
    def add_from(
        self,
        source_files: list[str] | list[Path],
        destiny_directory: str | Path,
    ) -> list[TaskPlugin]:
        destiny_directory = Path(destiny_directory)

        if not destiny_directory.is_dir():
            raise ValueError(
                f"Destiny directory {destiny_directory} is not a valid directory")

        loaded: list[TaskPlugin] = []

        for source_file in source_files:
            source_path = Path(source_file)

            if not source_path.is_file():
                logger.warning(
                    "Source file %s is not a valid file", source_path)
                continue

            destiny_path = destiny_directory / source_path.name

            try:
                shutil.copy2(source_path, destiny_path)
                plugin = self._get_plugin_from_file(destiny_path)

                if plugin is not None:
                    loaded.append(plugin)

            except Exception:
                logger.exception(
                    "Could not copy and load plugin from %s to %s", source_path, destiny_path)

        return loaded

    def load_from(
        self,
        directory: str | Path,
    ) -> list[TaskPlugin]:
        plugin_directory = Path(directory)

        if not plugin_directory.is_dir():
            return []

        loaded: list[TaskPlugin] = []

        for plugin_path in sorted(plugin_directory.glob("*.py")):
            plugin = self._get_plugin_from_file(plugin_path)

            if plugin is not None:
                loaded.append(plugin)

        return loaded

    def _get_plugin_from_file(
        self,
        plugin_path: str | Path,
    ) -> TaskPlugin | None:
        module_name = f"civil_3P_user_plugin_{plugin_path.stem}"

        try:
            spec = importlib.util.spec_from_file_location(
                module_name,
                plugin_path,
            )

            if spec is None or spec.loader is None:
                raise ImportError("Could not create module loader")

            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            return self._get_plugin_from_module(module)

        except Exception:
            logger.exception("Could not load plugin module %s", plugin_path)

    def _get_plugin_from_module(
        self,
        module: ModuleType,
    ) -> TaskPlugin | None:
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

            return plugin
