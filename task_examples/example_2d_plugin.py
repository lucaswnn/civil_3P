from __future__ import annotations

from typing import TYPE_CHECKING

import pandas as pd

from civil_3P.standard.model_components import ModelComponents as mc
from civil_3P.standard.model_repr import ModelTables as mt
from civil_3P.standard.model_repr import ShellResCols as rpr_shell_res
from civil_3P.standard.task_res_repr import TaskShellResCols as task_rpr_2d
from civil_3P.tasks.task_metadata import TaskMetadata
from civil_3P.tasks.task_plugin import TaskPlugin
from civil_3P.tasks.task_res import TaskRes

if TYPE_CHECKING:
    from civil_3P.tasks.task_input_context import TaskInputContext


class Example2DPlugin(TaskPlugin):
    @property
    def metadata(self) -> TaskMetadata:
        return TaskMetadata(
            identifier="example_2d",
            display_name="Example 2D task",
            supported_element_type=mc.SHELLS,
        )

    def validate_input(
        self,
        context: TaskInputContext,
    ) -> None:
        if context.selection_model.tables[mt.SHELLS].empty:
            raise ValueError("No 2D elements selected for the task")

    def execute(
        self,
        context: TaskInputContext,
    ) -> TaskRes:
        res_df = pd.DataFrame(
            columns=[
                task_rpr_2d.ELEMENT,
                task_rpr_2d.NODE,
                task_rpr_2d.VALUE,
            ]
        )
        case = context.case_id
        my_df = context.selection_model.tables[mt.SHELL_RESULTS]
        my_df = my_df[my_df[rpr_shell_res.CASE] == case]
        res_df[task_rpr_2d.ELEMENT] = my_df[rpr_shell_res.ELEMENT]
        res_df[task_rpr_2d.NODE] = my_df[rpr_shell_res.NODE]
        res_df[task_rpr_2d.VALUE] = my_df[rpr_shell_res.BENDING_22]

        return TaskRes(metadata=self.metadata, results=res_df)
