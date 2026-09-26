from __future__ import annotations

from typing import TYPE_CHECKING

from civil_3P.core.selection_context import SelectionContext
from civil_3P.standard.model_components import ModelComponents as mc

if TYPE_CHECKING:
    from civil_3P.application.model_service import ModelService
    from civil_3P.application.result_builder_service import ResultBuilderService
    from civil_3P.application.task_service import TaskService
    from civil_3P.application.view_builder_service import ViewBuilderService
    from civil_3P.gui.scene_widget_controller import SceneWidgetController
    from civil_3P.standard.result_components import ViewContentKind
    from civil_3P.tasks.task_result import TaskResult


class TaskMenuController:
    def __init__(
        self,
        task_service: TaskService,
        result_builder_service: ResultBuilderService,
        view_builder_service: ViewBuilderService,
        model_service: ModelService,
        scene_widget_controller: SceneWidgetController,
    ) -> None:
        self._task_service = task_service
        self._result_builder_service = result_builder_service
        self._view_builder_service = view_builder_service
        self._model_service = model_service
        self._scene_widget_controller = scene_widget_controller

    @property
    def current_model(self):
        return self._model_service.get_model()

    def create_selection(
        self,
        element_type: mc.ModelComponents,
        selected_element_ids: list[str],
        adjacent_element_ids: list[str] | None = None,
    ) -> SelectionContext:
        selected = set(map(str, selected_element_ids))
        adjacent = set(map(str, adjacent_element_ids or ()))

        return SelectionContext(
            node_ids=selected if element_type == mc.NODES else set(),
            element_1d_ids=selected if element_type == mc.ELEMENTS_1D else set(),
            element_2d_ids=selected if element_type == mc.ELEMENTS_2D else set(),
            adjacent_element_2d_ids=adjacent,
        )

    def execute_task(
        self,
        task_id: str,
        selection: SelectionContext,
        case_id: str,
    ) -> TaskResult:
        model = self.current_model

        if model is None:
            raise ValueError("Cannot execute a task without a model")

        return self._task_service.execute_task(
            task_id,
            model,
            selection,
            case_id,
        )

    def set_result_scene(
        self,
        selection: SelectionContext,
        task_result: TaskResult,
        view_content_kind: ViewContentKind,
    ) -> None:
        model = self.current_model

        if model is None:
            raise ValueError("Cannot build a result scene without a model")

        result = self._result_builder_service.build_result_data(
            task_result=task_result,
            selection=selection,
            view_content_kind=view_content_kind,
        )

        scene = self._view_builder_service.build_result_scene(
            results=result,
            view_content_kind=view_content_kind,
            model=model,
        )
        self._scene_widget_controller.set_result_scene(scene)

    def get_task_identifiers(self) -> list[str]:
        return self._task_service.get_task_identifiers()

    def get_load_case_ids(self) -> list[str]:
        return self._model_service.get_load_cases()
