from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from civil_3P.app.model_service import ModelService
from civil_3P.core.sel_context import SelContext
from civil_3P.standard.model_repr import BarCols as rpr_1d
from civil_3P.standard.model_repr import ModelTables as mt
from civil_3P.standard.res_components import ResSceneKind
from civil_3P.standard.task_res_repr import TaskBarResCols as task_rpr_1d
from civil_3P.visual.res_element_scene_data import ResElementSceneData
from civil_3P.visual.res_scene_data import ResSceneData
from civil_3P.visual.scene import Scene
from civil_3P.visual.scene_builder import SceneBuilder

if TYPE_CHECKING:
    from civil_3P.core.model import Model
    from civil_3P.core.res_data import ResultData


class BarResSceneBuilder(SceneBuilder):
    def build_res_scene(
        self,
        results: ResultData,
        model: Model,
    ) -> Scene:
        res_selection = SelContext(
            node_ids=set(),
            bar_ids=results.elements,
            shell_ids=set(),
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
        res_df = results.res_df

        elements: dict[str, list[tuple[float, float]]] = dict()

        for row in res_df.itertuples(index=False):
            element_id = getattr(row, task_rpr_1d.ELEMENT)
            station = getattr(row, task_rpr_1d.STATION)
            value = getattr(row, task_rpr_1d.VALUE)

            if element_id not in elements:
                elements[element_id] = []

            elements[element_id].append((station, value))

        for k in elements.keys():
            elements[k].sort()

        elements_topology: dict[str, tuple[str, str]] = dict()
        bar_df = res_model.tables[mt.BARS]

        for row in bar_df.itertuples(index=False):
            element_id = getattr(row, rpr_1d.ELEMENT)
            start_node = getattr(row, rpr_1d.NODE_I)
            end_node = getattr(row, rpr_1d.NODE_J)
            elements_topology[element_id] = (start_node, end_node)

        bar_points: list[np.ndarray] = []
        bar_values: list[float] = []
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
                bar_points.append(start + fraction * (end - start))
                bar_values.append(value)
                line.append(len(bar_points) - 1)

            lines.extend(line)

        return Scene(
            node_map=node_map,
            model_view=model_scene.model_view,
            res_view=ResSceneData(
                kind=ResSceneKind.BAR_PROFILE,
                value_range=(
                    (
                        np.nanmin(bar_values),
                        np.nanmax(bar_values),
                    )
                    if bar_values
                    else (0.0, 0.0)
                ),
                data=ResElementSceneData(
                    nodes=np.array(bar_points),
                    values=np.array(bar_values),
                    connection=np.array(lines),
                ),
            ),
        )
