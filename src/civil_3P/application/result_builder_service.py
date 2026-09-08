from __future__ import annotations

from typing import TYPE_CHECKING

from civil_3P.core.selection import SelectionContext
from civil_3P.tasks.task_base import TaskResult

if TYPE_CHECKING:
    from civil_3P.application.model_service import ModelService
    from civil_3P.core.result_builder import (
        ResultBuilder,
        Visualization2DMode,
    )
    from civil_3P.core.result_data import ResultData


class ResultBuilderService:
    def __init__(
        self,
        model_service: ModelService,
        processor: ResultBuilder,
    ) -> None:
        self._model_service = model_service
        self._processor = processor

    def process(
        self,
        task_result: TaskResult,
        criteria: Visualization2DMode,
        selection: SelectionContext,
    ) -> ResultData:
        return self._processor.process(
            task_result.results,
            selection,
            criteria,
            self._model_service.model,
        )
