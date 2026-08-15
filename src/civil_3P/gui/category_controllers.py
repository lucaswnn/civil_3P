from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from civil_3P.application.services import (
    ImportModelService,
    ModelService,
    ResultQueryService,
    TaskExecutionService,
    VisualizationService,
)
from civil_3P.core.model import FEMModel
from civil_3P.core.results import ResultProcessor, VisualizationCriteria
from civil_3P.core.selection import SelectionContext
from civil_3P.file_service.file_service import FileService
from civil_3P.standard import model_components as mc
from civil_3P.standard.importer_profiles import ImporterProfiles
from civil_3P.tasks.task_base import TaskResult


class FileMenuController:
    def __init__(
        self,
        import_model_service: ImportModelService | None = None,
        file_service: FileService | None = None,
        visualization_service: VisualizationService | None = None,
        model_service: ModelService | None = None,
    ) -> None:
        self._import_service = import_model_service or ImportModelService()
        self._file_service = file_service or FileService()
        self._visualization_service = visualization_service or VisualizationService()
        self._model_service = model_service or ModelService()

    @property
    def current_model(self) -> FEMModel | None:
        return self._model_service.model

    def import_model(
        self,
        profile: ImporterProfiles,
        directory: str | Path,
    ) -> FEMModel:
        model = self._import_service.import_model(profile, directory)
        self._model_service.model = model
        return model

    def load_model_file(self, path: str | Path) -> FEMModel:
        model = self._file_service.load(path)
        self._model_service.model = model
        return model

    def save_model(self, model: FEMModel, path: str | Path) -> None:
        self._file_service.save(model, path)

    def build_scene(self, model: FEMModel) -> dict[str, Any]:
        return self._visualization_service.build_scene(model)


class TarefasController:
    def __init__(
        self,
        task_service: TaskExecutionService | None = None,
        result_service: ResultQueryService | None = None,
        session: ModelService | None = None,
    ) -> None:
        self._task_service = task_service or TaskExecutionService()
        self._result_service = result_service or ResultQueryService(
            processor=ResultProcessor()
        )
        self._session = session or ModelService()

    @property
    def current_model(self) -> FEMModel | None:
        return self._session.model

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
        return self._task_service.execute(task_id, model, selection, case_id)

    def build_result_view(
        self,
        selection: SelectionContext,
        criteria: VisualizationCriteria,
        task_result: TaskResult,
    ) -> pd.DataFrame:
        return self._result_service.process(task_result, criteria, selection)
