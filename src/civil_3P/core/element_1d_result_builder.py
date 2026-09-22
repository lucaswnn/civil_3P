from __future__ import annotations

from typing import TYPE_CHECKING

from civil_3P.core.result_data import ResultData
from civil_3P.standard.model_components import ModelComponents as mc
from civil_3P.standard.model_representation import (
    ModelTables as mt,
    Elements1DColumns as rpr_1d,
)
from civil_3P.standard.task_result_representation import (
    Task1DResultsColumns as task_1d_rpr,
)

from civil_3P.core.result_builder import ResultBuilder

if TYPE_CHECKING:
    from civil_3P.core.model import FEMModel
    from civil_3P.core.selection import SelectionContext
    from civil_3P.tasks.task_base import TaskResult


class Element1DResultBuilder(ResultBuilder):
    def process(
        self,
        task_result: TaskResult,
        selection: SelectionContext,
        model: FEMModel,
    ) -> ResultData:
        results_df = task_result.results

        elements = (
            set(results_df[task_1d_rpr.ELEMENT].to_list()) & selection.element_1d_ids
        )

        model_elements_df = model.tables[mt.ELEMENTS_1D]
        filtered_elements_df = model_elements_df[
            model_elements_df[rpr_1d.ELEMENT].isin(elements)
        ]

        nodes_i = set(filtered_elements_df[rpr_1d.NODE_I].to_list())
        nodes_j = set(filtered_elements_df[rpr_1d.NODE_J].to_list())
        nodes = nodes_i | nodes_j

        return ResultData(
            element_type=mc.ELEMENTS_1D,
            result_df=results_df,
            elements=elements,
            nodes=nodes,
        )
