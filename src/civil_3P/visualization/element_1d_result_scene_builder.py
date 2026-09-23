import numpy as np

from civil_3P.core.model import FEMModel
from civil_3P.core.result_data import ResultData
from civil_3P.core.selection import SelectionContext
from civil_3P.standard.result_components import Visualization2DMode
from civil_3P.standard.model_representation import ModelTables as mt
from civil_3P.standard.model_representation import Elements1DColumns as rpr_1d
from civil_3P.visualization.scene_builder import SceneBuilder
from civil_3P.visualization.scene import Scene
from civil_3P.visualization.result_scene_data import (
    ResultSceneData,
    ResultElementSceneData,
    ViewContentKind,
)
from civil_3P.standard.task_result_representation import (
    Task1DResultsColumns as task_rpr_1d,
)
from civil_3P.application.model_service import ModelService


class Element1DResultSceneBuilder(SceneBuilder):
    def build_result_scene(
        self,
        results: ResultData,
        model: FEMModel,
    ) -> Scene:
        res_selection = SelectionContext(
            node_ids=set(),
            element_1d_ids=results.elements,
            element_2d_ids=set(),
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
        node_map, nodes = self.get_node_map(res_model)
        result_df = results.result_df

        elements: dict[str, list[tuple[float, float]]] = dict()

        for row in result_df.itertuples(index=False):
            element_id = getattr(row, task_rpr_1d.ELEMENT)
            station = getattr(row, task_rpr_1d.STATION)
            value = getattr(row, task_rpr_1d.VALUE)
            if element_id not in elements:
                elements[element_id] = []
            elements[element_id].append((station, value))

        for k in elements.keys():
            elements[k].sort()

        elements_topology: dict[str, tuple[str, str]] = dict()
        element_1d_df = res_model.tables[mt.ELEMENTS_1D]

        for row in element_1d_df.itertuples(index=False):
            element_id = getattr(row, rpr_1d.ELEMENT)
            start_node = getattr(row, rpr_1d.NODE_I)
            end_node = getattr(row, rpr_1d.NODE_J)
            elements_topology[element_id] = (start_node, end_node)

        element_1d_points: list[np.ndarray] = []
        element_1d_values: list[float] = []
        lines: list[int] = []

        for element_id, profile in elements.items():
            bar = elements_topology.get(element_id)
            if bar is None or not profile:
                continue

            start = nodes[node_map[bar[0]]]
            end = nodes[node_map[bar[1]]]
            length = float(np.linalg.norm(end - start))

            line = [len(profile)]
            for station, value in profile:
                fraction = 0.0 if length == 0 else min(max(station / length, 0.0), 1.0)
                element_1d_points.append(start + fraction * (end - start))
                element_1d_values.append(value)
                line.append(len(element_1d_points) - 1)
            lines.extend(line)

        return Scene(
            node_map=node_map,
            model_view=model_scene.model_view,
            result_view=ResultSceneData(
                kind=ViewContentKind.ELEMENT_1D_PROFILE,
                value_range=(
                    (
                        np.nanmin(element_1d_values),
                        np.nanmax(element_1d_values),
                    )
                    if element_1d_values
                    else (0.0, 0.0)
                ),
                data=ResultElementSceneData(
                    nodes=np.array(element_1d_points),
                    values=np.array(element_1d_values),
                    connection=np.array(lines),
                ),
            ),
        )
