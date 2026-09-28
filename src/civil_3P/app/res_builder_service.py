from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from civil_3P.app.model_service import ModelService
    from civil_3P.core.res_builder_registry import ResBuilderRegistry
    from civil_3P.core.res_data import ResData
    from civil_3P.core.sel_context import SelContext
    from civil_3P.standard.res_components import ResSceneKind
    from civil_3P.tasks.task_res import TaskRes


class ResBuilderService:
    _instance: ResBuilderService | None = None

    def __new__(
        cls,
        model_service: ModelService,
        res_builder_registry: ResBuilderRegistry,
    ) -> ResBuilderService:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._model_service = model_service
            cls._instance._registry = res_builder_registry

        return cls._instance

    _registry: ResBuilderRegistry
    _model_service: ModelService

    def build_res_data(
        self,
        task_result: TaskRes,
        selection: SelContext,
        view_content_kind: ResSceneKind,
    ) -> ResData:
        model = self._model_service.get_model()

        if model is None:
            raise ValueError("Cannot process results without a model")

        return self._registry.build_result(
            task_result=task_result,
            selection=selection,
            model=model,
            view_content_kind=view_content_kind,
        )
