from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


from civil_3P.core.result_data import ResultData
from civil_3P.standard.model_components import ModelComponents as mc
from civil_3P.standard.model_representation import (
    ModelTables as mt,
    Elements1DColumns as rpr_1d,
    Elements2DColumns as rpr_2d,
)
from civil_3P.standard.task_result_representation import (
    TaskNodeResultsColumns as task_node_rpr,
    Task1DResultsColumns as task_1d_rpr,
    Task2DResultsColumns as task_2d_rpr,
)
from civil_3P.standard.result_components import (
    ResultLocation,
    Visualization2DMode,
)

if TYPE_CHECKING:
    import pandas as pd

    from civil_3P.core.model import FEMModel
    from civil_3P.core.selection import SelectionContext
    from civil_3P.tasks.task_base import TaskResult


@dataclass(frozen=True, slots=True)
class Result2DAveragingPolicy:
    include_adjacent: bool = True

    def target_element_ids(
        self,
        selection: SelectionContext,
    ) -> set[str]:
        if self.include_adjacent:
            return selection.all_element_ids

        return selection.selected_element_ids


@dataclass(frozen=True, slots=True)
class ResultVisualization2DCriteria:
    mode: Visualization2DMode
    averaging_policy: Result2DAveragingPolicy | None = None


class ResultBuilder:
    def process(
        self,
        task_result: TaskResult,
        selection: SelectionContext,
        model: FEMModel,
        *,
        visual_2d_criteria: ResultVisualization2DCriteria | None = None,
    ) -> ResultData:
        self._check_process_args(
            task_result,
            visual_2d_criteria,
        )
        results_df = task_result.results
        element_type = task_result.metadata.supported_element_type

        if element_type == mc.NODES:
            return self._process_node(
                results_df,
                selection,
            )

        elif element_type == mc.ELEMENTS_1D:
            return self._process_1d(
                results_df,
                selection,
                model,
            )

        elif element_type == mc.ELEMENTS_2D:
            return self._process_2d(
                results_df,
                selection,
                model,
                visual_2d_criteria,
            )

        raise ValueError(
            f"Unsupported element type: "
            f"{element_type}"
        )

    def _check_process_args(
        self,
        task_result: TaskResult,
        criteria: ResultVisualization2DCriteria | None,
    ) -> None:
        task_element = task_result.metadata.supported_element_type

        if task_element == mc.ELEMENTS_2D and criteria is None:
            raise ValueError(
                "Visualization2DCriteria must be provided for 2D elements"
            )

    def _process_node(
        self,
        results: pd.DataFrame,
        selection: SelectionContext,
    ) -> ResultData:
        elements_nodes = set(
            results[task_node_rpr.NODE]
            .to_list()
        ) & selection.node_ids

        results = results[
            results[task_node_rpr.NODE]
            .isin(elements_nodes)
        ]

        return ResultData(
            element_type=mc.NODES,
            result_df=results,
            elements=elements_nodes,
            nodes=elements_nodes,
        )

    def _process_1d(
        self,
        results: pd.DataFrame,
        selection: SelectionContext,
        model: FEMModel,
    ) -> ResultData:
        elements = set(
            results[task_1d_rpr.ELEMENT]
            .to_list()
        ) & selection.element_1d_ids

        model_elements_df = model.tables[mt.ELEMENTS_1D]
        filtered_elements_df = model_elements_df[
            model_elements_df[rpr_1d.ELEMENT]
            .isin(elements)
        ]

        nodes_i = set(
            filtered_elements_df[rpr_1d.NODE_I]
            .to_list()
        )
        nodes_j = set(
            filtered_elements_df[rpr_1d.NODE_J]
            .to_list()
        )
        nodes = nodes_i | nodes_j

        return ResultData(
            element_type=mc.ELEMENTS_1D,
            result_df=results,
            elements=elements,
            nodes=nodes,
        )

    def _process_2d(
        self,
        results: pd.DataFrame,
        selection: SelectionContext,
        model: FEMModel,
        criteria: ResultVisualization2DCriteria,
    ) -> ResultData:
        elements = set(
            results[task_2d_rpr.ELEMENT]
            .to_list()
        ) & selection.all_element_2d_ids

        model_elements_df = model.tables[mt.ELEMENTS_2D]
        filtered_elements_df = model_elements_df[
            model_elements_df[rpr_2d.ELEMENT]
            .isin(elements)
        ]

        nodes_1 = set(
            filtered_elements_df[rpr_2d.NODE_1]
            .to_list()
        )
        nodes_2 = set(
            filtered_elements_df[rpr_2d.NODE_2]
            .to_list()
        )
        nodes_3 = set(
            filtered_elements_df[rpr_2d.NODE_3]
            .to_list()
        )
        nodes_4 = set(
            filtered_elements_df[rpr_2d.NODE_4]
            .to_list()
        )
        nodes = nodes_1 | nodes_2 | nodes_3 | nodes_4

        if criteria.mode == Visualization2DMode.ELEMENT:
            return ResultData(
                element_type=mc.ELEMENTS_2D,
                result_df=results
                .groupby(
                    [task_2d_rpr.ELEMENT],
                    as_index=False,
                )[task_2d_rpr.VALUE]
                .mean()
                .assign(location=ResultLocation.ELEMENT),
                elements=elements,
                nodes=nodes,
            )

        if criteria.mode == Visualization2DMode.NODE_RAW:
            return ResultData(
                element_type=mc.ELEMENTS_2D,
                result_df=results,
                elements=elements,
                nodes=nodes,
            )

        return ResultData(
            element_type=mc.ELEMENTS_2D,
            result_df=results
            .groupby(
                [
                    task_2d_rpr.CASE,
                    task_2d_rpr.NODE,
                ],
                as_index=False,
            )[task_2d_rpr.VALUE]
            .mean()
            .assign(location=ResultLocation.NODE),
            elements=elements,
            nodes=nodes,
        )
