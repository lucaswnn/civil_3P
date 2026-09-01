from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from pathlib import Path

import pandas as pd

from civil_3P.core.model import FEMModel
from civil_3P.core.results import ResultProcessor, VisualizationCriteria
from civil_3P.core.selection import SelectionContext
from civil_3P.importers.importer_registry import ImporterRegistry
from civil_3P.tasks.task_registry import TaskRegistry
from civil_3P.tasks.plugin_loader import PluginLoader
from civil_3P.tasks.task_base import TaskContext, TaskResult
from civil_3P.visualization.scene_builder import SceneBuilder
from civil_3P.standard import model_representation as rpr
from civil_3P.standard.importer_profiles import ImporterProfiles
from civil_3P.standard.result_components import Result
from civil_3P.application.preferences import UserPreferencesService


class ImportModelService:
    def __init__(self, registry: ImporterRegistry | None = None) -> None:
        self._registry = registry or ImporterRegistry()

    def import_model(
        self, profile: ImporterProfiles, directory: str | Path
    ) -> FEMModel:
        return self._registry.import_model(profile, directory)


class TaskExecutionService:
    def __init__(
        self,
        task_registry: TaskRegistry | None = None,
        context: ApplicationContext | None = None,
    ) -> None:
        self._task_registry = (
            task_registry or (context or ApplicationContext()).task_registry
        )

    def execute(
        self, task_id: str, model: FEMModel, selection: SelectionContext, case_id: str
    ) -> TaskResult:
        plugin = self._task_registry.get(task_id)
        selection_model = model.filter_by_selection(selection)
        context = TaskContext(
            full_model=model.copy(), selection_model=selection_model, case_id=case_id
        )
        plugin.validate_input(context)

        return plugin.execute(context)


class ResultQueryService:
    def __init__(self, processor: ResultProcessor | None = None) -> None:
        self._processor = processor or ResultProcessor()

    def process(
        self,
        task_result: TaskResult,
        criteria: VisualizationCriteria,
        selection: SelectionContext,
    ) -> Result:
        model = ModelService().model
        return self._processor.process(task_result.results, selection, criteria, model)


class VisualizationService:
    def __init__(self, builder: SceneBuilder | None = None) -> None:
        self._builder = builder or SceneBuilder()

    def build_scene(self, model: FEMModel) -> dict[str, dict[str, dict[str, Any]]]:
        return self._builder.build_scene(model)

    def build_result_scene(
        self,
        model: FEMModel,
        results: Result,
        criteria: VisualizationCriteria,
        selection: SelectionContext,
    ) -> dict[str, Any]:
        return self._builder.build_result_scene(model, results, criteria, selection)


class ModelService:
    # Process-wide singleton holding the model currently loaded in the app session.
    _instance: ModelService | None = None

    def __new__(cls) -> ModelService:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.model = None
        return cls._instance

    model: FEMModel | None


class ApplicationContext:
    _instance: ApplicationContext | None = None

    def __new__(
        cls,
        model_service: ModelService | None = None,
        preferences: UserPreferencesService | None = None,
    ) -> ApplicationContext:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.model_service = model_service or ModelService()
            cls._instance.preferences = preferences or UserPreferencesService()
            cls._instance.task_registry = TaskRegistry()
            cls._instance.plugin_loader = PluginLoader(cls._instance.task_registry)
            cls._instance.load_plugins()
        return cls._instance

    model_service: ModelService
    preferences: UserPreferencesService
    task_registry: TaskRegistry
    plugin_loader: PluginLoader

    def load_plugins(self) -> list[str]:
        self.task_registry.clear_external()
        return self.plugin_loader.load_from(self.preferences.plugins_base_path)

    def add_plugins(self, files: list[str] | list[Path]) -> list[str]:
        if not Path(self.preferences.plugins_base_path).exists():
            Path(self.preferences.plugins_base_path).mkdir(parents=True, exist_ok=True)

        return self.plugin_loader.add_from(
            source_files=files,
            destiny_directory=self.preferences.plugins_base_path,
        )

    def get_task_identifiers(self) -> list[str]:
        return self.task_registry.get_task_identifiers()

    def get_load_cases(self) -> list[str]:
        model = self.model_service.model
        if model is None:
            return []
        cases = model.tables[rpr.ModelTables.LOAD_CASES][rpr.LoadCasesColumns.CASE]
        return list(dict.fromkeys(cases.astype(str)))
