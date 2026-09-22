from __future__ import annotations

import numpy as np
import pyvista as pv
from PySide6.QtWidgets import QWidget
from pyvistaqt import QtInteractor

from civil_3P.visualization.config import SceneViewerConfig
from civil_3P.visualization.result_view_data import ResultElementViewData
from civil_3P.visualization.scene import Scene


class SceneRenderer(QtInteractor):
    def __init__(
        self,
        parent: QWidget | None = None,
        config: SceneViewerConfig | None = None,
    ) -> None:
        super().__init__(parent)
        self._config = config or SceneViewerConfig()
        self.set_background(self._config.background_color)

    def load_scene(self, scene: Scene) -> None:
        model_view = scene.model_view
        self.clear()

        points = model_view.nodes
        if model_view.elements_1d_connection.size:
            bar_grid = pv.UnstructuredGrid(
                model_view.elements_1d_connection,
                model_view.elements_1d_type,
                points,
            )
            self.add_mesh(
                bar_grid,
                show_edges=True,
                color=self._config.element_1d_color,
                line_width=self._config.element_1d_line_width,
            )

        if model_view.elements_2d_connection.size:
            shell_grid = pv.UnstructuredGrid(
                model_view.elements_2d_connection,
                model_view.elements_2d_type,
                points,
            )
            self.add_mesh(
                shell_grid,
                show_edges=True,
                edge_color=self._config.edge_color,
                color=self._config.element_2d_color,
                line_width=self._config.element_2d_line_width,
            )

        if points.size:
            self.add_points(
                points,
                color=self._config.node_color,
                point_size=self._config.node_point_size,
                render_points_as_spheres=True,
            )

        self.reset_camera()

    def load_result_scene(self, scene: Scene) -> None:
        self.load_scene(scene)
        if scene.result_view is None:
            return

        data = scene.result_view.data
        if scene.result_view.kind.value == "node_points":
            self._render_points(data)
        elif scene.result_view.kind.value == "element_1d_profile":
            self._render_lines(data)
        else:
            self._render_cells(data, scene.result_view.value_range)

        self.reset_camera()

    def _render_points(self, data: ResultElementViewData) -> None:
        if not data.nodes.size:
            return
        self.add_points(
            data.nodes,
            scalars=data.values,
            point_size=self._config.result_node_point_size,
            render_points_as_spheres=True,
            cmap=self._config.colormap,
            show_scalar_bar=True,
        )

    def _render_lines(self, data: ResultElementViewData) -> None:
        if not data.nodes.size or data.connection is None:
            return
        poly = pv.PolyData(data.nodes)
        poly.lines = data.connection
        poly["value"] = data.values
        self.add_mesh(
            poly,
            scalars="value",
            cmap=self._config.colormap,
            line_width=self._config.result_element_1d_line_width,
            show_scalar_bar=True,
        )

    def _render_cells(
        self,
        data: ResultElementViewData,
        value_range: tuple[float, float],
    ) -> None:
        if not data.nodes.size or data.connection is None or data.element_type is None:
            return
        grid = pv.UnstructuredGrid(data.connection, data.element_type, data.nodes)
        grid.cell_data["value"] = np.asarray(data.values)
        self.add_mesh(
            grid,
            scalars="value",
            clim=value_range,
            cmap=self._config.colormap,
            show_edges=True,
            show_scalar_bar=True,
        )