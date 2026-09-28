from __future__ import annotations

import pandas as pd
import pytest
from conftest import build_small_model

from civil_3P.core.result_data import ResultData
from civil_3P.standard.model_components import ModelComponents as mc
from civil_3P.standard.task_result_representation import Task1DResultsColumns as t1d
from civil_3P.visualization.element_1d_result_scene_builder import (
    Element1DResultSceneBuilder,
)

class TestElement1DResultSceneBuilder:
    @classmethod
    def setup_class(cls) -> None:
        cls.model = build_small_model()
        cls.builder = Element1DResultSceneBuilder()

    def test_build_result_scene_creates_profile_points(self) -> None:
        result_df = pd.DataFrame(
            {
                t1d.ELEMENT: ["F1", "F1"],
                t1d.STATION: [0.0, 1.0],
                t1d.VALUE: [5.0, -5.0],
            }
        )
        results = ResultData(
            element_type=mc.ELEMENTS_1D,
            result_df=result_df,
            elements={"F1"},
            nodes={"N1", "N2"},
        )

        scene = self.builder.build_result_scene(results, self.model)

        assert scene.result_view.data.values.tolist() == [5.0, -5.0]
        assert scene.result_view.value_range == pytest.approx((-5.0, 5.0))

    def test_build_result_scene_with_unknown_element_yields_no_points(self) -> None:
        result_df = pd.DataFrame(
            {
                t1d.ELEMENT: ["UNKNOWN"],
                t1d.STATION: [0.0],
                t1d.VALUE: [1.0],
            }
        )
        results = ResultData(
            element_type=mc.ELEMENTS_1D,
            result_df=result_df,
            elements=set(),
            nodes=set(),
        )

        scene = self.builder.build_result_scene(results, self.model)

        assert scene.result_view.data.nodes.shape == (0,)

