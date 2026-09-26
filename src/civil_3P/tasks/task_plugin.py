from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from civil_3P.standard.model_components import ModelComponents as mc
from civil_3P.standard.task_result_representation import (
    TaskNodeResultsColumns as task_rpr_node,
    Task1DResultsColumns as task_rpr_1d,
    Task2DResultsColumns as task_rpr_2d,
)
from civil_3P.utils.pandas_utils import PandasUtils

if TYPE_CHECKING:
    from civil_3P.tasks.task_input_context import TaskInputContext
    from civil_3P.tasks.task_metadata import TaskMetadata
    from civil_3P.tasks.task_result import TaskResult


class TaskPlugin(ABC):
    @property
    @abstractmethod
    def metadata(self) -> TaskMetadata:
        raise NotImplementedError

    def supports(
        self,
        element_type: mc,
    ) -> bool:
        return self.metadata.supported_element_type == element_type

    @abstractmethod
    def validate_input(
        self,
        context: TaskInputContext,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def execute(
        self,
        context: TaskInputContext,
    ) -> TaskResult:
        raise NotImplementedError

    def validate_output(self, result: TaskResult) -> None:
        if self.supports(mc.NODES):
            PandasUtils.ensure_strict_columns(
                result.results,
                {
                    task_rpr_node.NODE,
                    task_rpr_node.VALUE,
                },
            )

        elif self.supports(mc.ELEMENTS_1D):
            PandasUtils.ensure_strict_columns(
                result.results,
                {
                    task_rpr_1d.ELEMENT,
                    task_rpr_1d.STATION,
                    task_rpr_1d.VALUE,
                },
            )

        elif self.supports(mc.ELEMENTS_2D):
            PandasUtils.ensure_strict_columns(
                result.results,
                {
                    task_rpr_2d.ELEMENT,
                    task_rpr_2d.NODE,
                    task_rpr_2d.VALUE,
                },
            )

        else:
            raise ValueError(
                "Unsupported element type for task result validation")

    def get_task_result(
        self,
        context: TaskInputContext,
    ) -> TaskResult:
        result = self.execute(context)
        self.validate_output(result)
        return result
