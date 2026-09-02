from __future__ import annotations

from typing import Any

import pyvista as pv
from pyvistaqt import QtInteractor
from PySide6.QtWidgets import QWidget
import numpy as np

from civil_3P.standard import model_components as mc
from civil_3P.standard.result_components import (
    VisualizationContentKind,
    VisualizationData,
)
from civil_3P.visualization.config import SceneViewerConfig


class SceneViewer(QtInteractor):
    def __init__(
        self,
        parent: QWidget | None = None,
        config: SceneViewerConfig | None = None,
    ) -> None:
        super().__init__(parent)
        self._config = config or SceneViewerConfig()
        self.set_background(self._config.background_color)

    def _get_node_map(
        self,
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

    def _load_bars(
        self,
        scene: dict[str, dict[str, dict[str, Any]]],
        node_map: dict[str, int],
        cells: list[int],
        celltypes: list[int],
    ) -> None:
        bars = scene.get(mc.ModelComponents.ELEMENTS_1D, {})

        for bar in bars.values():
            start = node_map[bar[mc.ModelElement1DComponents.ELEMENT_1D_START_NODE]]
            end = node_map[bar[mc.ModelElement1DComponents.ELEMENT_1D_END_NODE]]

            cells.extend([2, start, end])
            celltypes.append(pv.CellType.LINE)

    def _load_shells(
        self,
        scene: dict[str, dict[str, dict[str, Any]]],
        node_map: dict[str, int],
        cells: list[int],
        celltypes: list[int],
        element_ids: list[str] | None = None,
    ) -> None:
        shells = scene.get(mc.ModelComponents.ELEMENTS_2D, {})

        for shell_id, shell in shells.items():
            if len(shell[mc.ModelElement2DComponents.ELEMENT_2D_NODES]) == 3:
                ids = [
                    node_map[p]
                    for p in shell[mc.ModelElement2DComponents.ELEMENT_2D_NODES]
                ]

                cells.extend([3, *ids])
                celltypes.append(pv.CellType.TRIANGLE)
                if element_ids is not None:
                    element_ids.append(str(shell_id))

            elif len(shell[mc.ModelElement2DComponents.ELEMENT_2D_NODES]) == 4:
                ids = [
                    node_map[p]
                    for p in shell[mc.ModelElement2DComponents.ELEMENT_2D_NODES]
                ]

                cells.extend([4, *ids])
                celltypes.append(pv.CellType.QUAD)
                if element_ids is not None:
                    element_ids.append(str(shell_id))

    def load_scene(
        self,
        scene: dict[str, dict[str, dict[str, Any]]],
    ) -> None:
        node_map, points = self._get_node_map(scene)

        element_1d_cells, element_2d_cells = [], []
        element_1d_celltypes, element_2d_celltypes = [], []
        self._load_bars(scene, node_map, element_1d_cells, element_1d_celltypes)
        self._load_shells(scene, node_map, element_2d_cells, element_2d_celltypes)

        bar_grid = pv.UnstructuredGrid(
            np.array(element_1d_cells), np.array(element_1d_celltypes), points
        )

        shell_grid = pv.UnstructuredGrid(
            np.array(element_2d_cells), np.array(element_2d_celltypes), points
        )

        self.clear()
        self.add_mesh(
            bar_grid,
            show_edges=True,
            color=self._config.element_1d_color,
            line_width=self._config.element_1d_line_width,
        )

        self.add_mesh(
            shell_grid,
            show_edges=True,
            edge_color=self._config.edge_color,
            color=self._config.element_2d_color,
            line_width=self._config.element_2d_line_width,
        )

        self.add_points(
            points,
            color=self._config.node_color,
            point_size=self._config.node_point_size,
            render_points_as_spheres=True,
        )

        self.reset_camera()

    def load_result_scene(self, scene: dict[str, Any]) -> None:
        visualization: VisualizationData = scene["visualization"]

        self.clear()

        result_scene = {
            mc.ModelComponents.NODES: {
                k: v
                for k, v in scene.get(mc.ModelComponents.NODES, {}).items()
                if k in visualization.nodes
            },
            mc.ModelComponents.ELEMENTS_1D: {
                k: v
                for k, v in scene.get(mc.ModelComponents.ELEMENTS_1D, {}).items()
                if k in visualization.elements
            },
            mc.ModelComponents.ELEMENTS_2D: {
                k: v
                for k, v in scene.get(mc.ModelComponents.ELEMENTS_2D, {}).items()
                if k in visualization.elements
            },
        }

        idle_scene = {
            mc.ModelComponents.NODES: {
                k: v
                for k, v in scene.get(mc.ModelComponents.NODES, {}).items()
            },
            mc.ModelComponents.ELEMENTS_1D: {
                k: v
                for k, v in scene.get(mc.ModelComponents.ELEMENTS_1D, {}).items()
                if k not in visualization.elements
            },
            mc.ModelComponents.ELEMENTS_2D: {
                k: v
                for k, v in scene.get(mc.ModelComponents.ELEMENTS_2D, {}).items()
                if k not in visualization.elements
            },
        }

        result_node_map, result_points = self._get_node_map(result_scene)

        self.load_scene(idle_scene)

        if visualization.kind == VisualizationContentKind.NODE_POINTS:
            self._render_node_points(result_points, result_node_map, visualization)
        elif visualization.kind == VisualizationContentKind.ELEMENT_1D_PROFILE:
            self._render_element_1d_profile(
                result_scene, result_node_map, result_points, visualization
            )
        elif visualization.kind == VisualizationContentKind.ELEMENT_2D_UNIFORM:
            self._render_element_2d_uniform(
                result_scene, result_node_map, result_points, visualization
            )
        elif visualization.kind == VisualizationContentKind.ELEMENT_2D_SHARED_NODES:
            self._render_element_2d_shared_nodes(
                result_scene, result_node_map, result_points, visualization
            )
        elif visualization.kind == VisualizationContentKind.ELEMENT_2D_ISOLATED_NODES:
            self._render_element_2d_isolated_nodes(result_scene, visualization)
        else:
            raise ValueError(f"Unsupported visualization kind: {visualization.kind}")

        self.reset_camera()

    def _render_node_points(
        self,
        points: np.ndarray,
        node_map: dict[str, int],
        visualization: VisualizationData,
    ) -> None:
        if not node_map:
            self.render()
            return

        values = np.full(points.shape[0], np.nan)
        for node_id, value in visualization.node_values.items():
            index = node_map.get(node_id)
            if index is not None:
                values[index] = value

        self.add_points(
            points,
            scalars=values,
            point_size=self._config.result_node_point_size,
            render_points_as_spheres=True,
            cmap=self._config.colormap,
            clim=visualization.value_range,
            show_scalar_bar=True,
        )

    def _render_element_1d_profile(
        self,
        scene: dict[str, Any],
        node_map: dict[str, int],
        points: np.ndarray,
        visualization: VisualizationData,
    ) -> None:
        bars = scene.get(mc.ModelComponents.ELEMENTS_1D, {})

        profile_points: list[np.ndarray] = []
        profile_values: list[float] = []
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
                fraction = 0.0 if length == 0 else min(max(station / length, 0.0), 1.0)
                profile_points.append(start + fraction * (end - start))
                profile_values.append(value)
                line.append(len(profile_points) - 1)
            lines.extend(line)

        if not profile_points:
            self.render()
            return

        poly = pv.PolyData()
        poly.points = np.array(profile_points)
        poly.lines = np.array(lines)
        poly["value"] = np.array(profile_values)

        self.add_mesh(
            poly,
            scalars="value",
            cmap=self._config.colormap,
            clim=visualization.value_range,
            line_width=self._config.result_element_1d_line_width,
            show_scalar_bar=True,
        )

    def _render_element_2d_uniform(
        self,
        scene: dict[str, Any],
        node_map: dict[str, int],
        points: np.ndarray,
        visualization: VisualizationData,
    ) -> None:
        cells: list[int] = []
        celltypes: list[int] = []
        element_ids: list[str] = []
        self._load_shells(scene, node_map, cells, celltypes, element_ids)

        if not cells:
            self.render()
            return

        shell_grid = pv.UnstructuredGrid(np.array(cells), np.array(celltypes), points)
        shell_grid.cell_data["value"] = np.array(
            [
                visualization.element_values.get(element_id, np.nan)
                for element_id in element_ids
            ]
        )

        self.add_mesh(
            shell_grid,
            scalars="value",
            show_edges=True,
            edge_color=self._config.edge_color,
            cmap=self._config.colormap,
            clim=visualization.value_range,
            show_scalar_bar=True,
        )

    def _render_element_2d_shared_nodes(
        self,
        scene: dict[str, Any],
        node_map: dict[str, int],
        points: np.ndarray,
        visualization: VisualizationData,
    ) -> None:
        cells: list[int] = []
        celltypes: list[int] = []
        self._load_shells(scene, node_map, cells, celltypes)

        if not cells:
            self.render()
            return

        shell_grid = pv.UnstructuredGrid(np.array(cells), np.array(celltypes), points)

        values = np.full(points.shape[0], 0.0)

        for node_id, value in visualization.element_node_values.items():
            index = node_map.get(node_id)
            if index is not None:
                values[index] = value

        shell_grid.point_data["value"] = values
        mesh = shell_grid.extract_surface(algorithm=None)
        banded = mesh.contour_banded(
            self._config.n_bands,
            rng=visualization.value_range,
            scalars="value",
            generate_contour_edges=False,
        )

        self.add_mesh(
            banded,
            scalars="value",
            cmap=self._config.colormap,
            clim=visualization.value_range,
            show_scalar_bar=True,
        )

        contour = mesh.contour(isosurfaces=self._config.n_bands)
        self.add_mesh(
            contour,
            color="black",
            line_width=2.0,
        )

    def _render_element_2d_isolated_nodes(
        self, scene: dict[str, Any], visualization: VisualizationData
    ) -> None:
        shells = scene.get(mc.ModelComponents.ELEMENTS_2D, {})
        nodes = scene.get(mc.ModelComponents.NODES, {})

        blocks = pv.MultiBlock()
        for element_id, node_values in visualization.element_node_values.items():
            shell = shells.get(element_id)
            if shell is None:
                continue

            node_ids = shell[mc.ModelElement2DComponents.ELEMENT_2D_NODES]
            local_points = np.array(
                [
                    (
                        nodes[node_id][mc.ModelNodeComponents.NODE_X],
                        nodes[node_id][mc.ModelNodeComponents.NODE_Y],
                        nodes[node_id][mc.ModelNodeComponents.NODE_Z],
                    )
                    for node_id in node_ids
                ],
                dtype=float,
            )
            values = np.array(
                [node_values.get(node_id, np.nan) for node_id in node_ids]
            )

            face = pv.PolyData(
                local_points, faces=[len(node_ids), *range(len(node_ids))]
            )
            face["value"] = values

            banded = face.contour_banded(
                self._config.n_bands,
                rng=visualization.value_range,
                scalars="value",
                generate_contour_edges=False,
            )
            blocks.append(banded)

        if len(blocks) == 0:
            self.render()
            return

        self.add_mesh(
            blocks,
            scalars="value",
            cmap=self._config.colormap,
            clim=visualization.value_range,
            show_scalar_bar=True,
        )
