from __future__ import annotations

import pandas as pd

from civil_3P.core.enums import (
    ElementType,
    ResultLocation,
    TaskType,
)

from civil_3P.tasks.base import (
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
                            task_type=TaskType.CHECK,
                            supported_element_type=ElementType.BAR_1D)

    def validate_input(self,
                       context: TaskContext) -> None:
        if context.selection.element_type != ElementType.BAR_1D:
            raise ValueError("ExampleBarCheckPlugin only supports 1D bars")

        if not context.selection.selected_element_ids:
            raise ValueError("Selection cannot be empty")

    def execute(self,
                context: TaskContext) -> TaskResult:
        property_map = context.model.property_map("element")
        base = context.model.results
        axial = base[
            (base["case_id"] == context.case_id)
            & (base["result_name"] == "axial_force")
            & (base["element_id"].isin(context.selection.selected_element_ids))
        ].copy()

        axial["capacity"] = axial["element_id"].map(
            lambda element_id: float(property_map.get(
                (str(element_id), "axial_capacity"),
                1.0))
        )

        axial["value"] = (axial["value"].abs() / axial["capacity"]).round(6)
        axial["result_name"] = "utilization"
        axial["location"] = ResultLocation.ELEMENT.value
        report = (
            axial.groupby("element_id", as_index=False)["value"]
            .max()
            .rename(columns={"value": "max_utilization"})
        )
        
        return TaskResult(metadata=self.metadata, results=axial, report=report)
