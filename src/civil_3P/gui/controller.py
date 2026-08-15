from __future__ import annotations

from pathlib import Path
from typing import Protocol

import pandas as pd

from civil_3P.application.services import (
    ImportModelService,
    ResultQueryService,
    TaskExecutionService,
)
from civil_3P.standard import model_components as mc
from civil_3P.core.model import FEMModel
from civil_3P.core.results import ResultProcessor, VisualizationCriteria
from civil_3P.core.selection import SelectionContext
from civil_3P.importers.importer import ImporterProfile
from civil_3P.file_service.file_service import ModelArchiveService
from civil_3P.tasks.base import TaskResult
from civil_3P.tasks.registry import BuiltinTaskRegistry


class SupportsQtWindow(Protocol):
    def show(self) -> None: ...


class AppController:
    def __init__(
        self,
        import_service: ImportModelService | None = None,
        task_service: TaskExecutionService | None = None,
        result_service: ResultQueryService | None = None,
        task_registry: BuiltinTaskRegistry | None = None,
        archive_service: ModelArchiveService | None = None,
    ) -> None:
        self._import_service = import_service or ImportModelService()
        self._task_service = task_service or TaskExecutionService()
        self._result_service = result_service or ResultQueryService(
            processor=ResultProcessor()
        )
        self._task_registry = task_registry or BuiltinTaskRegistry()
        self._archive_service = archive_service or ModelArchiveService()

    def import_model(
        self,
        profile: ImporterProfile,
        directory: str | Path,
    ) -> FEMModel:
        return self._import_service.import_model(profile, directory)

    def create_selection(
        self,
        element_type: mc.ModelComponents,
        selected_element_ids: tuple[str, ...] | list[str],
        adjacent_element_ids: tuple[str, ...] | list[str] | None = None,
    ) -> SelectionContext:
        return SelectionContext(
            element_type=element_type,
            selected_element_ids=tuple(selected_element_ids),
            adjacent_element_ids=tuple(adjacent_element_ids or ()),
        )

    def execute_task(
        self,
        task_id: str,
        model: FEMModel,
        selection: SelectionContext,
        case_id: str,
    ) -> TaskResult:
        plugin = self._task_registry.get(task_id)
        return self._task_service.execute(plugin, model, selection, case_id)

    def build_result_view(
        self,
        selection: SelectionContext,
        criteria: VisualizationCriteria,
        task_result: TaskResult,
    ) -> pd.DataFrame:
        return self._result_service.process(task_result, criteria, selection)

    def save_model(
        self,
        model: FEMModel,
        path: str | Path,
    ) -> None:
        self._archive_service.save(model, path)

    def load_model_archive(
        self,
        path: str | Path,
    ) -> FEMModel:
        return self._archive_service.load(path)

    def create_main_window(self) -> SupportsQtWindow:
        try:
            from civil_3P.gui.main_window import MainWindow
        except ImportError as exc:  # pragma: no cover - exercised when Qt absent
            raise RuntimeError(
                "PySide6 is required to create the main window"
            ) from exc

        return MainWindow(controller=self)
