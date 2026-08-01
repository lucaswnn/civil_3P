from __future__ import annotations

from civil_3P.tasks.base import TaskPlugin
from civil_3P.tasks.check_example import ExampleBarCheckPlugin
from civil_3P.tasks.design_example import ExampleShellDesignPlugin


class BuiltinTaskRegistry:
    def __init__(self) -> None:
        self._plugins: dict[str, TaskPlugin] = {
            plugin.metadata.identifier: plugin
            for plugin in (ExampleBarCheckPlugin(), ExampleShellDesignPlugin())
        }

    def get(self, identifier: str) -> TaskPlugin:
        return self._plugins[identifier]

    def all(self) -> tuple[TaskPlugin, ...]:
        return tuple(self._plugins.values())
