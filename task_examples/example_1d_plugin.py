from __future__ import annotations

from typing import TYPE_CHECKING

import pandas as pd

from civil_3P.standard.model_components import ModelComponents as mc
from civil_3P.standard.model_representation import (
    ModelTables as mt,
    Origin1DResultsColumns as rpr_origin_1d,
)
from civil_3P.standard.task_result_representation import (
    Task1DResultsColumns as task_rpr_1d
)
from civil_3P.tasks.task_metadata import TaskMetadata
from civil_3P.tasks.task_plugin import TaskPlugin
from civil_3P.tasks.task_result import TaskResult

if TYPE_CHECKING:
    from civil_3P.tasks.task_input_context import TaskInputContext


class Example1DPlugin(TaskPlugin):
    @property
    def metadata(self) -> TaskMetadata:
        return TaskMetadata(
            identifier="example_1d",
            display_name="Example 1D task",
            supported_element_type=mc.ELEMENTS_1D,
        )

    def validate_input(self, context: TaskInputContext) -> None:
        if context.selection_model.tables[mt.ELEMENTS_1D].empty:
            raise ValueError("No 1D elements selected for the task")

    def execute(
        self,
        context: TaskInputContext,
    ) -> TaskResult:
        result_df = pd.DataFrame(
            columns=[
                task_rpr_1d.ELEMENT,
                task_rpr_1d.STATION,
                task_rpr_1d.VALUE,
            ]
        )
        case = context.case_id
        my_df = context.selection_model.tables[mt.ORIGIN_1D_RESULTS]
        my_df = my_df[my_df[rpr_origin_1d.CASE] == case]
        result_df[task_rpr_1d.ELEMENT] = my_df[rpr_origin_1d.ELEMENT]
        result_df[task_rpr_1d.STATION] = my_df[rpr_origin_1d.STATION]
        result_df[task_rpr_1d.VALUE] = my_df[rpr_origin_1d.BENDING_3]

        return TaskResult(metadata=self.metadata, results=result_df)
