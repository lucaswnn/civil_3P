from __future__ import annotations

from typing import TYPE_CHECKING

from civil_3P.core.result_data import ResultData
from civil_3P.standard.model_components import ModelComponents as mc
from civil_3P.standard.model_representation import (
    ModelTables as mt,
    Elements2DColumns as rpr_2d,
)
from civil_3P.standard.task_result_representation import (
    Task2DResultsColumns as task_2d_rpr,
)
from civil_3P.core.result_builder import ResultBuilder

if TYPE_CHECKING:
    from civil_3P.core.model import FEMModel
    from civil_3P.core.selection import SelectionContext
    from civil_3P.tasks.task_base import TaskResult


class Element2DIsolatedResultBuilder(ResultBuilder):
    def process(
        self,
        task_result: TaskResult,
        selection: SelectionContext,
        model: FEMModel,
    ) -> ResultData:
        results_df = task_result.results
        elements = (
            set(results_df[task_2d_rpr.ELEMENT].to_list())
            & selection.all_element_2d_ids
        )

        model_elements_df = model.tables[mt.ELEMENTS_2D]
        filtered_elements_df = model_elements_df[
            model_elements_df[rpr_2d.ELEMENT].isin(elements)
        ]

        nodes_1 = set(filtered_elements_df[rpr_2d.NODE_1].to_list())
        nodes_2 = set(filtered_elements_df[rpr_2d.NODE_2].to_list())
        nodes_3 = set(filtered_elements_df[rpr_2d.NODE_3].to_list())
        nodes_4 = set(filtered_elements_df[rpr_2d.NODE_4].to_list())
        nodes = nodes_1 | nodes_2 | nodes_3 | nodes_4

        return ResultData(
            element_type=mc.ELEMENTS_2D,
            result_df=results_df,
            elements=elements,
            nodes=nodes,
        )
