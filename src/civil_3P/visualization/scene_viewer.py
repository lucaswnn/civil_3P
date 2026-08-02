from __future__ import annotations

from typing import Any

import pyvista as pv
from pyvistaqt import QtInteractor
from PySide6.QtWidgets import QWidget
import numpy as np


class SceneViewer(QtInteractor):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.set_background("black")

    def _get_node_map(self,
                      scene: dict[str, dict[str, dict[str, Any]]],
                      ) -> tuple[dict[str, int], np.ndarray]:
        nodes = scene.get("nodes", {})
        if not nodes:
            self.render()
            return {}, []

        points = np.array(
            [
                (n["x"], n["y"], n["z"])
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
        bars = scene.get("bars", {})

        for bar in bars.values():
            start = node_map[bar["start"]]
            end = node_map[bar["end"]]

            cells.extend([2, start, end])
            celltypes.append(pv.CellType.LINE)

    def _load_shells(self,
                     scene: dict[str, dict[str, dict[str, Any]]],
                     node_map: dict[str, int],
                     cells: list[int],
                     celltypes: list[int]) -> None:
        shells = scene.get("shells", {})

        for shell in shells.values():
            if len(shell["nodes"]) == 3:
                ids = [
                    node_map[p]
                    for p in shell["nodes"]
                ]

                cells.extend([3, *ids])
                celltypes.append(pv.CellType.TRIANGLE)

            elif len(shell["nodes"]) == 4:
                ids = [
                    node_map[p]
                    for p in shell["nodes"]
                ]

                cells.extend([4, *ids])
                celltypes.append(pv.CellType.QUAD)

    def load_scene(
        self,
        scene: dict[str, dict[str, dict[str, Any]]],
    ) -> None:
        node_map, points = self._get_node_map(scene)

        bar_cells, shell_cells = [], []
        bar_celltypes, shell_celltypes = [], []
        self._load_bars(scene, node_map, bar_cells, bar_celltypes)
        self._load_shells(scene, node_map, shell_cells, shell_celltypes)
        
        bar_grid = pv.UnstructuredGrid(
            np.array(bar_cells),
            np.array(bar_celltypes),
            points)

        shell_grid = pv.UnstructuredGrid(
            np.array(shell_cells),
            np.array(shell_celltypes),
            points)        
        
        self.clear()
        self.add_mesh(bar_grid,
                      show_edges=True,
                      color="blue",
                      line_width=4.0)

        self.add_mesh(shell_grid,
                      show_edges=True,
                      edge_color="gray",
                      color="lightgray",
                      line_width=1.0)
        
        self.add_points(points,
                        color="red",
                        point_size=10.0,
                        render_points_as_spheres=True)
        
        self.reset_camera()
