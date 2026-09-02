from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from civil_3P.core.selection import SelectionContext
from civil_3P.core.model import FEMModel
from civil_3P.standard import model_components as mc
from civil_3P.standard.result_components import (
    VisualizationMode,
    ResultLocation,
    Result,
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
        model: FEMModel,
    ) -> Result:
        if selection.element_type == mc.ModelComponents.ELEMENTS_1D:
            return self._process_1d(task_results, criteria, model)
        elif selection.element_type == mc.ModelComponents.ELEMENTS_2D:
            return self._process_2d(task_results, criteria, model)
        elif selection.element_type == mc.ModelComponents.NODES:
            return self._process_node(task_results, criteria, model)

        raise ValueError(f"Unsupported element type: {selection.element_type}")

    def _process_1d(
        self,
        results: pd.DataFrame,
        criteria: VisualizationCriteria,
        model: FEMModel,
    ) -> Result:
        elements = set(results[rpr.Task1DResultsColumns.ELEMENT].to_list())
        model_elements_df = model.tables[rpr.ModelTables.ELEMENTS_1D]
        filtered_elements_df = model_elements_df[
            model_elements_df[rpr.Elements1DColumns.ELEMENT].isin(elements)
        ]
        nodes_i = set(filtered_elements_df[rpr.Elements1DColumns.NODE_I].to_list())
        nodes_j = set(filtered_elements_df[rpr.Elements1DColumns.NODE_J].to_list())
        nodes = nodes_i | nodes_j
        return Result(
            result_df=results,
            elements=elements,
            nodes=nodes,
        )

    def _process_node(
        self,
        results: pd.DataFrame,
        criteria: VisualizationCriteria,
        model: FEMModel,
    ) -> Result:
        elements_nodes = set(results[rpr.TaskNodeResultsColumns.NODE].to_list())
        return Result(
            result_df=results,
            elements=elements_nodes,
            nodes=elements_nodes,
        )

    def _process_2d(
        self,
        results: pd.DataFrame,
        criteria: VisualizationCriteria,
        model: FEMModel,
    ) -> Result:
        elements = set(results[rpr.Task2DResultsColumns.ELEMENT].to_list())
        model_elements_df = model.tables[rpr.ModelTables.ELEMENTS_2D]
        filtered_elements_df = model_elements_df[
            model_elements_df[rpr.Elements2DColumns.ELEMENT].isin(elements)
        ]
        nodes_1 = set(filtered_elements_df[rpr.Elements2DColumns.NODE_1].to_list())
        nodes_2 = set(filtered_elements_df[rpr.Elements2DColumns.NODE_2].to_list())
        nodes_3 = set(filtered_elements_df[rpr.Elements2DColumns.NODE_3].to_list())
        nodes_4 = set(filtered_elements_df[rpr.Elements2DColumns.NODE_4].to_list())
        nodes = nodes_1 | nodes_2 | nodes_3 | nodes_4

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
                elements=elements,
                nodes=nodes,
            )

        if criteria.mode == VisualizationMode.NODE_RAW:
            return Result(
                result_df=results,
                elements=elements,
                nodes=nodes,
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
            elements=elements,
            nodes=nodes,
        )
