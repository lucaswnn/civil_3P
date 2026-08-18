from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from civil_3P.core.selection import SelectionContext
from civil_3P.standard import model_components as mc
from civil_3P.standard import model_representation as rpr
from civil_3P.standard.result_components import (
    VisualizationMode,
    ResultLocation,
)


@dataclass(frozen=True, slots=True)
class ResultAveragingPolicy:
    include_adjacent_for_2d_average: bool = True

    def target_element_ids(self,
                           selection: SelectionContext) -> tuple[str, ...]:
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
    def process(self,
                task_results: pd.DataFrame,
                selection: SelectionContext,
                criteria: VisualizationCriteria) -> pd.DataFrame:
        filtered = task_results[
            (task_results["result_name"] == criteria.result_name)
            & (task_results["case_id"] == criteria.case_id)
            & (task_results["element_type"] == selection.element_type.value)
            & (task_results["element_id"].isin(selection.all_element_ids))
        ].copy()

        if filtered.empty:
            return filtered

        if selection.element_type == mc.ModelComponents.ELEMENTS_1D:
            return self._process_1d(filtered, selection)

        return self._process_2d(filtered, selection, criteria)

    def _process_1d(self,
                    results: pd.DataFrame,
                    selection: SelectionContext) -> pd.DataFrame:
        filtered = results[results["element_id"].isin(
            selection.selected_element_ids)].copy()

        aggregated = (
            filtered.groupby([
                "case_id",
                "result_name",
                "element_id",
            ],
                as_index=False)["value"]
            .max()
            .assign(location=ResultLocation.ELEMENT.value)
        )

        return aggregated

    def _process_2d(
        self,
        results: pd.DataFrame,
        selection: SelectionContext,
        criteria: VisualizationCriteria,
    ) -> pd.DataFrame:
        if criteria.mode == VisualizationMode.ELEMENT:
            filtered = results[results["element_id"].isin(
                selection.selected_element_ids)].copy()

            return (
                filtered.groupby([
                    "case_id",
                    "result_name",
                    "element_id",
                ],
                    as_index=False)["value"]
                .mean()
                .assign(location=ResultLocation.ELEMENT.value)
            )

        if criteria.mode == VisualizationMode.NODE_RAW:
            filtered = results[
                results["element_id"].isin(selection.selected_element_ids)
            ].copy()
            return filtered.assign(location=ResultLocation.NODE.value)

        element_ids = criteria.averaging_policy.target_element_ids(selection)
        filtered = results[results["element_id"].isin(element_ids)].copy()
        averaged = (
            filtered.groupby([
                "case_id",
                "result_name",
                "node_id",
            ],
                as_index=False)["value"]
            .mean()
            .assign(location=ResultLocation.NODE.value)
        )

        return averaged
