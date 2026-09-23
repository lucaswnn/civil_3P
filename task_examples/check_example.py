from __future__ import annotations

from civil_3P.standard.model_representation import ModelTables as mt
from civil_3P.standard.model_components import ModelComponents as mc
from civil_3P.standard.task_result_representation import (
    Task1DResultsColumns as task_rpr_1d,
)
from civil_3P.standard.model_representation import (
    Origin1DResultsColumns as rpr_origin_1d,
)

from civil_3P.tasks.task_base import (
    TaskInputContext,
    TaskMetadata,
    TaskPlugin,
    TaskResult,
)

import pandas as pd


class ExampleBarCheckPlugin(TaskPlugin):
    @property
    def metadata(self) -> TaskMetadata:
        return TaskMetadata(
            identifier="example_bar_check",
            display_name="Example Bar Check",
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
