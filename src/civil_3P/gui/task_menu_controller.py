from typing import Any

from civil_3P.application.services import ResultQueryService, TaskExecutionService, VisualizationService, ModelService, ApplicationContext
from civil_3P.core.model import FEMModel
from civil_3P.core.results import ResultProcessor, VisualizationCriteria
from civil_3P.core.selection import SelectionContext
from civil_3P.standard import model_components as mc
from civil_3P.tasks.task_base import TaskResult


class TaskMenuController:
    def __init__(
        self,
        task_service: TaskExecutionService | None = None,
        result_service: ResultQueryService | None = None,
        visualization_service: VisualizationService | None = None,
        session: ModelService | None = None,
        context: ApplicationContext | None = None,
    ) -> None:
        self._context = context or ApplicationContext()
        self._task_service = task_service or TaskExecutionService(
            context=self._context)
        self._result_service = result_service or ResultQueryService(
            processor=ResultProcessor()
        )
        self._visualization_service = visualization_service or VisualizationService()
        self._session = session or self._context.model_service

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

    def build_result_scene(
        self,
        selection: SelectionContext,
        criteria: VisualizationCriteria,
        task_result: TaskResult,
    ) -> dict[str, Any]:
        result = self._result_service.process(
            task_result, criteria, selection)
        return self._visualization_service.build_result_scene(
            self._session.model,
            result,
            criteria,
            selection,
        )

    def get_task_identifiers(self) -> list[str]:
        return self._context.get_task_identifiers()

    def get_load_case_ids(self) -> list[str]:
        return self._context.get_load_cases()
