from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from civil_3P.app.model_service import ModelService
from civil_3P.core.sel_context import SelContext
from civil_3P.standard.res_components import ResSceneKind
from civil_3P.standard.task_res_repr import TaskNodeResCols as task_rpr_node
from civil_3P.visual.res_element_scene_data import ResElementSceneData
from civil_3P.visual.res_scene_data import ResSceneData
from civil_3P.visual.scene import Scene
from civil_3P.visual.scene_builder import SceneBuilder

if TYPE_CHECKING:
    from civil_3P.core.model import Model
    from civil_3P.core.res_data import ResData


class NodeResSceneBuilder(SceneBuilder):
    def build_res_scene(
        self,
        results: ResData,
        model: Model,
    ) -> Scene:
        model_scene = self.build_scene(model)

        res_selection = SelContext(
            node_ids=results.nodes,
            bar_ids=set(),
            shell_ids=set(),
        )
        res_model = ModelService.model_with_elements(
            model,
            res_selection,
        )
        node_map, nodes = self.get_node_map(res_model)

        values = np.full(nodes.shape[0], np.nan)

        for row in results.res_df.itertuples():
            node_id = getattr(row, task_rpr_node.NODE)
            value = getattr(row, task_rpr_node.VALUE)
            index = node_map.get(node_id)

            if index is not None:
                values[index] = value

        return Scene(
            node_map=node_map,
            model_view=model_scene.model_view,
            res_view=ResSceneData(
                kind=ResSceneKind.NODE,
                value_range=(
                    (np.nanmin(values), np.nanmax(values))
                    if values.size > 0
                    else (0.0, 0.0)
                ),
                data=ResElementSceneData(
                    nodes=nodes,
                    values=values,
                ),
            ),
        )
