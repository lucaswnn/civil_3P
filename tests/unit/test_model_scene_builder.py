from __future__ import annotations

import pytest
import pyvista as pv
from conftest import build_small_model

from civil_3P.core.model import Model
from civil_3P.core.sel_context import SelContext
from civil_3P.standard.model_repr import ModelTables as mt
from civil_3P.visual.model_scene_builder import ModelSceneBuilder


class TestModelSceneBuilder:
    @classmethod
    def setup_class(cls) -> None:
        cls.model = build_small_model()
        cls.builder = ModelSceneBuilder()

    def test_build_scene_maps_all_nodes(self) -> None:
        scene = self.builder.build_scene(self.model)

        assert set(scene.node_map.keys()) == {"N1", "N2", "N3", "N4", "N5"}
        assert scene.model_view.nodes.shape == (5, 3)

    def test_build_scene_creates_line_cell_for_bar(self) -> None:
        scene = self.builder.build_scene(self.model)

        assert scene.model_view.bars_type.tolist() == [pv.CellType.LINE]
        # connectivity is [n_points, *point_indices] for a single 2-node line
        assert list(scene.model_view.bars_connection) == [
            2,
            scene.node_map["N1"],
            scene.node_map["N2"],
        ]

    def test_build_scene_creates_quad_cell_for_shell(self) -> None:
        model = self.model.remove_elements(
            SelContext(
                node_ids=set(),
                bar_ids=set(),
                shell_ids={"A2"},
            ),
        )
        scene = self.builder.build_scene(model)

        assert scene.model_view.shells_type.tolist() == [pv.CellType.QUAD]
        assert scene.model_view.shells_connection[0] == 4

    def test_build_scene_creates_triangle_cell_for_2d_element(self) -> None:
        model = self.model.remove_elements(
            SelContext(
                node_ids=set(),
                bar_ids=set(),
                shell_ids={"A1"},
            ),
        )
        scene = self.builder.build_scene(model)

        assert scene.model_view.shells_type.tolist() == [pv.CellType.TRIANGLE]
        assert scene.model_view.shells_connection[0] == 3

    def test_build_scene_with_empty_model_has_no_elements(self) -> None:
        empty_scene = self.builder.build_scene(Model.empty())

        assert empty_scene.node_map == {}
        assert empty_scene.model_view.nodes.shape == (0,)

    def test_build_scene_with_dangling_element_raises_key_error(self) -> None:
        broken_model = self.model.copy()
        broken_model.tables[mt.BARS].loc[0, "node_i"] = "GHOST"

        with pytest.raises(KeyError):
            self.builder.build_scene(broken_model)

    def test_build_res_scene_delegates_to_build_scene(self) -> None:
        res_scene = self.builder.build_res_scene(
            results=None,
            model=self.model,
        )
        model_scene = self.builder.build_scene(self.model)

        assert res_scene.node_map == model_scene.node_map
