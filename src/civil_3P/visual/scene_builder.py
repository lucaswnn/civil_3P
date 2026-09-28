from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import numpy as np
import pandas as pd
import pyvista as pv

from civil_3P.standard import model_repr as rpr
from civil_3P.visual.model_scene_data import ModelSceneData
from civil_3P.visual.scene import Scene

if TYPE_CHECKING:
    from civil_3P.core.model import Model
    from civil_3P.core.res_data import ResData


class SceneBuilder(ABC):
    def get_node_map(
        self,
        model: Model,
    ) -> tuple[dict[str, int], np.ndarray]:
        nodes_df = model.tables[rpr.ModelTables.NODES]
        node_map = {
            str(getattr(row, rpr.NodeCols.NODE)): idx
            for idx, row in enumerate(nodes_df.itertuples(index=False))
        }
        nodes = np.array(
            [
                (
                    float(getattr(n, rpr.NodeCols.X)),
                    float(getattr(n, rpr.NodeCols.Y)),
                    float(getattr(n, rpr.NodeCols.Z)),
                )
                for n in nodes_df.itertuples(index=False)
            ],
            dtype=float,
        )

        return node_map, nodes

    def build_scene(
        self,
        model: Model,
    ) -> Scene:
        node_map, nodes = self.get_node_map(model)
        bar_df = model.tables[rpr.ModelTables.BARS]
        bars_connection = []
        bars_type = []

        for row in bar_df.itertuples(index=False):
            start = node_map[str(getattr(row, rpr.BarCols.NODE_I))]
            end = node_map[str(getattr(row, rpr.BarCols.NODE_J))]
            bars_connection.extend([2, start, end])
            bars_type.append(pv.CellType.LINE)

        shell_df = model.tables[rpr.ModelTables.SHELLS]
        shells_connection = []
        shells_type = []

        for row in shell_df.itertuples(index=False):
            node_4 = getattr(row, rpr.ShellCols.NODE_4)

            if not pd.isna(node_4):
                n1 = node_map[str(getattr(row, rpr.ShellCols.NODE_1))]
                n2 = node_map[str(getattr(row, rpr.ShellCols.NODE_2))]
                n3 = node_map[str(getattr(row, rpr.ShellCols.NODE_3))]
                n4 = node_map[str(getattr(row, rpr.ShellCols.NODE_4))]

                shells_connection.extend([4, n1, n2, n3, n4])
                shells_type.append(pv.CellType.QUAD)

            else:
                n1 = node_map[str(getattr(row, rpr.ShellCols.NODE_1))]
                n2 = node_map[str(getattr(row, rpr.ShellCols.NODE_2))]
                n3 = node_map[str(getattr(row, rpr.ShellCols.NODE_3))]

                shells_connection.extend([3, n1, n2, n3])
                shells_type.append(pv.CellType.TRIANGLE)

        model_view_data = ModelSceneData(
            nodes=nodes,
            bars_connection=np.array(bars_connection),
            bars_type=np.array(bars_type),
            shells_connection=np.array(shells_connection),
            shells_type=np.array(shells_type),
        )

        return Scene(
            node_map=node_map,
            model_view=model_view_data,
        )

    @abstractmethod
    def build_res_scene(
        self,
        results: ResData,
        model: Model,
    ) -> Scene:
        raise NotImplementedError()
