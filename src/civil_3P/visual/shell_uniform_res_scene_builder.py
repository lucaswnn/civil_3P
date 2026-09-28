from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pyvista as pv

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
    from civil_3P.core.res_data import ResData


class ShellUniformResSceneBuilder(SceneBuilder):
    def build_res_scene(
        self,
        results: ResData,
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
        results: ResSceneData,
    ) -> Scene:
        res_df = results.res_df

        elements_values: dict[str, float] = dict()

        for row in res_df.itertuples(index=False):
            element_id = getattr(row, task_rpr_2d.ELEMENT)
            value = getattr(row, task_rpr_2d.VALUE)
            elements_values[element_id] = value

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

        cells: list[int] = []
        celltypes: list[int] = []
        values: list[float] = []

        for element_id, nodes in elements_topology.items():
            if len(nodes) == 3:
                ids = [node_map[p] for p in nodes]
                cells.extend([3, *ids])
                celltypes.append(pv.CellType.TRIANGLE)

            elif len(nodes) == 4:
                ids = [node_map[p] for p in nodes]
                cells.extend([4, *ids])
                celltypes.append(pv.CellType.QUAD)

            values.append(elements_values[element_id])

        return ResSceneData(
            kind=ResSceneKind.SHELL_UNIFORM,
            value_range=((min(values), max(values)) if values.size > 0 else (0.0, 0.0)),
            data=ResElementSceneData(
                nodes=points,
                values=np.array(values),
                connection=np.array(cells),
                element_type=np.array(celltypes),
            ),
        )
