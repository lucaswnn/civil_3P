from __future__ import annotations

from civil_3P.standard.model_components import ModelComponents as mc
from civil_3P.standard.model_representation import (
    Origin2DResultsColumns as rpr_origin_2d,
)
from civil_3P.standard.model_representation import ModelTables as mt
from civil_3P.standard.task_result_representation import (
    Task2DResultsColumns as task_rpr_2d,
)
from civil_3P.tasks.task_base import (
    TaskInputContext,
    TaskMetadata,
    TaskPlugin,
    TaskResult,
)

import pandas as pd


class ExampleShellDesignPlugin(TaskPlugin):
    @property
    def metadata(self) -> TaskMetadata:
        return TaskMetadata(
            identifier="example_shell_design",
            display_name="Example Shell Design",
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
