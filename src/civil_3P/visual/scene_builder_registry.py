from __future__ import annotations

from typing import TYPE_CHECKING

from civil_3P.standard.res_components import ResSceneKind as vk
from civil_3P.visual.bar_res_scene_builder import BarResSceneBuilder
from civil_3P.visual.model_scene_builder import (
    ModelSceneBuilder,
)
from civil_3P.visual.node_res_scene_builder import NodeResSceneBuilder
from civil_3P.visual.shell_isolated_res_scene_builder import (
    ShellIsolatedResSceneBuilder,
)
from civil_3P.visual.shell_shared_res_scene_builder import (
    ShellSharedResSceneBuilder,
)
from civil_3P.visual.shell_uniform_res_scene_builder import (
    ShellUniformResSceneBuilder,
)

if TYPE_CHECKING:
    from civil_3P.core.model import Model
    from civil_3P.core.res_data import ResData
    from civil_3P.visual.scene import Scene
    from civil_3P.visual.scene_builder import SceneBuilder


class SceneBuilderRegistry:
    def __init__(self) -> None:
        self._registry: dict[str, SceneBuilder] = {
            vk.NODE: NodeResSceneBuilder(),
            vk.BAR_PROFILE: BarResSceneBuilder(),
            vk.SHELL_UNIFORM: ShellUniformResSceneBuilder(),
            vk.SHELL_SHARED_NODES: ShellSharedResSceneBuilder(),
            vk.SHELL_ISOLATED_NODES: ShellIsolatedResSceneBuilder(),
        }
        self._model_builder = ModelSceneBuilder()

    def build_scene(
        self,
        model: Model,
    ) -> Scene:
        return self._model_builder.build_scene(model)

    def build_res_scene(
        self,
        results: ResData,
        view_content_kind: vk,
        model: Model,
    ) -> Scene:
        builder = self._registry[view_content_kind]

        return builder.build_res_scene(
            results=results,
            model=model,
        )
