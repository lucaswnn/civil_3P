from __future__ import annotations

from typing import TYPE_CHECKING

from civil_3P.visual.scene_builder import SceneBuilder

if TYPE_CHECKING:
    from civil_3P.core.model import Model
    from civil_3P.core.res_data import ResData
    from civil_3P.visual.scene import Scene


class ModelSceneBuilder(SceneBuilder):
    def build_res_scene(
        self,
        results: ResData,
        model: Model,
    ) -> Scene:
        return self.build_scene(model)
