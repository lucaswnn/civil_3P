from __future__ import annotations

from civil_3P.tasks.task_base import TaskPlugin


class TaskRegistry:
    def __init__(self) -> None:
        self._plugin_ids: set[str] = set()
        self._plugins: dict[str, TaskPlugin] = {}

    def register(self, plugin: TaskPlugin) -> bool:
        identifier = plugin.metadata.identifier
        if identifier in self._plugins:
            return False
        self._plugins[identifier] = plugin
        self._plugin_ids.add(identifier)
        return True

    def clear_external(self) -> None:
        self._plugins = {
            identifier: plugin
            for identifier, plugin in self._plugins.items()
            if plugin.__class__.__module__.startswith("task_examples.")
        }
        self._plugin_ids = set(self._plugins)

    def get(self, identifier: str) -> TaskPlugin:
        return self._plugins[identifier]

    def all(self) -> tuple[TaskPlugin, ...]:
        return tuple(self._plugins.values())
