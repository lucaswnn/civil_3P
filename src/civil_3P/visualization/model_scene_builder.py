from __future__ import annotations

from typing import TYPE_CHECKING

from civil_3P.visualization.scene_builder import SceneBuilder

if TYPE_CHECKING:
    from civil_3P.core.model import Model
    from civil_3P.core.result_data import ResultData
    from civil_3P.visualization.scene import Scene


class ModelSceneBuilder(SceneBuilder):
    def build_result_scene(
        self,
        results: ResultData,
        model: Model,
    ) -> Scene:
        return self.build_scene(model)
