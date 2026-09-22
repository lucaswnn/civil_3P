from __future__ import annotations

from abc import ABC, abstractmethod
import numpy as np
import pandas as pd

from civil_3P.core.model import FEMModel
from civil_3P.standard import model_representation as rpr
from civil_3P.core.result_data import ResultData
from civil_3P.visualization.model_view_data import ModelViewData
from civil_3P.visualization.scene import Scene
import pyvista as pv
from civil_3P.core.result_builder import ResultVisualization2DCriteria


class SceneBuilder(ABC):
    def get_node_map(
        self,
        model: FEMModel,
    ) -> tuple[dict[str, int], np.ndarray]:
        nodes_df = model.tables[rpr.ModelTables.NODES]
        node_map = {
            str(getattr(row, rpr.NodesColumns.NODE)): idx
            for idx, row in enumerate(
                nodes_df.itertuples(index=False))
        }
        nodes = np.array(
            [
                (
                    float(getattr(n, rpr.NodesColumns.X)),
                    float(getattr(n, rpr.NodesColumns.Y)),
                    float(getattr(n, rpr.NodesColumns.Z)),
                )
                for n in nodes_df.itertuples(index=False)
            ],
            dtype=float,
        )

        return node_map, nodes

    def build_scene(
        self,
        model: FEMModel,
    ) -> Scene:
        node_map, nodes = self.get_node_map(model)
        element_1d_df = model.tables[rpr.ModelTables.ELEMENTS_1D]
        elements_1d_connection = []
        elements_1d_type = []

        for row in element_1d_df.itertuples(index=False):
            start = node_map[str(getattr(row, rpr.Elements1DColumns.NODE_I))]
            end = node_map[str(getattr(row, rpr.Elements1DColumns.NODE_J))]

            elements_1d_connection.extend([2, start, end])
            elements_1d_type.append(pv.CellType.LINE)

        element_2d_df = model.tables[rpr.ModelTables.ELEMENTS_2D]
        elements_2d_connection = []
        elements_2d_type = []

        for row in element_2d_df.itertuples(index=False):
            node_4 = getattr(row, rpr.Elements2DColumns.NODE_4)
            if not pd.isna(node_4):
                n1 = node_map[str(getattr(row, rpr.Elements2DColumns.NODE_1))]
                n2 = node_map[str(getattr(row, rpr.Elements2DColumns.NODE_2))]
                n3 = node_map[str(getattr(row, rpr.Elements2DColumns.NODE_3))]
                n4 = node_map[str(getattr(row, rpr.Elements2DColumns.NODE_4))]

                elements_2d_connection.extend([4, n1, n2, n3, n4])
                elements_2d_type.append(pv.CellType.QUAD)

            else:
                n1 = node_map[str(getattr(row, rpr.Elements2DColumns.NODE_1))]
                n2 = node_map[str(getattr(row, rpr.Elements2DColumns.NODE_2))]
                n3 = node_map[str(getattr(row, rpr.Elements2DColumns.NODE_3))]

                elements_2d_connection.extend([3, n1, n2, n3])
                elements_2d_type.append(pv.CellType.TRIANGLE)

        model_view_data = ModelViewData(
            nodes=nodes,
            elements_1d_connection=np.array(elements_1d_connection),
            elements_1d_type=np.array(elements_1d_type),
            elements_2d_connection=np.array(elements_2d_connection),
            elements_2d_type=np.array(elements_2d_type),
        )

        return Scene(
            node_map=node_map,
            model_view=model_view_data,
        )

    @abstractmethod
    def build_result_scene(
        self,
        results: ResultData,
        criteria: ResultVisualization2DCriteria,
        model: FEMModel,
    ) -> Scene:
        raise NotImplementedError()


class ModelSceneBuilder(SceneBuilder):
    def build_result_scene(
        self,
        results: ResultData,
        criteria: ResultVisualization2DCriteria,
        model: FEMModel,
    ) -> Scene:
        return self.build_scene(model)
