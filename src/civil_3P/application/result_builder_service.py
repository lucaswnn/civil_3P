from __future__ import annotations

from typing import TYPE_CHECKING

from civil_3P.core.selection import SelectionContext
from civil_3P.tasks.task_base import TaskResult

if TYPE_CHECKING:
    from civil_3P.application.model_service import ModelService
    from civil_3P.core.result_builder import (
        ResultBuilder,
        ResultVisualization2DCriteria,
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
        selection: SelectionContext,
        criteria: ResultVisualization2DCriteria | None = None,
    ) -> ResultData:
        model = self._model_service.get_model()
        if model is None:
            raise ValueError("Cannot process results without a model")

        return self._processor.process(
            task_result,
            selection,
            model,
            visual_2d_criteria=criteria,
        )
