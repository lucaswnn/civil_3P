from __future__ import annotations

from typing import TYPE_CHECKING

from civil_3P.core.result_data import ResultData
from civil_3P.standard.model_components import ModelComponents as mc
from civil_3P.standard.task_result_representation import (
    TaskNodeResultsColumns as task_node_rpr,
)
from civil_3P.core.result_builder import ResultBuilder

if TYPE_CHECKING:
    from civil_3P.core.model import FEMModel
    from civil_3P.core.selection import SelectionContext
    from civil_3P.tasks.task_base import TaskResult


class NodeResultBuilder(ResultBuilder):
    def process(
        self,
        task_result: TaskResult,
        selection: SelectionContext,
        model: FEMModel,
    ) -> ResultData:
        results_df = task_result.results

        elements_nodes = (
            set(results_df[task_node_rpr.NODE].to_list()) & selection.node_ids
        )

        results_df = results_df[results_df[task_node_rpr.NODE].isin(elements_nodes)]

        return ResultData(
            element_type=mc.NODES,
            result_df=results_df,
            elements=elements_nodes,
            nodes=elements_nodes,
        )
