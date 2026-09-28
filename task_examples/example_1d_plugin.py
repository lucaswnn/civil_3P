from __future__ import annotations

from typing import TYPE_CHECKING

import pandas as pd

from civil_3P.standard.model_components import ModelComponents as mc
from civil_3P.standard.model_repr import BarResCols as rpr_bar_res
from civil_3P.standard.model_repr import ModelTables as mt
from civil_3P.standard.task_res_repr import TaskBarResCols as task_rpr_1d
from civil_3P.tasks.task_metadata import TaskMetadata
from civil_3P.tasks.task_plugin import TaskPlugin
from civil_3P.tasks.task_res import TaskRes

if TYPE_CHECKING:
    from civil_3P.tasks.task_input_context import TaskInputContext


class Example1DPlugin(TaskPlugin):
    @property
    def metadata(self) -> TaskMetadata:
        return TaskMetadata(
            identifier="example_1d",
            display_name="Example 1D task",
            supported_element_type=mc.BARS,
        )

    def validate_input(self, context: TaskInputContext) -> None:
        if context.selection_model.tables[mt.BARS].empty:
            raise ValueError("No 1D elements selected for the task")

    def execute(
        self,
        context: TaskInputContext,
    ) -> TaskRes:
        res_df = pd.DataFrame(
            columns=[
                task_rpr_1d.ELEMENT,
                task_rpr_1d.STATION,
                task_rpr_1d.VALUE,
            ]
        )
        case = context.case_id
        my_df = context.selection_model.tables[mt.BAR_RESULTS]
        my_df = my_df[my_df[rpr_bar_res.CASE] == case]
        res_df[task_rpr_1d.ELEMENT] = my_df[rpr_bar_res.ELEMENT]
        res_df[task_rpr_1d.STATION] = my_df[rpr_bar_res.STATION]
        res_df[task_rpr_1d.VALUE] = my_df[rpr_bar_res.BENDING_3]

        return TaskRes(metadata=self.metadata, results=res_df)
