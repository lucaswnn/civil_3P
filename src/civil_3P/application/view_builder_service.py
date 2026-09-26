from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from civil_3P.core.model import Model
    from civil_3P.core.result_data import ResultData
    from civil_3P.standard.result_components import ViewContentKind
    from civil_3P.visualization.scene import Scene
    from civil_3P.visualization.scene_builder_registry import SceneBuilderRegistry


class ViewBuilderService:
    _instance: ViewBuilderService | None = None

    def __new__(
        cls,
        scene_builder_registry: SceneBuilderRegistry,
    ) -> ViewBuilderService:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._registry = scene_builder_registry

        return cls._instance

    _registry: SceneBuilderRegistry

    def build_scene(
        self,
        model: Model,
    ) -> Scene:
        return self._registry.build_scene(model)

    def build_result_scene(
        self,
        results: ResultData,
        view_content_kind: ViewContentKind,
        model: Model,
    ) -> Scene:
        return self._registry.build_result_scene(
            results=results,
            view_content_kind=view_content_kind,
            model=model,
        )
