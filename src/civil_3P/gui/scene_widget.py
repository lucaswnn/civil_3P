from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtWidgets import QVBoxLayout, QWidget

if TYPE_CHECKING:
    from civil_3P.gui.scene_widget_controller import SceneWidgetController
    from civil_3P.visual.scene import Scene
    from civil_3P.visual.scene_renderer import SceneRenderer


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
        if scene.res_view is None:
            self._renderer.load_scene(scene)

        else:
            self._renderer.load_res_scene(scene)
