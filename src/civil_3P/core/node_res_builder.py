from __future__ import annotations

from typing import TYPE_CHECKING

from civil_3P.core.res_builder import ResBuilder
from civil_3P.core.res_data import ResData
from civil_3P.standard.model_components import ModelComponents as mc
from civil_3P.standard.task_res_repr import TaskNodeResCols as task_node_rpr

if TYPE_CHECKING:
    from civil_3P.core.model import Model
    from civil_3P.core.sel_context import SelContext
    from civil_3P.tasks.task_res import TaskRes


class NodeResBuilder(ResBuilder):
    def process(
        self,
        task_result: TaskRes,
        selection: SelContext,
        model: Model,
    ) -> ResData:
        results_df = task_result.results
        elements_nodes = (
            set(results_df[task_node_rpr.NODE].to_list()) & selection.node_ids
        )
        results_df = results_df[results_df[task_node_rpr.NODE].isin(elements_nodes)]

        return ResData(
            element_type=mc.NODES,
            res_df=results_df,
            elements=elements_nodes,
            nodes=elements_nodes,
        )
