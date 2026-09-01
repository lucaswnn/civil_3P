from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from civil_3P.core.selection import SelectionContext
from civil_3P.standard import model_components as mc
from civil_3P.standard.result_components import (
    VisualizationMode,
    ResultLocation,
    Result
)
from civil_3P.standard import model_representation as rpr


@dataclass(frozen=True, slots=True)
class ResultAveragingPolicy:
    include_adjacent_for_2d_average: bool = True

    def target_element_ids(self, selection: SelectionContext) -> tuple[str, ...]:
        if selection.element_type != mc.ModelComponents.ELEMENTS_2D:
            return selection.selected_element_ids

        if self.include_adjacent_for_2d_average:
            return selection.all_element_ids

        return selection.selected_element_ids


@dataclass(frozen=True, slots=True)
class VisualizationCriteria:
    result_name: str
    case_id: str
    mode: VisualizationMode
    averaging_policy: ResultAveragingPolicy = ResultAveragingPolicy()



class ResultProcessor:
    def process(
        self,
        task_results: pd.DataFrame,
        selection: SelectionContext,
        criteria: VisualizationCriteria,
    ) -> Result:
        if selection.element_type == mc.ModelComponents.ELEMENTS_1D:
            return self._process_1d(task_results, criteria)
        elif selection.element_type == mc.ModelComponents.ELEMENTS_2D:
            return self._process_2d(task_results, criteria)
        elif selection.element_type == mc.ModelComponents.NODES:
            return self._process_node(task_results, criteria)

        raise ValueError(f"Unsupported element type: {selection.element_type}")

    def _process_1d(
        self,
        results: pd.DataFrame,
        criteria: VisualizationCriteria,
    ) -> Result:
        return Result(
            result_df=results,
            elements=set(results[rpr.Task1DResultsColumns.ELEMENT].to_list()),
        )

    def _process_node(
        self,
        results: pd.DataFrame,
        criteria: VisualizationCriteria,
    ) -> Result:
        return Result(
            result_df=results,
            elements=set(results[rpr.TaskNodeResultsColumns.NODE].to_list()),
        )

    def _process_2d(
        self,
        results: pd.DataFrame,
        criteria: VisualizationCriteria,
    ) -> Result:
        if criteria.mode == VisualizationMode.ELEMENT:
            return Result(
                result_df=results.groupby(
                    [
                        rpr.Task2DResultsColumns.ELEMENT,
                    ],
                    as_index=False,
                )[rpr.Task2DResultsColumns.VALUE]
                .mean()
                .assign(location=ResultLocation.ELEMENT.value),
                elements=set(results[rpr.Task2DResultsColumns.ELEMENT].to_list()),
            )

        if criteria.mode == VisualizationMode.NODE_RAW:
            return Result(
                result_df=results,
                elements=set(results[rpr.Task2DResultsColumns.ELEMENT].to_list()),
            )

        averaged = (
            results.groupby(
                [
                    rpr.Task2DResultsColumns.CASE,
                    rpr.Task2DResultsColumns.NODE,
                ],
                as_index=False,
            )[rpr.Task2DResultsColumns.VALUE]
            .mean()
            .assign(location=ResultLocation.NODE.value)
        )

        return Result(
            result_df=averaged,
            elements=set(results[rpr.Task2DResultsColumns.ELEMENT].to_list()),
        )
