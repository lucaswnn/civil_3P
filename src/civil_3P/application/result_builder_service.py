from __future__ import annotations

from typing import TYPE_CHECKING

from civil_3P.core.selection import SelectionContext
from civil_3P.tasks.task_base import TaskResult

if TYPE_CHECKING:
    from civil_3P.application.model_service import ModelService
    from civil_3P.standard.result_components import ViewContentKind
    from civil_3P.core.result_data import ResultData
    from civil_3P.core.result_builder_registry import ResultBuilderRegistry


class ResultBuilderService:
    _instance: ResultBuilderService | None = None

    def __new__(
        cls,
        model_service: ModelService,
        result_builder_registry: ResultBuilderRegistry,
    ) -> ResultBuilderService:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._model_service = model_service
            cls._instance._registry = result_builder_registry
        return cls._instance

    _registry: ResultBuilderRegistry
    _model_service: ModelService

    def build_result_data(
        self,
        task_result: TaskResult,
        selection: SelectionContext,
        view_content_kind: ViewContentKind,
    ) -> ResultData:
        model = self._model_service.get_model()
        if model is None:
            raise ValueError("Cannot process results without a model")

        return self._registry.build_result(
            task_result=task_result,
            selection=selection,
            model=model,
            view_content_kind=view_content_kind,
        )
