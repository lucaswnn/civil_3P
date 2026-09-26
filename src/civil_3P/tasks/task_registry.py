from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from civil_3P.tasks.task_plugin import TaskPlugin


class TaskRegistry:
    def __init__(self) -> None:
        self._plugins: dict[str, TaskPlugin] = {}

    def register_or_replace(self, plugin: TaskPlugin) -> None:
        identifier = plugin.metadata.identifier
        self._plugins[identifier] = plugin

    def clear_plugins(self) -> None:
        self._plugins = {}

    def get(self, identifier: str) -> TaskPlugin:
        return self._plugins[identifier]

    def all(self) -> tuple[TaskPlugin, ...]:
        return tuple(self._plugins.values())

    def get_task_identifiers(self) -> list[str]:
        return list(self._plugins.keys())
