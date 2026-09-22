from __future__ import annotations

from civil_3P.application.model_service import ModelService
from civil_3P.application.result_builder_service import ResultBuilderService
from civil_3P.application.task_service import TaskService
from civil_3P.application.view_builder_service import ViewBuilderService
from civil_3P.core.result_builder import ResultVisualization2DCriteria
from civil_3P.core.selection import SelectionContext
from civil_3P.standard.model_components import ModelComponents as mc
from civil_3P.tasks.task_base import TaskResult


class TaskMenuController:
    def __init__(
        self,
        task_service: TaskService,
        result_builder_service: ResultBuilderService,
        view_builder_service: ViewBuilderService,
        model_service: ModelService,
        listeners=None,
    ) -> None:
        self._task_service = task_service
        self._result_builder_service = result_builder_service
        self._view_builder_service = view_builder_service
        self._model_service = model_service
        self._listeners = listeners or []

    @property
    def current_model(self):
        return self._model_service.get_model()

    def create_selection(
        self,
        element_type: mc.ModelComponents,
        selected_element_ids: tuple[str, ...] | list[str],
        adjacent_element_ids: tuple[str, ...] | list[str] | None = None,
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
        return self._task_service.execute_task(task_id, model, selection, case_id)

    def build_result_scene(
        self,
        selection: SelectionContext,
        task_result: TaskResult,
        criteria: ResultVisualization2DCriteria | None = None,
    ):
        model = self.current_model
        if model is None:
            raise ValueError("Cannot build a result scene without a model")
        result = self._result_builder_service.process(
            task_result,
            selection,
            criteria,
        )
        return self._view_builder_service.build_result_scene(model, result, criteria)

    def get_task_identifiers(self) -> list[str]:
        return self._task_service.get_task_identifiers()

    def get_load_case_ids(self) -> list[str]:
        return self._model_service.get_load_cases()
