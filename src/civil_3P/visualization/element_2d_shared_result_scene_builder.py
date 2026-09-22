from __future__ import annotations

import numpy as np

from civil_3P.core.model import FEMModel
from civil_3P.application.model_service import ModelService
from civil_3P.core.result_data import ResultData
from civil_3P.visualization.result_view_data import (
    ResultViewData,
    ResultElementViewData,
)
from civil_3P.standard.result_components import ViewContentKind
from civil_3P.core.selection import SelectionContext
from civil_3P.visualization.scene import Scene
from civil_3P.standard.task_result_representation import (
    Task2DResultsColumns as task_rpr_2d,
)
import pyvista as pv
from civil_3P.standard.model_representation import ModelTables as mt
from civil_3P.standard.model_representation import Elements2DColumns as rpr_2d

from civil_3P.visualization.scene_builder import SceneBuilder


class Element2DSharedResultSceneBuilder(SceneBuilder):
    def build_result_scene(
        self,
        results: ResultData,
        model: FEMModel,
    ) -> Scene:
        res_selection = SelectionContext(
            node_ids=set(),
            element_1d_ids=set(),
            element_2d_ids=results.elements,
        )
        idle_model = ModelService.model_without_elements(
            model,
            res_selection,
        )
        model_scene = self.build_scene(idle_model)

        res_model = self._model_service.model_with_elements(
            model,
            res_selection,
        )
        node_map, points = self.get_node_map(res_model)

        result_view = self._render_element_2d_shared_nodes(
            res_model=res_model,
            node_map=node_map,
            points=points,
            results=results,
        )

        return Scene(
            node_map=node_map,
            model_view=model_scene.model_view,
            result_view=result_view,
        )

    def _render_element_2d_shared_nodes(
        self,
        res_model: FEMModel,
        node_map: dict[str, int],
        points: np.ndarray,
        results: ResultData,
    ) -> ResultViewData:
        result_df = results.result_df

        node_values: dict[str, float] = dict()

        for row in result_df.itertuples(index=False):
            node_id = getattr(row, task_rpr_2d.NODE)
            value = getattr(row, task_rpr_2d.VALUE)
            node_values[node_id] = value

        elements_topology: dict[str, list[str]] = dict()
        element_2d_df = res_model.tables[mt.ELEMENTS_2D]

        for row in element_2d_df.itertuples(index=False):
            element_id = getattr(row, rpr_2d.ELEMENT)
            node1 = getattr(row, rpr_2d.NODE_1)
            node2 = getattr(row, rpr_2d.NODE_2)
            node3 = getattr(row, rpr_2d.NODE_3)
            node4 = getattr(row, rpr_2d.NODE_4, None)
            if node4 is not None:
                elements_topology[element_id] = [node1, node2, node3, node4]
            else:
                elements_topology[element_id] = [node1, node2, node3]

        cells: list[int] = []
        celltypes: list[int] = []
        for _, nodes in elements_topology.items():
            ids = [node_map[p] for p in nodes]
            if len(nodes) == 3:
                cells.extend([3, *ids])
                celltypes.append(pv.CellType.TRIANGLE)

            elif len(nodes) == 4:
                cells.extend([4, *ids])
                celltypes.append(pv.CellType.QUAD)

        values = np.full(points.shape[0], 0.0)
        for node_id, value in node_values.items():
            index = node_map.get(node_id)
            if index is not None:
                values[index] = value

        return ResultViewData(
            kind=ViewContentKind.ELEMENT_2D_SHARED_NODES,
            value_range=(min(values), max(values)) if values else (0.0, 0.0),
            data=ResultElementViewData(
                nodes=points,
                values=np.array(values),
                connection=np.array(cells),
                element_type=np.array(celltypes),
            ),
        )
