from typing import Any

from civil_3P.application.application_context import ApplicationContext
from civil_3P.application.result_builder_service import ResultService
from civil_3P.application.task_service import TaskService
from civil_3P.application.view_builder_service import ViewBuilderService
from civil_3P.application.model_service import ModelService
from civil_3P.core.model import FEMModel
from civil_3P.core.result_builder import ResultBuilder, Visualization2DMode
from civil_3P.core.selection import SelectionContext
from civil_3P.standard import model_components as mc
from civil_3P.tasks.task_base import TaskResult


class TaskMenuController:
    def __init__(
        self,
        result_service: ResultService,
        visualization_service: ViewBuilderService,
        context: ApplicationContext,
    ) -> None:
        self._context = context
        self._result_service = result_service
        self._visualization_service = visualization_service

    @property
    def current_model(self) -> FEMModel | None:
        return self._context.get_model()

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
        selection: SelectionContext,
        case_id: str,
    ) -> TaskResult:
        return self._context.execute_task(
            task_id,
            selection,
            case_id,
        )

    def build_result_scene(
        self,
        selection: SelectionContext,
        criteria: Visualization2DMode,
        task_result: TaskResult,
    ) -> dict[str, Any]:
        result = self._result_service.process(
            task_result,
            criteria,
            selection,
        )
        model = self._context.get_model()

        return self._visualization_service.build_result_scene(
            model,
            result,
            criteria,
            selection,
        )

    def get_task_identifiers(self) -> list[str]:
        return self._context.get_task_identifiers()

    def get_load_case_ids(self) -> list[str]:
        return self._context.get_load_cases()
