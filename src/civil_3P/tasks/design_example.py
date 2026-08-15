from __future__ import annotations

import pandas as pd

from civil_3P.standard import model_components as mc
from civil_3P.standard.result_components import ResultLocation
from civil_3P.standard.task_components import TaskType

from civil_3P.tasks.base import (
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
                            task_type=TaskType.DESIGN,
                            supported_element_type=mc.ModelComponents.ELEMENTS_2D)

    def validate_input(self,
                       context: TaskContext) -> None:
        if context.selection.element_type != mc.ModelComponents.ELEMENTS_2D:
            raise ValueError(
                "ExampleShellDesignPlugin only supports 2D shells")

        if not context.selection.selected_element_ids:
            raise ValueError("Selection cannot be empty")

    def execute(self,
                context: TaskContext) -> TaskResult:
        property_map = context.model.property_map("element")
        base = context.model.origin_results_2d_df
        target_element_ids = context.selection.all_element_ids
        membrane = base[
            (base["case_id"] == context.case_id)
            & (base["result_name"] == "membrane_force")
            & (base["element_id"].isin(target_element_ids))
        ].copy()

        membrane["design_strength"] = membrane["element_id"].map(
            lambda element_id: float(property_map.get(
                (str(element_id), "design_strength"),
                1.0))
        )

        membrane["value"] = (membrane["value"].abs() /
                             membrane["design_strength"]).round(6)

        membrane["result_name"] = "required_thickness"
        membrane["location"] = ResultLocation.NODE.value
        report = (
            membrane[membrane["element_id"].isin(
                context.selection.selected_element_ids)]
            .groupby("element_id", as_index=False)["value"]
            .max()
            .rename(columns={"value": "required_thickness"})
        )

        return TaskResult(metadata=self.metadata, results=membrane, report=report)
