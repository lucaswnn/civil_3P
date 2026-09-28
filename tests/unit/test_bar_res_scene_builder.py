from __future__ import annotations

import pandas as pd
import pytest
from conftest import build_small_model

from civil_3P.core.res_data import ResData
from civil_3P.standard.model_components import ModelComponents as mc
from civil_3P.standard.task_res_repr import TaskBarResCols as t1d
from civil_3P.visual.bar_res_scene_builder import (
    BarResSceneBuilder,
)


class TestBarResSceneBuilder:
    @classmethod
    def setup_class(cls) -> None:
        cls.model = build_small_model()
        cls.builder = BarResSceneBuilder()

    def test_build_res_scene_creates_profile_points(self) -> None:
        res_df = pd.DataFrame(
            {
                t1d.ELEMENT: ["F1", "F1"],
                t1d.STATION: [0.0, 1.0],
                t1d.VALUE: [5.0, -5.0],
            }
        )
        results = ResData(
            element_type=mc.BARS,
            res_df=res_df,
            elements={"F1"},
            nodes={"N1", "N2"},
        )

        scene = self.builder.build_res_scene(results, self.model)

        assert scene.res_view.data.values.tolist() == [5.0, -5.0]
        assert scene.res_view.value_range == pytest.approx((-5.0, 5.0))

    def test_build_res_scene_with_unknown_element_yields_no_points(self) -> None:
        res_df = pd.DataFrame(
            {
                t1d.ELEMENT: ["UNKNOWN"],
                t1d.STATION: [0.0],
                t1d.VALUE: [1.0],
            }
        )
        results = ResData(
            element_type=mc.BARS,
            res_df=res_df,
            elements=set(),
            nodes=set(),
        )

        scene = self.builder.build_res_scene(results, self.model)

        assert scene.res_view.data.nodes.shape == (0,)
