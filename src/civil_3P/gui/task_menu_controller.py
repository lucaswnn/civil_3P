from __future__ import annotations

from typing import TYPE_CHECKING

from civil_3P.core.sel_context import SelContext
from civil_3P.standard.model_components import ModelComponents as mc

if TYPE_CHECKING:
    from civil_3P.app.model_service import ModelService
    from civil_3P.app.res_builder_service import ResBuilderService
    from civil_3P.app.task_service import TaskService
    from civil_3P.app.view_builder_service import ViewBuilderService
    from civil_3P.gui.scene_widget_controller import SceneWidgetController
    from civil_3P.standard.res_components import ResSceneKind
    from civil_3P.tasks.task_res import TaskRes


class TaskMenuController:
    def __init__(
        self,
        task_service: TaskService,
        res_builder_service: ResBuilderService,
        view_builder_service: ViewBuilderService,
        model_service: ModelService,
        scene_widget_controller: SceneWidgetController,
    ) -> None:
        self._task_service = task_service
        self._res_builder_service = res_builder_service
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
    ) -> SelContext:
        selected = set(map(str, selected_element_ids))
        adjacent = set(map(str, adjacent_element_ids or ()))

        return SelContext(
            node_ids=selected if element_type == mc.NODES else set(),
            bar_ids=selected if element_type == mc.BARS else set(),
            shell_ids=selected if element_type == mc.SHELLS else set(),
            adjacent_shell_ids=adjacent,
        )

    def execute_task(
        self,
        task_id: str,
        selection: SelContext,
        case_id: str,
    ) -> TaskRes:
        model = self.current_model

        if model is None:
            raise ValueError("Cannot execute a task without a model")

        return self._task_service.execute_task(
            task_id,
            model,
            selection,
            case_id,
        )

    def set_res_scene(
        self,
        selection: SelContext,
        task_result: TaskRes,
        view_content_kind: ResSceneKind,
    ) -> None:
        model = self.current_model

        if model is None:
            raise ValueError("Cannot build a result scene without a model")

        result = self._res_builder_service.build_res_data(
            task_result=task_result,
            selection=selection,
            view_content_kind=view_content_kind,
        )

        scene = self._view_builder_service.build_res_scene(
            results=result,
            view_content_kind=view_content_kind,
            model=model,
        )
        self._scene_widget_controller.set_res_scene(scene)

    def get_task_identifiers(self) -> list[str]:
        return self._task_service.get_task_identifiers()

    def get_load_case_ids(self) -> list[str]:
        return self._model_service.get_load_cases()
