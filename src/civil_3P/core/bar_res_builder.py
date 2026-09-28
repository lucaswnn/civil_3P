from __future__ import annotations

from typing import TYPE_CHECKING

from civil_3P.core.res_builder import ResBuilder
from civil_3P.core.res_data import ResData
from civil_3P.standard.model_components import ModelComponents as mc
from civil_3P.standard.model_repr import BarCols as rpr_1d
from civil_3P.standard.model_repr import ModelTables as mt
from civil_3P.standard.task_res_repr import TaskBarResCols as task_1d_rpr

if TYPE_CHECKING:
    from civil_3P.core.model import Model
    from civil_3P.core.sel_context import SelContext
    from civil_3P.tasks.task_res import TaskRes


class BarResBuilder(ResBuilder):
    def process(
        self,
        task_result: TaskRes,
        selection: SelContext,
        model: Model,
    ) -> ResData:
        results_df = task_result.results
        elements = set(results_df[task_1d_rpr.ELEMENT].to_list()) & selection.bar_ids
        model_elements_df = model.tables[mt.BARS]
        filtered_elements_df = model_elements_df[
            model_elements_df[rpr_1d.ELEMENT].isin(elements)
        ]
        nodes_i = set(filtered_elements_df[rpr_1d.NODE_I].to_list())
        nodes_j = set(filtered_elements_df[rpr_1d.NODE_J].to_list())
        nodes = nodes_i | nodes_j

        return ResData(
            element_type=mc.BARS,
            res_df=results_df,
            elements=elements,
            nodes=nodes,
        )
