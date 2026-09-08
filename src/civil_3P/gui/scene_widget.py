from __future__ import annotations

from PySide6.QtWidgets import QVBoxLayout, QWidget
from typing import Any
from civil_3P.application.visualization_service import VisualizationService

from civil_3P.application.application_context import ApplicationContext
from civil_3P.visualization.config import SceneViewerConfig
from civil_3P.visualization.scene_renderer import SceneViewer


class SceneWidget(QWidget):
    def __init__(
        self,
        parent: QWidget,
        config: SceneViewerConfig,
        visualization_service: VisualizationService,
        context: ApplicationContext,
    ) -> None:
        super().__init__(parent)
        self._viewer = SceneViewer(self, config=config)
        self._layout = QVBoxLayout(self)
        self._layout.addWidget(self._viewer)
        self._visualization_service = visualization_service
        self._context = context

    def set_scene(self) -> None:
        model = self._context.current_model
        scene = self._visualization_service.build_scene(model)
        self._viewer.load_scene(scene)

    def set_result_scene(self) -> None:
        model = self._context.current_model
        scene = self._visualization_service.build_result_scene(model)
        self._viewer.load_result_scene(scene)
