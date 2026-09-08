from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

import pandas as pd

from civil_3P.standard import model_components as mc
from civil_3P.standard import task_result_representation as rpr_task
from civil_3P.core.model import FEMModel
from civil_3P.utils.pandas_utils import PandasUtils


@dataclass(frozen=True, slots=True)
class TaskMetadata:
    identifier: str
    display_name: str
    supported_element_type: mc.ModelComponents
    version: str = "0.1.0"


@dataclass(frozen=True, slots=True)
class TaskInputContext:
    full_model: FEMModel
    selection_model: FEMModel
    case_id: str


@dataclass(frozen=True, slots=True)
class TaskResult:
    metadata: TaskMetadata
    results: pd.DataFrame


class TaskPlugin(ABC):
    @property
    @abstractmethod
    def metadata(self) -> TaskMetadata:
        raise NotImplementedError

    def supports(self,
                 element_type: mc.ModelComponents) -> bool:
        return self.metadata.supported_element_type == element_type

    @abstractmethod
    def validate_input(self,
                       context: TaskInputContext) -> None:
        raise NotImplementedError

    @abstractmethod
    def execute(
        self,
        context: TaskInputContext,
    ) -> TaskResult:
        raise NotImplementedError

    def validade_output(self, result: TaskResult) -> None:
        if self.supports(mc.ModelComponents.NODES):
            PandasUtils.ensure_columns(
                result.results,
                [
                    rpr_task.TaskNodeResultsColumns.NODE,
                    rpr_task.TaskNodeResultsColumns.CASE,
                    rpr_task.TaskNodeResultsColumns.VALUE,
                ],
            )

        elif self.supports(mc.ModelComponents.ELEMENTS_1D):
            PandasUtils.ensure_columns(
                result.results,
                [
                    rpr_task.Task1DResultsColumns.ELEMENT,
                    rpr_task.Task1DResultsColumns.STATION,
                    rpr_task.Task1DResultsColumns.CASE,
                    rpr_task.Task1DResultsColumns.VALUE,
                ],
            )

        elif self.supports(mc.ModelComponents.ELEMENTS_2D):
            PandasUtils.ensure_columns(
                result.results,
                [
                    rpr_task.Task2DResultsColumns.ELEMENT,
                    rpr_task.Task2DResultsColumns.NODE,
                    rpr_task.Task2DResultsColumns.CASE,
                    rpr_task.Task2DResultsColumns.VALUE,
                ],
            )

        else:
            raise ValueError(
                "Unsupported element type for task result validation")

    def get_task_result(
        self,
        context: TaskInputContext,
    ) -> TaskResult:
        result = self.execute(context)
        self.validade_output(result)
        return result
