from __future__ import annotations

from civil_3P.standard import model_components as mc
from civil_3P.standard import model_representation as rpr

from civil_3P.tasks.task_base import (
    TaskContext,
    TaskMetadata,
    TaskPlugin,
    TaskResult,
)


class ExampleShellDesignPlugin(TaskPlugin):
    @property
    def metadata(self) -> TaskMetadata:
        return TaskMetadata(identifier="example_shell_design",
                            display_name="Example Shell Design",
                            supported_element_type=mc.ModelComponents.ELEMENTS_2D)

    def validate_input(self,
                       context: TaskContext) -> None:
        if context.selection_model.tables[rpr.ModelTables.ELEMENTS_2D].empty:
            raise ValueError("No 2D elements selected for the task")

    def execute(self,
                context: TaskContext) -> TaskResult:
        result_df = context.selection_model.tables[rpr.ModelTables.TASK_2D_RESULTS]
        my_df = context.selection_model.tables[rpr.ModelTables.ORIGIN_2D_RESULTS]
        result_df[rpr.Task2DResultsColumns.ELEMENT] = my_df[rpr.Origin2DResultsColumns.ELEMENT]
        result_df[rpr.Task2DResultsColumns.CASE] = my_df[rpr.Origin2DResultsColumns.CASE]
        result_df[rpr.Task2DResultsColumns.NODE] = my_df[rpr.Origin2DResultsColumns.NODE]
        result_df[rpr.Task2DResultsColumns.VALUE] = my_df[rpr.Origin2DResultsColumns.BENDING_22]

        return TaskResult(metadata=self.metadata, results=result_df, report=result_df)
