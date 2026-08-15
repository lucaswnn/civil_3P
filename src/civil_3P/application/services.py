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
from civil_3P.tasks.task_base import TaskContext, TaskPlugin, TaskResult
from civil_3P.visualization.scene_builder import SceneBuilder
from civil_3P.standard.importer_profiles import ImporterProfiles


class ImportModelService:
    def __init__(self, registry: ImporterRegistry | None = None) -> None:
        self._registry = registry or ImporterRegistry()

    def import_model(self,
                     profile: ImporterProfiles,
                     directory: str | Path) -> FEMModel:
        return self._registry.import_model(profile, directory)


class TaskExecutionService:
    def __init__(self, task_registry: TaskRegistry | None = None) -> None:
        self._task_registry = task_registry or TaskRegistry()

    def execute(self,
                task_id: str,
                model: FEMModel,
                selection: SelectionContext,
                case_id: str) -> TaskResult:
        plugin = self._task_registry.get(task_id)
        context = TaskContext(model=model,
                              selection=selection,
                              case_id=case_id)
        plugin.validate_input(context)

        return plugin.execute(context)


class ResultQueryService:
    def __init__(self,
                 processor: ResultProcessor | None = None) -> None:
        self._processor = processor or ResultProcessor()

    def process(self,
                task_result: TaskResult,
                criteria: VisualizationCriteria,
                selection: SelectionContext) -> pd.DataFrame:
        return self._processor.process(task_result.results, selection, criteria)


class VisualizationService:
    def __init__(self, builder: SceneBuilder | None = None) -> None:
        self._builder = builder or SceneBuilder()

    def build_scene(self, model: FEMModel) -> dict[str, dict[str, dict[str, Any]]]:
        return self._builder.build_scene(model)


class ModelService:
    # Process-wide singleton holding the model currently loaded in the app session.
    _instance: ModelService | None = None

    def __new__(cls) -> ModelService:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.model = None
        return cls._instance

    model: FEMModel | None
