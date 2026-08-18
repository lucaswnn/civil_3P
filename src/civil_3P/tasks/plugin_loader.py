from __future__ import annotations

import importlib.util
import inspect
import logging
from pathlib import Path

from civil_3P.tasks.task_base import TaskMetadata, TaskPlugin
from civil_3P.tasks.task_registry import TaskRegistry

logger = logging.getLogger(__name__)


class PluginLoader:
    def __init__(self, registry: TaskRegistry) -> None:
        self._registry = registry

    def load_from(self, directory: str | Path) -> tuple[str, ...]:
        plugin_directory = Path(directory)
        if not plugin_directory.is_dir():
            return ()

        loaded: list[str] = []
        for plugin_path in sorted(plugin_directory.glob("*.py")):
            module_name = f"civil_3P_user_plugin_{plugin_path.stem}"
            try:
                spec = importlib.util.spec_from_file_location(
                    module_name, plugin_path)
                if spec is None or spec.loader is None:
                    raise ImportError("Could not create module loader")
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
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
                        loaded.append(metadata.identifier)
                    else:
                        logger.warning(
                            "Ignoring duplicate plugin identifier %s from %s",
                            metadata.identifier,
                            plugin_path,
                        )
            except Exception:
                logger.exception("Could not load plugin module %s", plugin_path)

        return tuple(loaded)