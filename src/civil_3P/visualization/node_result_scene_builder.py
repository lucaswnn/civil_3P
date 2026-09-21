import numpy as np

from civil_3P.core.model import FEMModel
from civil_3P.core.result_builder import Visualization2DMode
from civil_3P.core.selection import SelectionContext
from civil_3P.core.result_data import ResultData
from civil_3P.standard.result_components import ViewContentKind
from civil_3P.standard.task_result_representation import TaskNodeResultsColumns as task_rpr_node
from civil_3P.visualization.result_view_data import ResultElementViewData, ResultViewData
from civil_3P.visualization.scene import Scene
from civil_3P.visualization.scene_builder import SceneBuilder


class NodeResultSceneBuilder(SceneBuilder):
    def build_result_scene(
        self,
        results: ResultData,
        criteria: Visualization2DMode,
        model: FEMModel,
    ) -> Scene:
        model_scene = self.build_scene(model)

        res_selection = SelectionContext(
            node_ids=results.nodes,
            element_1d_ids={},
            element_2d_ids={},
        )
        res_model = self._model_service.model_without_elements(
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
            result_view=ResultViewData(
                kind=ViewContentKind.NODE_POINTS,
                value_range=(np.nanmin(values), np.nanmax(values))
                if values.size > 0
                else (0.0, 0.0),
                data=ResultElementViewData(
                    nodes=nodes,
                    values=values,
                )
            ),
        )
