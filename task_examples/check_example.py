from __future__ import annotations

from civil_3P.standard import model_components as mc
from civil_3P.standard import model_representation as rpr

from civil_3P.tasks.task_base import (
    TaskContext,
    TaskMetadata,
    TaskPlugin,
    TaskResult,
)


class ExampleBarCheckPlugin(TaskPlugin):
    @property
    def metadata(self) -> TaskMetadata:
        return TaskMetadata(identifier="example_bar_check",
                            display_name="Example Bar Check",
                            supported_element_type=mc.ModelComponents.ELEMENTS_1D)

    def validate_input(self,
                       context: TaskContext) -> None:
        if context.selection_model.tables[rpr.ModelTables.ELEMENTS_1D].empty:
            raise ValueError("No 1D elements selected for the task")

    def execute(self,
                context: TaskContext) -> TaskResult:
        result_df = context.full_model.tables[rpr.ModelTables.TASK_1D_RESULTS]
        my_df = context.full_model.tables[rpr.ModelTables.ORIGIN_1D_RESULTS]
        result_df[rpr.Task1DResultsColumns.ELEMENT] = my_df[rpr.Origin1DResultsColumns.ELEMENT]
        result_df[rpr.Task1DResultsColumns.CASE] = my_df[rpr.Origin1DResultsColumns.CASE]
        result_df[rpr.Task1DResultsColumns.STATION] = my_df[rpr.Origin1DResultsColumns.STATION]
        result_df[rpr.Task1DResultsColumns.VALUE] = my_df[rpr.Origin1DResultsColumns.BENDING_3]

        return TaskResult(metadata=self.metadata, results=result_df, report=result_df)
