from __future__ import annotations

import numpy as np
import pyvista as pv
from PySide6.QtWidgets import QWidget
from pyvistaqt import QtInteractor

from civil_3P.visualization.config import SceneViewerConfig
from civil_3P.visualization.result_scene_data import ResultElementSceneData
from civil_3P.visualization.scene import Scene
from civil_3P.standard.result_components import ViewContentKind


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
        if scene.result_view.kind == ViewContentKind.NODE_POINTS:
            self._render_points(data)
        elif scene.result_view.kind == ViewContentKind.ELEMENT_1D_PROFILE:
            self._render_lines(data)
        elif scene.result_view.kind == ViewContentKind.ELEMENT_2D_UNIFORM:
            self._render_uniform_cells(data, scene.result_view.value_range)
        elif scene.result_view.kind == ViewContentKind.ELEMENT_2D_SHARED_NODES:
            self._render_shared_cells(data, scene.result_view.value_range)
        elif scene.result_view.kind == ViewContentKind.ELEMENT_2D_ISOLATED_NODES:
            self._render_isolated_cells(data, scene.result_view.value_range)
        else:
            raise ValueError(f"Unsupported view content kind: {scene.result_view.kind}")

        self.reset_camera()

    def _render_points(self, data: ResultElementSceneData) -> None:
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

    def _render_lines(self, data: ResultElementSceneData) -> None:
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

    def _render_uniform_cells(
        self,
        data: ResultElementSceneData,
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

    def _render_shared_cells(
        self,
        data: ResultElementSceneData,
        value_range: tuple[float, float],
    ) -> None:
        grid = pv.UnstructuredGrid(data.connection, data.element_type, data.nodes)
        grid.point_data["value"] = data.values
        mesh = grid.extract_surface(algorithm=None)
        mesh = mesh.triangulate()
        refined_mesh = mesh.subdivide(nsub=3, subfilter="butterfly")
        banded = refined_mesh.contour_banded(
            self._config.n_bands,
            rng=value_range,
            scalars="value",
            generate_contour_edges=False,
        )

        self.add_mesh(
            banded,
            scalars="value",
            cmap=self._config.colormap,
            clim=value_range,
            show_scalar_bar=True,
        )

        contour = refined_mesh.contour(isosurfaces=self._config.n_bands)
        self.add_mesh(
            contour,
            color="black",
            line_width=2.0,
        )

    def _render_isolated_cells(
        self,
        data: ResultElementSceneData,
        value_range: tuple[float, float],
    ) -> None:
        blocks = pv.MultiBlock()
        contour_blocks = pv.MultiBlock()
        for local_points, faces, values in data.block_data:
            face = pv.PolyData(local_points, faces=faces)
            face["value"] = values
            banded = face.contour_banded(
                self._config.n_bands,
                rng=value_range,
                scalars="value",
                generate_contour_edges=False,
            )
            blocks.append(banded)

            contour = face.contour(isosurfaces=self._config.n_bands)
            contour_blocks.append(contour)

        if len(blocks) == 0:
            self.render()
            return

        self.add_mesh(
            blocks,
            scalars="value",
            cmap=self._config.colormap,
            clim=value_range,
            show_scalar_bar=True,
        )

        self.add_mesh(
            contour_blocks,
            color="black",
            line_width=2.0,
        )
