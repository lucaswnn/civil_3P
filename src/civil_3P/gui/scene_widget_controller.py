from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import QObject, Signal

if TYPE_CHECKING:
    from civil_3P.app.model_service import ModelService
    from civil_3P.app.res_builder_service import ResBuilderService
    from civil_3P.app.view_builder_service import ViewBuilderService
    from civil_3P.visual.scene import Scene


class SceneWidgetController(QObject):
    scene_ready = Signal(object)

    def __init__(
        self,
        model_service: ModelService,
        res_builder_service: ResBuilderService,
        view_builder_service: ViewBuilderService,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)
        self._model_service = model_service
        self._res_builder_service = res_builder_service
        self._view_builder_service = view_builder_service

    def set_model_scene(self) -> None:
        model = self._model_service.get_model()
        if model is None:
            raise ValueError("Cannot build a scene without a model")

        scene = self._view_builder_service.build_scene(model)
        self.scene_ready.emit(scene)

    def set_res_scene(self, scene: Scene) -> None:
        self.scene_ready.emit(scene)
