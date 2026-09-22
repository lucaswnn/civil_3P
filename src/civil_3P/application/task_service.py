from __future__ import annotations

from typing import TYPE_CHECKING

from civil_3P.tasks.task_registry import TaskRegistry
from civil_3P.tasks.task_base import TaskInputContext

if TYPE_CHECKING:
    from pathlib import Path

    from civil_3P.application.plugin_loader_service import PluginLoaderService
    from civil_3P.core.model import FEMModel
    from civil_3P.core.selection import SelectionContext
    from civil_3P.tasks.task_base import TaskResult


class TaskService:
    _instance: TaskService | None = None

    def __new__(
        cls,
        task_registry: TaskRegistry,
        plugin_loader_service: PluginLoaderService,
    ) -> TaskService:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._task_registry = task_registry
            cls._instance._plugin_loader_service = plugin_loader_service

        return cls._instance

    _task_registry: TaskRegistry
    _plugin_loader_service: PluginLoaderService

    def execute_task(
        self,
        task_id: str,
        model: FEMModel,
        selection: SelectionContext,
        case_id: str,
    ) -> TaskResult:
        plugin = self._task_registry.get(task_id)
        selection_model = model.filter_by_selection(selection)
        selection_model = selection_model.filter_by_load_case(case_id)
        context = TaskInputContext(
            full_model=model.copy(),
            selection_model=selection_model,
            case_id=case_id,
        )
        plugin.validate_input(context)

        return plugin.get_task_result(context)

    def register_plugin(self, plugin) -> bool:
        return self._task_registry.register_or_replace(plugin)

    def clear_plugins(self) -> None:
        self._task_registry.clear_plugins()

    def get_task_identifiers(self) -> list[str]:
        return self._task_registry.get_task_identifiers()

    def add_plugins_from(
        self,
        source_files: list[str] | list[Path],
        destiny_directory: str | Path,
    ) -> list[str]:
        plugins = self._plugin_loader_service.add_from(
            source_files,
            destiny_directory,
        )

        for plugin in plugins:
            self.register_plugin(plugin)

        identifiers = {plugin.metadata.identifier for plugin in plugins}

        return list(identifiers)

    def load_plugins_from(
        self,
        directory: str | Path,
    ) -> list[str]:
        plugins = self._plugin_loader_service.load_from(directory)

        for plugin in plugins:
            self.register_plugin(plugin)

        identifiers = {plugin.metadata.identifier for plugin in plugins}

        return list(identifiers)
