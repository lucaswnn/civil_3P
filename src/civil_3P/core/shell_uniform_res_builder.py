from __future__ import annotations

from typing import TYPE_CHECKING

from civil_3P.core.res_builder import ResBuilder
from civil_3P.core.res_data import ResData
from civil_3P.standard.model_components import ModelComponents as mc
from civil_3P.standard.model_repr import ModelTables as mt
from civil_3P.standard.model_repr import ShellCols as rpr_2d
from civil_3P.standard.task_res_repr import TaskShellResCols as task_2d_rpr

if TYPE_CHECKING:
    from civil_3P.core.model import Model
    from civil_3P.core.sel_context import SelContext
    from civil_3P.tasks.task_res import TaskRes


class ShellUniformResBuilder(ResBuilder):
    def process(
        self,
        task_result: TaskRes,
        selection: SelContext,
        model: Model,
    ) -> ResData:
        results_df = task_result.results
        elements = (
            set(results_df[task_2d_rpr.ELEMENT].to_list()) & selection.all_shell_ids
        )

        model_elements_df = model.tables[mt.SHELLS]
        filtered_elements_df = model_elements_df[
            model_elements_df[rpr_2d.ELEMENT].isin(elements)
        ]
        nodes_1 = set(filtered_elements_df[rpr_2d.NODE_1].to_list())
        nodes_2 = set(filtered_elements_df[rpr_2d.NODE_2].to_list())
        nodes_3 = set(filtered_elements_df[rpr_2d.NODE_3].to_list())
        nodes_4 = set(filtered_elements_df[rpr_2d.NODE_4].to_list())
        nodes = nodes_1 | nodes_2 | nodes_3 | nodes_4

        res_df = results_df.groupby(
            [
                task_2d_rpr.ELEMENT,
            ],
            as_index=False,
        )[task_2d_rpr.VALUE].mean()

        res_df = res_df[res_df[task_2d_rpr.ELEMENT].isin(elements)]

        return ResData(
            element_type=mc.SHELLS,
            res_df=res_df,
            elements=elements,
            nodes=nodes,
        )
