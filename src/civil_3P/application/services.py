from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from civil_3P.core.model import FEMModel
from civil_3P.core.results import ResultProcessor, VisualizationCriteria
from civil_3P.core.selection import SelectionContext
from civil_3P.importers.csv_importers import CsvImportProfile, ImporterRegistry
from civil_3P.tasks.base import TaskContext, TaskPlugin, TaskResult


class ImportModelService:
    def __init__(self, registry: ImporterRegistry | None = None) -> None:
        self._registry = registry or ImporterRegistry()

    def import_model(self, profile: CsvImportProfile, directory: str | Path) -> FEMModel:
        return self._registry.import_model(profile, directory)


class TaskExecutionService:
    def execute(self, plugin: TaskPlugin, model: FEMModel, selection: SelectionContext, case_id: str) -> TaskResult:
        context = TaskContext(
            model=model, selection=selection, case_id=case_id)
        plugin.validate_input(context)
        return plugin.execute(context)


class ResultQueryService:
    def __init__(self, processor: ResultProcessor | None = None) -> None:
        self._processor = processor or ResultProcessor()

    def process(self, task_result: TaskResult, criteria: VisualizationCriteria, selection: SelectionContext) -> pd.DataFrame:
        return self._processor.process(task_result.results, selection, criteria)
