from __future__ import annotations

import pandas as pd
import pytest
from conftest import build_small_model

from civil_3P.core.result_data import ResultData
from civil_3P.standard.model_components import ModelComponents as mc
from civil_3P.standard.task_result_representation import TaskNodeResultsColumns as tnode
from civil_3P.visualization.node_result_scene_builder import NodeResultSceneBuilder


class TestNodeResultSceneBuilder:
    @classmethod
    def setup_class(cls) -> None:
        cls.model = build_small_model()
        cls.builder = NodeResultSceneBuilder()

    def test_build_result_scene_populates_result_view(self) -> None:
        result_df = pd.DataFrame(
            {
                tnode.NODE: ["N1", "N2"],
                tnode.VALUE: [1.5, 2.5],
            }
        )
        results = ResultData(
            element_type=mc.NODES,
            result_df=result_df,
            elements=set(),
            nodes={"N1", "N2"},
        )

        scene = self.builder.build_result_scene(results, self.model)

        assert scene.result_view is not None
        assert scene.result_view.value_range == pytest.approx((1.5, 2.5))

    def test_build_result_scene_with_empty_results_has_zero_range(self) -> None:
        results = ResultData(
            element_type=mc.NODES,
            result_df=pd.DataFrame(columns=[tnode.NODE, tnode.VALUE]),
            elements=set(),
            nodes=set(),
        )

        scene = self.builder.build_result_scene(results, self.model)

        assert scene
        assert scene.result_view.data.nodes.shape == (0,)
