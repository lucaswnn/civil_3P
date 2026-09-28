from __future__ import annotations

import pandas as pd
import pytest
from conftest import build_small_model

from civil_3P.core.res_data import ResData
from civil_3P.standard.model_components import ModelComponents as mc
from civil_3P.standard.task_res_repr import TaskNodeResCols as tnode
from civil_3P.visual.node_res_scene_builder import NodeResSceneBuilder


class TestNodeResSceneBuilder:
    @classmethod
    def setup_class(cls) -> None:
        cls.model = build_small_model()
        cls.builder = NodeResSceneBuilder()

    def test_build_res_scene_populates_res_view(self) -> None:
        res_df = pd.DataFrame(
            {
                tnode.NODE: ["N1", "N2"],
                tnode.VALUE: [1.5, 2.5],
            }
        )
        results = ResData(
            element_type=mc.NODES,
            res_df=res_df,
            elements=set(),
            nodes={"N1", "N2"},
        )

        scene = self.builder.build_res_scene(results, self.model)

        assert scene.res_view is not None
        assert scene.res_view.value_range == pytest.approx((1.5, 2.5))

    def test_build_res_scene_with_empty_results_has_zero_range(self) -> None:
        results = ResData(
            element_type=mc.NODES,
            res_df=pd.DataFrame(columns=[tnode.NODE, tnode.VALUE]),
            elements=set(),
            nodes=set(),
        )

        scene = self.builder.build_res_scene(results, self.model)

        assert scene
        assert scene.res_view.data.nodes.shape == (0,)
