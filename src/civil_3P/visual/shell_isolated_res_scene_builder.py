from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from civil_3P.app.model_service import ModelService
from civil_3P.core.sel_context import SelContext
from civil_3P.standard.model_repr import ModelTables as mt
from civil_3P.standard.model_repr import ShellCols as rpr_2d
from civil_3P.standard.res_components import ResSceneKind
from civil_3P.standard.task_res_repr import TaskShellResCols as task_rpr_2d
from civil_3P.visual.res_element_scene_data import ResElementSceneData
from civil_3P.visual.res_scene_data import ResSceneData
from civil_3P.visual.scene import Scene
from civil_3P.visual.scene_builder import SceneBuilder

if TYPE_CHECKING:
    from civil_3P.core.model import Model
    from civil_3P.core.res_data import ResultData


class ShellIsolatedResSceneBuilder(SceneBuilder):
    def build_res_scene(
        self,
        results: ResultData,
        model: Model,
    ) -> Scene:
        res_selection = SelContext(
            node_ids=set(),
            bar_ids=set(),
            shell_ids=results.elements,
        )
        idle_model = ModelService.model_without_elements(
            model,
            res_selection,
        )
        model_scene = self.build_scene(idle_model)

        res_model = ModelService.model_with_elements(
            model,
            res_selection,
        )
        node_map, points = self.get_node_map(res_model)

        res_view = self._build_res_scene(
            res_model=res_model,
            node_map=node_map,
            points=points,
            results=results,
        )

        return Scene(
            node_map=node_map,
            model_view=model_scene.model_view,
            res_view=res_view,
        )

    def _build_res_scene(
        self,
        res_model: Model,
        node_map: dict[str, int],
        points: np.ndarray,
        results: ResultData,
    ) -> ResSceneData:
        res_df = results.res_df

        elements_values: dict[str, dict[str, float]] = dict()

        for row in res_df.itertuples(index=False):
            element_id = getattr(row, task_rpr_2d.ELEMENT)
            node_id = getattr(row, task_rpr_2d.NODE)
            value = getattr(row, task_rpr_2d.VALUE)

            if element_id not in elements_values:
                elements_values[element_id] = dict()

            elements_values[element_id][node_id] = value

        elements_topology: dict[str, list[str]] = dict()
        shell_df = res_model.tables[mt.SHELLS]

        for row in shell_df.itertuples(index=False):
            element_id = getattr(row, rpr_2d.ELEMENT)
            node1 = getattr(row, rpr_2d.NODE_1)
            node2 = getattr(row, rpr_2d.NODE_2)
            node3 = getattr(row, rpr_2d.NODE_3)
            node4 = getattr(row, rpr_2d.NODE_4, None)

            if node4 is not None:
                elements_topology[element_id] = [
                    node1,
                    node2,
                    node3,
                    node4,
                ]

            else:
                elements_topology[element_id] = [node1, node2, node3]

        blocks: list[tuple[np.ndarray, list[int], np.ndarray]] = []
        min_max = [0.0, 0.0]

        for element_id, node_values in elements_values.items():
            model_node_ids = list(elements_topology[element_id])
            scene_node_ids = [node_map[p] for p in model_node_ids]
            local_points = np.array(
                [points[node_id] for node_id in scene_node_ids],
                dtype=float,
            )

            values = np.array([node_values[node_id] for node_id in model_node_ids])
            faces = [len(scene_node_ids), *range(len(scene_node_ids))]
            min_max[0] = min(min(values), min_max[0])
            min_max[1] = max(max(values), min_max[1])
            blocks.append((local_points, faces, values))

        return ResSceneData(
            kind=ResSceneKind.SHELL_ISOLATED_NODES,
            value_range=(min_max[0], min_max[1]),
            data=ResElementSceneData(
                nodes=points,
                block_data=blocks,
            ),
        )
