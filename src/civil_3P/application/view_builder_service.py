from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from civil_3P.core.model import FEMModel
    from civil_3P.core.result_builder import Visualization2DMode
    from civil_3P.core.selection import SelectionContext
    from civil_3P.core.result_data import ResultData
    from civil_3P.visualization.scene import Scene
    from civil_3P.visualization.scene_builder import SceneBuilder


class ViewBuilderService:
    def __init__(self, builder: SceneBuilder) -> None:
        self._builder = builder

    def build_scene(
        self,
        model: FEMModel,
    ) -> Scene:
        return self._builder.build_scene(model)

    def build_result_scene(
        self,
        model: FEMModel,
        results: ResultData,
        criteria: Visualization2DMode,
        selection: SelectionContext,
    ) -> Scene:
        return self._builder.build_result_scene(
            model,
            results,
            criteria,
            selection,
        )
