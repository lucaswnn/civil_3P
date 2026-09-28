from __future__ import annotations

import pytest
import pyvista as pv
from conftest import build_small_model

from civil_3P.core.model import Model
from civil_3P.core.selection_context import SelectionContext
from civil_3P.standard.model_representation import ModelTables as mt
from civil_3P.visualization.model_scene_builder import ModelSceneBuilder


class TestModelSceneBuilder:
    @classmethod
    def setup_class(cls) -> None:
        cls.model = build_small_model()
        cls.builder = ModelSceneBuilder()

    def test_build_scene_maps_all_nodes(self) -> None:
        scene = self.builder.build_scene(self.model)

        assert set(scene.node_map.keys()) == {"N1", "N2", "N3", "N4", "N5"}
        assert scene.model_view.nodes.shape == (5, 3)

    def test_build_scene_creates_line_cell_for_1d_element(self) -> None:
        scene = self.builder.build_scene(self.model)

        assert scene.model_view.elements_1d_type.tolist() == [pv.CellType.LINE]
        # connectivity is [n_points, *point_indices] for a single 2-node line
        assert list(scene.model_view.elements_1d_connection) == [
            2,
            scene.node_map["N1"],
            scene.node_map["N2"],
        ]

    def test_build_scene_creates_quad_cell_for_2d_element(self) -> None:
        model = self.model.remove_elements(
            SelectionContext(
                node_ids=set(),
                element_1d_ids=set(),
                element_2d_ids={"A2"},
            ),
        )
        scene = self.builder.build_scene(model)

        assert scene.model_view.elements_2d_type.tolist() == [pv.CellType.QUAD]
        assert scene.model_view.elements_2d_connection[0] == 4

    def test_build_scene_creates_triangle_cell_for_2d_element(self) -> None:
        model = self.model.remove_elements(
            SelectionContext(
                node_ids=set(),
                element_1d_ids=set(),
                element_2d_ids={"A1"},
            ),
        )
        scene = self.builder.build_scene(model)

        assert scene.model_view.elements_2d_type.tolist() == [pv.CellType.TRIANGLE]
        assert scene.model_view.elements_2d_connection[0] == 3

    def test_build_scene_with_empty_model_has_no_elements(self) -> None:
        empty_scene = self.builder.build_scene(Model.empty())

        assert empty_scene.node_map == {}
        assert empty_scene.model_view.nodes.shape == (0,)

    def test_build_scene_with_dangling_element_raises_key_error(self) -> None:
        broken_model = self.model.copy()
        broken_model.tables[mt.ELEMENTS_1D].loc[0, "node_i"] = "GHOST"

        with pytest.raises(KeyError):
            self.builder.build_scene(broken_model)

    def test_build_result_scene_delegates_to_build_scene(self) -> None:
        result_scene = self.builder.build_result_scene(
            results=None,
            model=self.model,
        )
        model_scene = self.builder.build_scene(self.model)

        assert result_scene.node_map == model_scene.node_map
