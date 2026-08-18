from __future__ import annotations

from typing import Any

from PySide6.QtWidgets import QVBoxLayout, QWidget
from civil_3P.visualization.config import SceneViewerConfig
from civil_3P.visualization.scene_viewer import SceneViewer


class SceneWidget(QWidget):
    def __init__(
        self,
        parent: QWidget | None = None,
        config: SceneViewerConfig | None = None,
    ) -> None:
        super().__init__(parent)
        self._viewer = SceneViewer(self, config=config)
        self._layout = QVBoxLayout(self)
        self._layout.addWidget(self._viewer)

    def set_scene(self, scene: dict[str, dict[str, dict[str, Any]]]) -> None:
        self._viewer.load_scene(scene)
