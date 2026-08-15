from __future__ import annotations

from typing import Any
from enum import StrEnum

import pyvista as pv
from pyvistaqt import QtInteractor
from PySide6.QtWidgets import QWidget
import numpy as np

from civil_3P.standard import model_components as mc
from civil_3P.utils.colors import Colors


class SceneViewerConfig:
    def __init__(self) -> None:
        self.background_color = Colors.BLACK
        self.element_1d_color = Colors.BLUE
        self.element_2d_color = Colors.LIGHTGRAY
        self.edge_color = Colors.GRAY
        self.node_color = Colors.RED
        self.element_1d_line_width = 4.0
        self.element_2d_line_width = 1.0
        self.node_point_size = 5.0


class SceneViewer(QtInteractor):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._config = SceneViewerConfig()
        self.set_background(self._config.background_color)

    def _get_node_map(self,
                      scene: dict[str, dict[str, dict[str, Any]]],
                      ) -> tuple[dict[str, int], np.ndarray]:
        nodes = scene.get(mc.ModelComponents.NODES, {})
        if not nodes:
            self.render()
            return {}, []

        points = np.array(
            [
                (
                    n[mc.ModelNodeComponents.NODE_X],
                    n[mc.ModelNodeComponents.NODE_Y],
                    n[mc.ModelNodeComponents.NODE_Z],
                )
                for n in nodes.values()
            ],
            dtype=float,
        )

        return {id: i for i, id in enumerate(nodes.keys())}, points

    def _load_bars(self,
                   scene: dict[str, dict[str, dict[str, Any]]],
                   node_map: dict[str, int],
                   cells: list[int],
                   celltypes: list[int]) -> None:
        bars = scene.get(mc.ModelComponents.ELEMENTS_1D, {})

        for bar in bars.values():
            start = node_map[bar[mc.ModelElement1DComponents.ELEMENT_1D_START_NODE]]
            end = node_map[bar[mc.ModelElement1DComponents.ELEMENT_1D_END_NODE]]

            cells.extend([2, start, end])
            celltypes.append(pv.CellType.LINE)

    def _load_shells(self,
                     scene: dict[str, dict[str, dict[str, Any]]],
                     node_map: dict[str, int],
                     cells: list[int],
                     celltypes: list[int]) -> None:
        shells = scene.get(mc.ModelComponents.ELEMENTS_2D, {})

        for shell in shells.values():
            if len(shell[mc.ModelElement2DComponents.ELEMENT_2D_NODES]) == 3:
                ids = [
                    node_map[p]
                    for p in shell[mc.ModelElement2DComponents.ELEMENT_2D_NODES]
                ]

                cells.extend([3, *ids])
                celltypes.append(pv.CellType.TRIANGLE)

            elif len(shell[mc.ModelElement2DComponents.ELEMENT_2D_NODES]) == 4:
                ids = [
                    node_map[p]
                    for p in shell[mc.ModelElement2DComponents.ELEMENT_2D_NODES]
                ]

                cells.extend([4, *ids])
                celltypes.append(pv.CellType.QUAD)

    def load_scene(
        self,
        scene: dict[str, dict[str, dict[str, Any]]],
    ) -> None:
        node_map, points = self._get_node_map(scene)

        element_1d_cells, element_2d_cells = [], []
        element_1d_celltypes, element_2d_celltypes = [], []
        self._load_bars(scene, node_map, element_1d_cells,
                        element_1d_celltypes)
        self._load_shells(scene, node_map, element_2d_cells,
                          element_2d_celltypes)

        bar_grid = pv.UnstructuredGrid(
            np.array(element_1d_cells),
            np.array(element_1d_celltypes),
            points)

        shell_grid = pv.UnstructuredGrid(
            np.array(element_2d_cells),
            np.array(element_2d_celltypes),
            points)

        self.clear()
        self.add_mesh(bar_grid,
                      show_edges=True,
                      color=self._config.element_1d_color,
                      line_width=self._config.element_1d_line_width)

        self.add_mesh(shell_grid,
                      show_edges=True,
                      edge_color=self._config.edge_color,
                      color=self._config.element_2d_color,
                      line_width=self._config.element_2d_line_width)

        self.add_points(points,
                        color=self._config.node_color,
                        point_size=self._config.node_point_size,
                        render_points_as_spheres=True)

        self.reset_camera()
