from __future__ import annotations

from typing import TYPE_CHECKING

from civil_3P.visualization.element_1d_result_scene_builder import (
    Element1DResultSceneBuilder
)
from civil_3P.visualization.element_2d_isolated_result_scene_builder import (
    Element2DIsolatedResultSceneBuilder
)
from civil_3P.visualization.element_2d_shared_result_scene_builder import (
    Element2DSharedResultSceneBuilder
)
from civil_3P.visualization.element_2d_uniform_result_scene_builder import (
    Element2DUniformResultSceneBuilder
)
from civil_3P.visualization.model_scene_builder import (
    ModelSceneBuilder,
)
from civil_3P.visualization.node_result_scene_builder import (
    NodeResultSceneBuilder
)
from civil_3P.standard.result_components import ViewContentKind as vk

if TYPE_CHECKING:
    from civil_3P.core.model import Model
    from civil_3P.core.result_data import ResultData
    from civil_3P.visualization.scene import Scene
    from civil_3P.visualization.scene_builder import SceneBuilder


class SceneBuilderRegistry:
    def __init__(self) -> None:
        self._registry: dict[str, SceneBuilder] = {
            vk.NODE_POINTS: NodeResultSceneBuilder(),
            vk.ELEMENT_1D_PROFILE: Element1DResultSceneBuilder(),
            vk.ELEMENT_2D_UNIFORM: Element2DUniformResultSceneBuilder(),
            vk.ELEMENT_2D_SHARED_NODES: Element2DSharedResultSceneBuilder(),
            vk.ELEMENT_2D_ISOLATED_NODES: Element2DIsolatedResultSceneBuilder(),
        }
        self._model_builder = ModelSceneBuilder()

    def build_scene(
        self,
        model: Model,
    ) -> Scene:
        return self._model_builder.build_scene(model)

    def build_result_scene(
        self,
        results: ResultData,
        view_content_kind: vk,
        model: Model,
    ) -> Scene:
        builder = self._registry[view_content_kind]

        return builder.build_result_scene(
            results=results,
            model=model,
        )
