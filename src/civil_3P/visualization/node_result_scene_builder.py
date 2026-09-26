from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from civil_3P.application.model_service import ModelService
from civil_3P.core.selection_context import SelectionContext
from civil_3P.standard.result_components import ViewContentKind
from civil_3P.standard.task_result_representation import (
    TaskNodeResultsColumns as task_rpr_node,
)
from civil_3P.visualization.result_element_scene_data import (
    ResultElementSceneData
)
from civil_3P.visualization.result_scene_data import (
    ResultSceneData
)
from civil_3P.visualization.scene import Scene
from civil_3P.visualization.scene_builder import SceneBuilder

if TYPE_CHECKING:
    from civil_3P.core.model import Model
    from civil_3P.core.result_data import ResultData


class NodeResultSceneBuilder(SceneBuilder):
    def build_result_scene(
        self,
        results: ResultData,
        model: Model,
    ) -> Scene:
        model_scene = self.build_scene(model)

        res_selection = SelectionContext(
            node_ids=results.nodes,
            element_1d_ids={},
            element_2d_ids={},
        )
        res_model = ModelService.model_without_elements(
            model,
            res_selection,
        )
        node_map, nodes = self.get_node_map(res_model)

        values = np.full(nodes.shape[0], np.nan)

        for row in results.result_df.itertuples():
            node_id = getattr(row, task_rpr_node.NODE)
            value = getattr(row, task_rpr_node.VALUE)
            index = node_map.get(node_id)

            if index is not None:
                values[index] = value

        return Scene(
            node_map=node_map,
            model_view=model_scene.model_view,
            result_view=ResultSceneData(
                kind=ViewContentKind.NODE_POINTS,
                value_range=(
                    (np.nanmin(values), np.nanmax(values))
                    if values.size > 0
                    else (0.0, 0.0)
                ),
                data=ResultElementSceneData(
                    nodes=nodes,
                    values=values,
                ),
            ),
        )
