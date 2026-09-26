from __future__ import annotations

from typing import TYPE_CHECKING

import pandas as pd

from civil_3P.standard.model_components import ModelComponents as mc
from civil_3P.standard.model_representation import (
    ModelTables as mt,
    Origin2DResultsColumns as rpr_origin_2d,
)
from civil_3P.standard.task_result_representation import (
    Task2DResultsColumns as task_rpr_2d
)
from civil_3P.tasks.task_metadata import TaskMetadata
from civil_3P.tasks.task_plugin import TaskPlugin
from civil_3P.tasks.task_result import TaskResult

if TYPE_CHECKING:
    from civil_3P.tasks.task_input_context import TaskInputContext


class Example2DPlugin(TaskPlugin):
    @property
    def metadata(self) -> TaskMetadata:
        return TaskMetadata(
            identifier="example_2d",
            display_name="Example 2D task",
            supported_element_type=mc.ELEMENTS_2D,
        )

    def validate_input(
        self,
        context: TaskInputContext,
    ) -> None:
        if context.selection_model.tables[mt.ELEMENTS_2D].empty:
            raise ValueError("No 2D elements selected for the task")

    def execute(
        self,
        context: TaskInputContext,
    ) -> TaskResult:
        result_df = pd.DataFrame(
            columns=[
                task_rpr_2d.ELEMENT,
                task_rpr_2d.NODE,
                task_rpr_2d.VALUE,
            ]
        )
        case = context.case_id
        my_df = context.selection_model.tables[mt.ORIGIN_2D_RESULTS]
        my_df = my_df[my_df[rpr_origin_2d.CASE] == case]
        result_df[task_rpr_2d.ELEMENT] = my_df[rpr_origin_2d.ELEMENT]
        result_df[task_rpr_2d.NODE] = my_df[rpr_origin_2d.NODE]
        result_df[task_rpr_2d.VALUE] = my_df[rpr_origin_2d.BENDING_22]

        return TaskResult(metadata=self.metadata, results=result_df)
