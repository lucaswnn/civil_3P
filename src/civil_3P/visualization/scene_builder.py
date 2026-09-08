from __future__ import annotations

from enum import StrEnum
from typing import Any
import pandas as pd
from abc import ABC, abstractmethod
import numpy as np

from civil_3P.application.model_service import ModelService
from civil_3P.core.model import FEMModel
from civil_3P.core.result_builder import Visualization2DMode
from civil_3P.core.selection import SelectionContext
from civil_3P.standard import model_representation as rpr
from civil_3P.standard import model_components as mc
from civil_3P.core.result_data import ResultData
from civil_3P.standard.result_components import ViewContentKind
from civil_3P.standard.task_result_representation import TaskNodeResultsColumns as task_rpr_node
from civil_3P.visualization.model_view_data import ModelViewData
from civil_3P.visualization.result_view_data import ResultElementViewData, ResultViewData
from civil_3P.visualization.scene import Scene
import pyvista as pv
from civil_3P.visualization.visualization_content_builder import ResultVisualizationBuilder


class SceneBuilder(ABC):
    def __init__(self, model_service: ModelService) -> None:
        self._model_service = model_service

    def get_node_map_with_node_set(
            self,
            model: FEMModel,
            nodes: set[str],
    ) -> tuple[dict[str, int], np.ndarray]:
        nodes_df = model.tables[rpr.ModelTables.NODES]
        node_map = {
            str(getattr(row, rpr.NodesColumns.NODE)): idx
            for idx, row in enumerate(
                nodes_df.itertuples(index=False))
            if str(getattr(row, rpr.NodesColumns.NODE)) in nodes
        }
        nodes_array = np.array(
            [
                (
                    float(getattr(n, mc.ModelNodeComponents.NODE_X)),
                    float(getattr(n, mc.ModelNodeComponents.NODE_Y)),
                    float(getattr(n, mc.ModelNodeComponents.NODE_Z)),
                )
                for n in nodes_df.itertuples(index=False)
                if str(getattr(n, rpr.NodesColumns.NODE)) in nodes
            ],
            dtype=float,
        )

        return node_map, nodes_array

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
                    float(getattr(n, mc.ModelNodeComponents.NODE_X)),
                    float(getattr(n, mc.ModelNodeComponents.NODE_Y)),
                    float(getattr(n, mc.ModelNodeComponents.NODE_Z)),
                )
                for n in nodes_df.itertuples(index=False)
            ],
            dtype=float,
        )

        return node_map, nodes

    def build_scene(self, selection: SelectionContext) -> Scene:
        model = self._model_service.get_model_by_selection(selection)
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
            if getattr(row, rpr.Elements2DColumns.NODE_4) is not None:
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
        criteria: Visualization2DMode,
    ) -> Scene:
        raise NotImplementedError()


class ModelSceneBuilder(SceneBuilder):
    def build_result_scene(
        self,
        results: ResultData,
        criteria: Visualization2DMode,
        selection: SelectionContext,
    ) -> Scene:
        raise NotImplementedError()


class NodeResultSceneBuilder(SceneBuilder):
    def build_result_scene(
        self,
        results: ResultData,
        criteria: Visualization2DMode,
        selection: SelectionContext,
    ) -> Scene:
        model_scene = self.build_scene(selection)

        res_selection = SelectionContext(
            node_ids=results.nodes,
            element_1d_ids={},
            element_2d_ids={},
        )
        model = self._model_service.get_model_by_selection(selection)
        model = self._model_service.model_without_elements(
            model, 
            res_selection,
        )
        node_map, nodes = self.get_node_map(model)

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


class Element1DResultSceneBuilder(SceneBuilder):
    def build_result_scene(
        self,
        results: ResultData,
        criteria: Visualization2DMode,
        selection: SelectionContext,
    ) -> Scene:
        model_scene = self.build_scene(selection)
        
        res_selection = SelectionContext(
            node_ids={},
            element_1d_ids=results.elements,
            element_2d_ids={},
        )
        model = self._model_service.get_model_by_selection(selection)
        model = self._model_service.model_without_elements(
            model, 
            res_selection,
        )
        node_map, nodes = self.get_node_map(model)

        element_1d_points: list[np.ndarray] = []
        element_1d_values: list[float] = []
        lines: list[int] = []

        for element_id, profile in visualization.element_station_values.items():
            bar = bars.get(element_id)
            if bar is None or not profile:
                continue

            start = points[
                node_map[bar[mc.ModelElement1DComponents.ELEMENT_1D_START_NODE]]
            ]
            end = points[node_map[bar[mc.ModelElement1DComponents.ELEMENT_1D_END_NODE]]]
            length = float(np.linalg.norm(end - start))

            line = [len(profile)]
            for station, value in profile:
                fraction = 0.0 if length == 0 else min(
                    max(station / length, 0.0), 1.0)
                profile_points.append(start + fraction * (end - start))
                profile_values.append(value)
                line.append(len(profile_points) - 1)
            lines.extend(line)


class Element2DResultSceneBuilder(SceneBuilder):
    def build_result_scene(
        self,
        results: ResultData,
        criteria: Visualization2DMode,
        selection: SelectionContext,
    ) -> Scene:
        raise NotImplementedError()


class SceneBuilderr:
    def build_scene(self, model: FEMModel) -> Scene:
        nodes = self._build_nodes(
            model.tables[rpr.ModelTables.NODES]
        )
        elements_1d = self._build_1d_elements(
            model.tables[rpr.ModelTables.ELEMENTS_1D]
        )
        elements_2d = self._build_2d_elements(
            model.tables[rpr.ModelTables.ELEMENTS_2D]
        )

        return Scene(
            nodes=nodes,
            elements_1d=elements_1d,
            elements_2d=elements_2d,
        )

    def build_result_scene(
        self,
        model: FEMModel,
        results: ResultData,
        criteria: Visualization2DMode,
        selection: SelectionContext,
    ) -> Scene:
        scene = self.build_scene(model)
        content = ResultVisualizationBuilder(
            mode=criteria.mode,
            component=selection.element_type,
        )
        visualization = content.build(results)

        return scene.with_result_visualization(visualization)

    def _build_nodes(
        self,
        nodes: pd.DataFrame,
    ) -> dict[str, dict[str, float]]:
        return {
            str(getattr(row, rpr.NodesColumns.NODE)): {
                mc.ModelNodeComponents.NODE_X: float(getattr(row, rpr.NodesColumns.X)),
                mc.ModelNodeComponents.NODE_Y: float(getattr(row, rpr.NodesColumns.Y)),
                mc.ModelNodeComponents.NODE_Z: float(getattr(row, rpr.NodesColumns.Z)),
            }
            for row in nodes.itertuples(index=False)
        }

    def _build_1d_elements(
        self,
        elements_1d: pd.DataFrame,
    ) -> dict[str, dict[str, Any]]:
        return {
            str(getattr(row, rpr.Elements1DColumns.ELEMENT)): {
                mc.ModelElement1DComponents.ELEMENT_1D_START_NODE: str(getattr(row, rpr.Elements1DColumns.NODE_I)),
                mc.ModelElement1DComponents.ELEMENT_1D_END_NODE: str(getattr(row, rpr.Elements1DColumns.NODE_J)),
            }
            for row in elements_1d.itertuples(index=False)
        }

    def _build_2d_elements(
        self,
        elements_2d: pd.DataFrame,
    ) -> dict[str, dict[str, Any]]:
        return {
            str(getattr(row, rpr.Elements2DColumns.ELEMENT)): {
                mc.ModelElement2DComponents.ELEMENT_2D_NODES: [
                    str(node_id)
                    for node_id in [
                        getattr(row, rpr.Elements2DColumns.NODE_1, None),
                        getattr(row, rpr.Elements2DColumns.NODE_2, None),
                        getattr(row, rpr.Elements2DColumns.NODE_3, None),
                        getattr(row, rpr.Elements2DColumns.NODE_4, None),
                    ]
                    if not pd.isna(node_id)
                ],
            }
            for row in elements_2d.itertuples(index=False)
        }
