from __future__ import annotations

from PySide6.QtWidgets import QVBoxLayout, QWidget
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from civil_3P.gui.scene_widget_controller import SceneWidgetController
    from civil_3P.visualization.scene import Scene
    from civil_3P.visualization.scene_renderer import SceneRenderer


class SceneWidget(QWidget):
    def __init__(
        self,
        controller: SceneWidgetController,
        renderer: SceneRenderer,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self._controller = controller
        self._renderer = renderer
        layout = QVBoxLayout(self)
        layout.addWidget(renderer)

        controller.scene_ready.connect(self._render_scene)

    def _render_scene(self, scene: Scene) -> None:
        if scene.result_view is None:
            self._renderer.load_scene(scene)

        else:
            self._renderer.load_result_scene(scene)
