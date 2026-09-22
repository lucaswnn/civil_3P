from __future__ import annotations

from PySide6.QtCore import QObject, Signal

from civil_3P.application.model_service import ModelService
from civil_3P.application.result_builder_service import ResultBuilderService
from civil_3P.application.view_builder_service import ViewBuilderService
from civil_3P.visualization.scene import Scene


class SceneWidgetController(QObject):
    scene_ready = Signal(object)

    def __init__(
        self,
        model_service: ModelService,
        result_builder_service: ResultBuilderService,
        view_builder_service: ViewBuilderService,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)
        self._model_service = model_service
        self._result_builder_service = result_builder_service
        self._view_builder_service = view_builder_service

    def build_model_scene(self) -> Scene:
        model = self._model_service.get_model()
        if model is None:
            raise ValueError("Cannot build a scene without a model")

        scene = self._view_builder_service.build_scene(model)
        self.scene_ready.emit(scene)
        return scene